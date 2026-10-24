from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import random
import string
import urllib.parse

app = Flask(__name__)

# Database lưu trữ Key
keys_db = {
    "GA-GAMING-VIP-2026": {
        "expiry": (datetime.now() + timedelta(days=30)).timestamp(),
        "ip": "all",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
}

# --- TRANG CHỦ: DÙNG LINK ĐIỀU HƯỚNG TRỰC TIẾP CHUẨN XÁC 100% ---
@app.route('/')
def index():
    token = "67d2f1b7f42a7c6c275420ab"  # Token Link4M của ông
    target_url = "https://gagaming-key-system.onrender.com/claim-key"
    
    # URL chuẩn theo tài liệu của Link4M
    link4m_direct_url = f"https://link4m.com/st?api={token}&url={urllib.parse.quote(target_url)}"

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GA Gaming - Key System</title>
        <style>
            :root {{
                --bg: #0d0e15;
                --card: #161822;
                --accent: #00ffcc;
                --text: #ffffff;
                --text-muted: #8b9bb4;
            }}
            body {{
                background-color: var(--bg);
                color: var(--text);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: var(--card);
                border: 1px solid rgba(0, 255, 204, 0.2);
                padding: 40px 30px;
                border-radius: 20px;
                text-align: center;
                max-width: 400px;
                width: 90%;
                box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            }}
            h1 {{
                font-size: 22px;
                color: var(--accent);
                margin-bottom: 10px;
            }}
            p {{
                color: var(--text-muted);
                font-size: 14px;
                margin-bottom: 25px;
            }}
            .btn {{
                background: linear-gradient(135deg, #00ffcc, #00b3ff);
                color: #0d0e15;
                padding: 16px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 10px;
                display: block;
                width: 100%;
                box-sizing: border-box;
                cursor: pointer;
                font-size: 16px;
                transition: opacity 0.2s, transform 0.2s;
                box-shadow: 0 5px 15px rgba(0, 255, 204, 0.3);
            }}
            .btn:hover {{
                opacity: 0.9;
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🛡️ GA GAMING SYSTEM</h1>
            <p>Vượt link Link4M tự động để nhận key bản quyền 24h.</p>
            <a href="{link4m_direct_url}" class="btn">⚡ LẤY KEY QUA LINK4M</a>
        </div>
    </body>
    </html>
    """

# --- TRANG NHẬN KEY VÀ SAO CHÉP 1 CHẠM ---
@app.route('/claim-key')
def claim_key():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_key = f"GA-{p1}-{p2}"
    
    expiry_time = datetime.now().timestamp() + (24 * 3600)
    keys_db[new_key] = {
        "expiry": expiry_time,
        "ip": user_ip,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thành Công - GA Gaming</title>
        <style>
            body {
                background-color: #0d0e15;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: #161822;
                border: 1px solid rgba(0, 255, 204, 0.2);
                padding: 40px 30px;
                border-radius: 20px;
                text-align: center;
                max-width: 400px;
                width: 90%;
                box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            }
            h1 {
                font-size: 22px;
                color: #00ffcc;
                margin-bottom: 10px;
            }
            p {
                color: #8b9bb4;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .key-box {
                background: #0d0e15;
                border: 1px dashed #00ffcc;
                padding: 15px;
                border-radius: 10px;
                color: #00ffcc;
                font-size: 20px;
                font-weight: bold;
                word-break: break-all;
                margin-bottom: 20px;
            }
            .btn-copy {
                background: #00ffcc;
                color: #0d0e15;
                padding: 14px 20px;
                font-weight: bold;
                border-radius: 10px;
                border: none;
                width: 100%;
                cursor: pointer;
                font-size: 16px;
                margin-bottom: 12px;
                transition: 0.2s;
            }
            .btn-copy:hover {
                opacity: 0.9;
                transform: translateY(-2px);
            }
            .btn-home {
                background: transparent;
                color: #8b9bb4;
                padding: 10px;
                text-decoration: none;
                font-size: 14px;
                display: block;
            }
            .btn-home:hover {
                color: white;
            }
            #toast {
                font-size: 13px;
                color: #00ffcc;
                height: 15px;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎉 VƯỢT LINK THÀNH CÔNG</h1>
            <p>Mã key bản quyền 24h của bạn:</p>
            <div class="key-box" id="keyText">""" + new_key + """</div>
            <button onclick="copyKey()" class="btn-copy">📋 SAO CHÉP KEY</button>
            <div id="toast"></div>
            <a href="/" class="btn-home">← Quay lại trang chủ</a>
        </div>

        <script>
            function copyKey() {
                const text = document.getElementById('keyText').innerText;
                navigator.clipboard.writeText(text).then(() => {
                    document.getElementById('toast').innerText = "Đã sao chép key vào bộ nhớ tạm!";
                    setTimeout(() => { document.getElementById('toast').innerText = ""; }, 3000);
                }).catch(() => {
                    alert("Không thể sao chép tự động, vui lòng copy thủ công!");
                });
            }
        </script>
    </body>
    </html>
    """
    return html_content

# --- API XÁC THỰC KEY TRONG GAME ---
@app.route('/api/check-key', methods=['POST'])
def api_check_key():
    data = request.json or request.form
    key = data.get('key', '').strip()
    now_ts = datetime.now().timestamp()
    
    if not key:
        return jsonify({'success': False, 'message': 'Thiếu tham số key!'})
        
    key_info = keys_db.get(key)
    if not key_info:
        return jsonify({'success': False, 'message': 'Key không tồn tại!'})
        
    if now_ts > key_info['expiry']:
        return jsonify({'success': False, 'message': 'Key đã hết hạn sử dụng!'})
        
    return jsonify({
        'success': True, 
        'message': 'Key hợp lệ!', 
        'expires_at': datetime.fromtimestamp(key_info['expiry']).strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
