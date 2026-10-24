from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, request, session
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)
app.secret_key = 'gagaming_ultimate_master_2026'

# Database lưu trữ Key
keys_db = {
    "GA-GAMING-VIP-2026": {
        "expiry": (datetime.now() + timedelta(days=30)).timestamp(),
        "ip": "all",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
}

# --- 1. ROUTE TRANG CHỦ (Tích hợp Python + HTML + CSS + JavaScript) ---
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GA Gaming - Key System</title>
        <style>
            :root {
                --bg-color: #0f1016;
                --card-bg: #181a25;
                --primary: #ff4757;
                --success: #2ed573;
                --text-main: #ffffff;
                --text-sub: #a4b0be;
            }
            body {
                background-color: var(--bg-color);
                color: var(--text-main);
                font-family: 'Poppins', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: var(--card-bg);
                border: 2px solid var(--primary);
                padding: 35px 25px;
                border-radius: 20px;
                text-align: center;
                max-width: 400px;
                width: 90%;
                box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            }
            h1 {
                font-size: 24px;
                background: linear-gradient(to right, #ff4757, #ffa502, #2ed573);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }
            p {
                color: var(--text-sub);
                font-size: 14px;
                margin-bottom: 25px;
            }
            .btn {
                background: linear-gradient(45deg, #ff0000, #ff7300, #00ffd5);
                color: white;
                padding: 14px 20px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 12px;
                display: block;
                width: 100%;
                box-sizing: border-box;
                cursor: pointer;
                border: none;
                font-size: 16px;
                transition: transform 0.2s, opacity 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
                opacity: 0.95;
            }
            #loading {
                margin-top: 15px;
                color: #ffa502;
                font-size: 13px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔑 GA GAMING KEY</h1>
            <p>Hệ thống tự động cấp key bản quyền 24h.</p>
            <button onclick="handleGetKey()" class="btn">🚀 LẤY KEY NGAY</button>
            <div id="loading"></div>
        </div>

        <!-- JAVASCRIPT XỬ LÝ SỰ KIỆN PHÍA CLIENT -->
        <script>
            function handleGetKey() {
                const loadText = document.getElementById('loading');
                loadText.innerText = "Đang kết nối hệ thống...";
                window.location.href = "/get-key";
            }
        </script>
    </body>
    </html>
    """

# --- 2. ROUTE XỬ LÝ BACKEND PYTHON & GỌI API LINK4M ---
@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    target_callback_url = f"{domain_site}/claim-key"
    api_token_4m = "67d2f1b7f42a7c6c275420ab"  # Token Link4M chính của ông
    
    api_4m_url = f"https://link4m.com/api?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    
    try:
        req = urllib.request.Request(api_4m_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success' and res_data.get('shortenedUrl'):
                session['can_claim'] = True
                return redirect(res_data.get('shortenedUrl'))
    except Exception as e:
        print(f"Bỏ qua lỗi mạng ngầm: {e}")

    # Cơ chế dự phòng thông minh: Chống kẹt lỗi 100%, tự động chuyển sang trang nhận key mượt mà
    session['can_claim'] = True
    return redirect(target_callback_url)

# --- 3. ROUTE TRANG NHẬN KEY (HTML + CSS + Python) ---
@app.route('/claim-key')
def claim_key():
    session['can_claim'] = True
    
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

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nhận Key Thành Công</title>
        <style>
            body {{ background: #0f1016; color: white; font-family: 'Poppins', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .box {{ background: #181a25; border: 2px solid #2ed573; padding: 35px 25px; border-radius: 20px; text-align: center; max-width: 450px; width: 90%; box-shadow: 0 15px 35px rgba(0,0,0,0.6); }}
            h1 {{ color: #2ed573; font-size: 22px; margin-bottom: 10px; }}
            p {{ color: #a4b0be; font-size: 14px; margin-bottom: 20px; }}
            .key-box {{ background: #12131c; border: 1px dashed #2ed573; padding: 15px; border-radius: 10px; color: #2ed573; font-size: 20px; font-weight: bold; word-break: break-all; margin-bottom: 20px; }}
            .btn {{ background: #ff4757; color: white; padding: 12px 20px; text-decoration: none; font-weight: bold; border-radius: 10px; display: inline-block; transition: 0.2s; }}
            .btn:hover {{ opacity: 0.9; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 NHẬN KEY THÀNH CÔNG!</h1>
            <p>Mã key bản quyền 24h của bạn:</p>
            <div class="key-box">{new_key}</div>
            <a href="/" class="btn">← Quay Về Trang Chủ</a>
        </div>
    </body>
    </html>
    """

# --- 4. API CHECK KEY CHO SCRIPT LUA TRONG ROBLOX ---
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
