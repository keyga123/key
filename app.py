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

# --- TRANG 1: TRANG CHỦ (Điều hướng thẳng bằng cấu trúc chuẩn Link4M) ---
@app.route('/')
def index():
    token = "67d2f1b7f42a7c6c275420ab"  # Token Link4M của ông
    target_url = "https://gagaming-key-system.onrender.com/claim-key"
    
    # Sử dụng chuẩn cấu trúc định hướng trực tiếp của Link4M
    link4m_url = f"https://link4m.com/st?api={token}&url={urllib.parse.quote(target_url)}"

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GA Gaming - Key System</title>
        <style>
            :root {{
                --bg-color: #0b0c10;
                --card-bg: #1f2833;
                --primary: #66fcf1;
                --text-main: #ffffff;
                --text-sub: #c5c6c7;
            }}
            body {{
                background-color: var(--bg-color);
                color: var(--text-main);
                font-family: 'Poppins', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: var(--card-bg);
                border: 2px solid var(--primary);
                padding: 40px 30px;
                border-radius: 24px;
                text-align: center;
                max-width: 420px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            }}
            h1 {{
                font-size: 24px;
                background: linear-gradient(to right, #66fcf1, #45f3ff, #ff007f);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 12px;
            }}
            p {{
                color: var(--text-sub);
                font-size: 14px;
                margin-bottom: 30px;
            }}
            .btn {{
                background: linear-gradient(45deg, #66fcf1, #45f3ff);
                color: #0b0c10;
                padding: 16px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 14px;
                display: block;
                width: 100%;
                box-sizing: border-box;
                cursor: pointer;
                border: none;
                font-size: 16px;
                transition: transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 5px 15px rgba(102, 252, 241, 0.4);
            }}
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(102, 252, 241, 0.6);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔑 GA GAMING VIP</h1>
            <p>Hoàn thành vượt link Link4M để nhận key bản quyền 24h.</p>
            <a href="{link4m_url}" class="btn">⚡ LẤY KEY QUA LINK4M</a>
        </div>
    </body>
    </html>
    """

# --- TRANG 2: TRANG NHẬN VÀ COPY KEY ---
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

    html_content = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nhận Key Thành Công</title>
        <style>
            body {{
                background-color: #0b0c10;
                color: white;
                font-family: 'Poppins', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .box {{
                background: #1f2833;
                border: 2px solid #66fcf1;
                padding: 40px 30px;
                border-radius: 24px;
                text-align: center;
                max-width: 450px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            }}
            h1 {{
                color: #66fcf1;
                font-size: 22px;
                margin-bottom: 12px;
            }}
            p {{
                color: #c5c6c7;
                font-size: 14px;
                margin-bottom: 20px;
            }}
            .key-box {{
                background: #0b0c10;
                border: 1px dashed #66fcf1;
                padding: 16px;
                border-radius: 12px;
                color: #66fcf1;
                font-size: 20px;
                font-weight: bold;
                word-break: break-all;
                margin-bottom: 20px;
                box-shadow: inset 0 0 10px rgba(102, 252, 241, 0.2);
            }}
            .btn-copy {{
                background: #66fcf1;
                color: #0b0c10;
                padding: 14px 20px;
                font-weight: bold;
                border-radius: 12px;
                border: none;
                width: 100%;
                cursor: pointer;
                font-size: 16px;
                margin-bottom: 12px;
                transition: 0.2s;
                box-shadow: 0 5px 15px rgba(102, 252, 241, 0.4);
            }}
            .btn-copy:hover {{
                opacity: 0.9;
                transform: translateY(-2px);
            }}
            .btn-home {{
                background: #ff007f;
                color: white;
                padding: 12px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 12px;
                display: block;
                transition: 0.2s;
            }}
            .btn-home:hover {{
                opacity: 0.9;
            }}
            #toast {{
                margin-top: 12px;
                font-size: 13px;
                color: #45f3ff;
                font-weight: bold;
                height: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 VƯỢT LINK THÀNH CÔNG!</h1>
            <p>Mã key bản quyền 24h của bạn:</p>
            <div class="key-box" id="keyText">""" + new_key + f"""</div>
            <button onclick="copyKey()" class="btn-copy">📋 SAO CHÉP KEY</button>
            <div id="toast"></div>
            <a href="/" class="btn-home">← Quay Về Trang Chủ</a>
        </div>

        <script>
            function copyKey() {{
                const keyElement = document.getElementById('keyText').innerText;
                navigator.clipboard.writeText(keyElement).then(() => {{
                    document.getElementById('toast').innerText = "Đã sao chép key vào bộ nhớ tạm!";
                    setTimeout(() => {{
                        document.getElementById('toast').innerText = "";
                    }}, 3000);
                }}).catch(err => {{
                    alert("Không thể tự động copy, hãy bôi đen và copy thủ công nhé!");
                }});
            }}
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
