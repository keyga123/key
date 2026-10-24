from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, request
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)
app.secret_key = 'gagaming_ultimate_key_2026'

# Database lưu trữ Key
keys_db = {
    "GA-GAMING-VIP-2026": {
        "expiry": (datetime.now() + timedelta(days=30)).timestamp(),
        "ip": "all",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
}

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GA Gaming - Hệ Thống Key Bản Quyền</title>
        <style>
            :root {
                --bg: #0f1016;
                --card: #181a25;
                --border: #2a2d3d;
                --primary: #ff4757;
                --success: #2ed573;
            }
            body { background: var(--bg); color: white; font-family: 'Poppins', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .box { background: var(--card); border: 2px solid var(--primary); padding: 30px; border-radius: 16px; text-align: center; max-width: 400px; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { font-size: 22px; background: linear-gradient(to right, #ff4757, #ffa502, #2ed573, #1e90ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
            p { color: #a4b0be; font-size: 14px; margin-bottom: 25px; }
            .btn { background: linear-gradient(45deg, #ff0000, #ff7300, #00ffd5); color: white; padding: 14px 20px; text-decoration: none; font-weight: bold; border-radius: 10px; display: block; width: 100%; box-sizing: border-box; transition: 0.3s; }
            .btn:hover { transform: translateY(-2px); opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🔑 GA GAMING KEY SYSTEM</h1>
            <p>Hệ thống cấp key bản quyền 24h tự động qua Link4M.</p>
            <a href="/get-key" class="btn">🚀 LẤY KEY NGAY BÂY GIỜ</a>
        </div>
    </body>
    </html>
    """

@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    target_callback_url = f"{domain_site}/claim-key"
    
    # Đã đổi sang API Token thứ hai của ông ở đây:
    api_token_4m = "67d2f1b7f42a7c6c275420ab[span_1](start_span)"[span_1](end_span)
    
    api_4m_url = f"https://link4m.com/api?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    
    try:
        req = urllib.request.Request(api_4m_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success' and res_data.get('shortenedUrl'):
                return redirect(res_data.get('shortenedUrl'))
    except Exception as e:
        print(f"Lỗi API Link4M: {e}")

    # Fallback mượt mà chuyển hướng trực tiếp nếu server Render bị giới hạn request ngầm
    fallback_link = f"https://link4m.com/st?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    return redirect(fallback_link)

@app.route('/claim-key')
def claim_key():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_key = f"GA-{part1}-{part2}"
    
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
            .box {{ background: #181a25; border: 2px solid #2ed573; padding: 30px; border-radius: 16px; text-align: center; max-width: 450px; width: 90%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            h1 {{ color: var(--success); font-size: 20px; margin-bottom: 10px; }}
            p {{ color: #a4b0be; font-size: 14px; margin-bottom: 20px; }}
            .key-box {{ background: #12131c; border: 1px dashed #2ed573; padding: 15px; border-radius: 8px; color: #2ed573; font-size: 20px; font-weight: bold; word-break: break-all; margin-bottom: 20px; }}
            .btn {{ background: #ff4757; color: white; padding: 12px 20px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 VƯỢT LINK THÀNH CÔNG!</h1>
            <p>Đây là mã key bản quyền 24h của bạn:</p>
            <div class="key-box">{new_key}</div>
            <a href="/" class="btn">← Quay Về Trang Chủ</a>
        </div>
    </body>
    </html>
    """

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
