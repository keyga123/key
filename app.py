
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

DATABASE = os.environ.get("DATABASE_PATH", "keys.db")
LINK4M_API_KEY = os.environ.get("LINK4M_API_KEY", "").strip()


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


HOME = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GA GAMING VIP</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;min-height:100vh;padding:20px;
 display:flex;align-items:center;justify-content:center;
 background:#0b0c10;color:white;
 font-family:Arial,sans-serif
}
.card{
 width:100%;max-width:480px;padding:36px 24px;
 background:#1f2833;border:2px solid #66fcf1;
 border-radius:28px;text-align:center;
 box-shadow:0 15px 40px #0008
}
h1{color:#66fcf1;font-size:27px}
p{color:#c5c6c7;line-height:1.6}
button,.btn{
 display:block;width:100%;padding:17px 12px;
 background:linear-gradient(45deg,#66fcf1,#45f3ff);
 border:0;border-radius:14px;color:#0b0c10;
 font-size:17px;font-weight:bold;text-decoration:none;
 cursor:pointer
}
button:disabled{opacity:.6}
#message{overflow-wrap:anywhere}
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
 msg.textContent='Đang tạo link...';
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
            message="Chưa cấu hình LINK4M_API_KEY trên Render."
        ), 500

    target = request.url_root.rstrip("/") + "/claim-key"

    try:
        response = requests.get(
            "https://link4m.com/api",
            params={"api": LINK4M_API_KEY, "url": target},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        short_url = (
            data.get("shortenedUrl")
            or data.get("shortened_url")
        )

        if data.get("status") != "success" or not short_url:
            app.logger.warning("Link4M response: %s", data)
            return jsonify(
                success=False,
                message="Link4M không tạo được link. Kiểm tra API key và định dạng API."
            ), 502

        parsed = urlparse(short_url)
        if parsed.scheme != "https" or not parsed.netloc:
            return jsonify(
                success=False,
                message="Link4M trả về URL không hợp lệ."
            ), 502

        return jsonify(success=True, url=short_url)

    except requests.RequestException:
        app.logger.exception("Link4M request failed")
        return jsonify(
            success=False,
            message="Không kết nối được Link4M. Kiểm tra Render Logs."
        ), 502
    except (ValueError, AttributeError):
        app.logger.exception("Invalid Link4M response")
        return jsonify(
            success=False,
            message="Phản hồi API Link4M không hợp lệ."
        ), 502


@app.get("/claim-key")
def claim_key():
    # Đây là trang cấp key mẫu; chưa xác minh hoàn thành Link4M.
    # Không dùng làm xác thực bản quyền thực tế cho tới khi tích hợp
    # callback/token xác nhận hợp lệ từ nhà cung cấp.
    new_key = "GA-" + secrets.token_hex(4).upper()

    expiry = now_utc() + timedelta(hours=24)

    try:
        with connect_db() as conn:
            conn.execute(
                "INSERT INTO keys (key, expiry, created_at) VALUES (?, ?, ?)",
                (
                    new_key,
                    expiry.isoformat(),
                    now_utc().isoformat()
                )
            )
    except sqlite3.Error:
        app.logger.exception("Database write failed")
        return "Không lưu được key. Vui lòng thử lại sau.", 500

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>GA GAMING - Key</title>
      <style>
      body{background:#0b0c10;color:white;font-family:Arial;
      min-height:100vh;display:flex;align-items:center;
      justify-content:center;margin:0;padding:16px}
      .card{background:#1f2833;border:2px solid #66fcf1;
      border-radius:24px;padding:30px 20px;text-align:center;
      width:100%;max-width:440px}
      h2,.key{color:#66fcf1}
      .key{padding:16px;background:#0b0c10;
      overflow-wrap:anywhere;font-weight:bold;font-size:22px}
      a,button{display:inline-block;margin-top:20px;padding:13px;
      border:0;border-radius:10px;background:#66fcf1;
      color:#0b0c10;font-weight:bold;text-decoration:none}
      </style>
    </head>
    <body><main class="card">
      <h2>🎉 KEY ĐÃ ĐƯỢC TẠO</h2>
      <p>Key có thời hạn 24 giờ kể từ khi tạo.</p>
      <div class="key" id="key">{{ key }}</div>
      <button onclick="copyKey()">SAO CHÉP KEY</button>
      <p id="status"></p>
      <a href="/">Quay về trang chủ</a>
      <script>
      async function copyKey(){
        try{
          await navigator.clipboard.writeText(
            document.getElementById('key').textContent
          );
          document.getElementById('status').textContent='Đã sao chép!';
        }catch(e){
          document.getElementById('status').textContent=
            'Hãy nhấn giữ key để sao chép.';
        }
      }
      </script>
    </main></body></html>
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
        app.logger.exception("Database read failed")
        return jsonify(success=False, message="Lỗi cơ sở dữ liệu."), 500

    if record is None:
        return jsonify(
            success=False,
            message="Key không tồn tại."
        ), 404

    expiry = datetime.fromisoformat(record["expiry"])

    if now_utc() >= expiry:
        return jsonify(
            success=False,
            message="Key đã hết hạn."
        ), 403

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
