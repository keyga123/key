import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# API key do người quản trị cung cấp.
# Cảnh báo: không công khai file này lên GitHub hoặc nơi công cộng.
LINK4M_API_KEY = "67d2f114875f8e29865d1fa9"

# Render: nên gắn Persistent Disk và đặt DATABASE_PATH vào disk mount path
# nếu muốn SQLite tồn tại qua lần deploy/restart.
DATABASE = os.environ.get("DATABASE_PATH", "keys.db")


def now_utc():
    return datetime.now(timezone.utc)


def connect_db():
    conn = sqlite3.connect(DATABASE, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key TEXT PRIMARY KEY,
                expiry TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


init_db()

HOME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b0c10">
<title>GA GAMING VIP - Key System</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;min-height:100vh;padding:20px;
 display:flex;align-items:center;justify-content:center;
 background:#0b0c10;color:#fff;font-family:Arial,sans-serif
}
.card{
 width:100%;max-width:480px;padding:38px 24px;
 background:#1f2833;border:2px solid #66fcf1;
 border-radius:30px;text-align:center;
 box-shadow:0 15px 40px #0008
}
h1{color:#66fcf1;font-size:clamp(23px,6vw,30px)}
p{color:#c5c6c7;line-height:1.6}
button,.btn{
 display:block;width:100%;padding:18px 12px;
 background:linear-gradient(45deg,#66fcf1,#45f3ff);
 border:0;border-radius:15px;color:#0b0c10;
 font-size:17px;font-weight:bold;text-decoration:none;cursor:pointer
}
button:disabled{opacity:.6;cursor:wait}
#message{overflow-wrap:anywhere;min-height:24px}
</style>
</head>
<body>
<main class="card">
<h1>🔑 GA GAMING VIP</h1>
<p>Hệ thống lấy key GA GAMING VIP thời hạn 24 giờ.</p>
<button id="btn" onclick="getLink()">⚡ LẤY KEY QUA LINK4M</button>
<p id="message" role="status" aria-live="polite"></p>
</main>
<script>
async function getLink(){
 const btn=document.getElementById('btn');
 const msg=document.getElementById('message');
 btn.disabled=true;
 msg.style.color='#66fcf1';
 msg.textContent='Đang tạo link, vui lòng chờ...';
 try{
   const res=await fetch('/create-link',{method:'POST'});
   const data=await res.json();
   if(!res.ok || !data.success) throw Error(data.message||'Có lỗi xảy ra');
   const url=new URL(data.url);
   if(url.protocol!=='https:') throw Error('URL không an toàn');
   location.href=url.href;
 }catch(e){
   msg.style.color='#ff007f';
   msg.textContent='Lỗi: '+e.message;
   btn.disabled=false;
 }
}
</script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(HOME)


@app.post("/create-link")
def create_link():
    if not LINK4M_API_KEY:
        return jsonify(
            success=False,
            message="Chưa cấu hình API key Link4M."
        ), 500

    target_url = request.url_root.rstrip("/") + "/claim-key"

    try:
        response = requests.get(
            "https://link4m.com/api",
            params={"api": LINK4M_API_KEY, "url": target_url},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        short_url = data.get("shortenedUrl") or data.get("shortened_url")
        if data.get("status") != "success" or not short_url:
            # Không ghi API key vào log.
            app.logger.warning("Link4M did not return a successful short URL")
            return jsonify(
                success=False,
                message="Link4M không tạo được link. Hãy kiểm tra API key và định dạng API."
            ), 502

        parsed = urlparse(short_url)
        if parsed.scheme != "https" or not parsed.netloc:
            return jsonify(
                success=False,
                message="Link4M trả về URL không hợp lệ."
            ), 502

        return jsonify(success=True, url=short_url)

    except requests.RequestException:
        app.logger.exception("Yêu cầu tới Link4M thất bại")
        return jsonify(
            success=False,
            message="Không kết nối được Link4M. Hãy kiểm tra Render Logs."
        ), 502
    except (ValueError, AttributeError):
        app.logger.exception("Phản hồi Link4M không hợp lệ")
        return jsonify(
            success=False,
            message="Phản hồi API Link4M không hợp lệ."
        ), 502


@app.get("/claim-key")
def claim_key():
    # QUAN TRỌNG:
    # Route này hiện tạo key khi được mở trực tiếp.
    # Muốn bắt buộc hoàn thành Link4M, cần tích hợp cơ chế xác minh
    # chính thức do Link4M cung cấp; chuyển hướng về URL này tự nó
    # không chứng minh người dùng đã hoàn thành nhiệm vụ.
    new_key = "GA-" + secrets.token_hex(4).upper()
    expiry = now_utc() + timedelta(hours=24)

    try:
        with connect_db() as conn:
            conn.execute(
                "INSERT INTO keys (key, expiry, created_at) VALUES (?, ?, ?)",
                (new_key, expiry.isoformat(), now_utc().isoformat())
            )
    except sqlite3.Error:
        app.logger.exception("Không ghi được key vào cơ sở dữ liệu")
        return "Không lưu được key. Vui lòng thử lại sau.", 500

    return render_template_string("""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GA GAMING VIP - Key</title>
<style>
*{box-sizing:border-box}
body{background:#0b0c10;color:#fff;font-family:Arial,sans-serif;
min-height:100vh;display:flex;align-items:center;justify-content:center;
margin:0;padding:16px}
.card{background:#1f2833;border:2px solid #66fcf1;border-radius:24px;
padding:30px 20px;text-align:center;width:100%;max-width:440px}
h2,.key{color:#66fcf1}
p{color:#c5c6c7;line-height:1.6}
.key{padding:16px;background:#0b0c10;border:1px dashed #66fcf1;
border-radius:12px;overflow-wrap:anywhere;font-weight:bold;font-size:22px}
button,a{display:inline-block;margin-top:20px;padding:13px 18px;
border:0;border-radius:10px;background:#66fcf1;color:#0b0c10;
font-weight:bold;text-decoration:none;cursor:pointer}
</style>
</head>
<body>
<main class="card">
<h2>🎉 KEY ĐÃ ĐƯỢC TẠO</h2>
<p>Key có thời hạn 24 giờ kể từ lúc tạo.</p>
<div class="key" id="key">{{ key }}</div>
<button onclick="copyKey()">SAO CHÉP KEY</button>
<p id="status" role="status"></p>
<a href="/">Quay về trang chủ</a>
<script>
async function copyKey(){
 const value=document.getElementById('key').textContent;
 try{
   await navigator.clipboard.writeText(value);
   document.getElementById('status').textContent='Đã sao chép key!';
 }catch(e){
   document.getElementById('status').textContent=
     'Trình duyệt không cho sao chép tự động. Hãy nhấn giữ key để sao chép.';
 }
}
</script>
</main>
</body>
</html>
""", key=new_key)


@app.post("/api/check-key")
def api_check_key():
    data = request.get_json(silent=True) or request.form
    key = str(data.get("key", "")).strip()

    if not key:
        return jsonify(success=False, message="Thiếu key."), 400

    try:
        with connect_db() as conn:
            record = conn.execute(
                "SELECT key, expiry FROM keys WHERE key = ?",
                (key,)
            ).fetchone()
    except sqlite3.Error:
        app.logger.exception("Không đọc được cơ sở dữ liệu")
        return jsonify(success=False, message="Lỗi cơ sở dữ liệu."), 500

    if record is None:
        return jsonify(success=False, message="Key không tồn tại."), 404

    expiry = datetime.fromisoformat(record["expiry"])
    if now_utc() >= expiry:
        return jsonify(success=False, message="Key đã hết hạn."), 403

    return jsonify(
        success=True,
        message="Key hợp lệ.",
        expires_at=expiry.isoformat()
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
