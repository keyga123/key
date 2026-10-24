from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, request, session, url_for
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)
app.secret_key = 'key_system_secure_v1'

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
    <html>
    <head>
        <meta charset="UTF-8">
        <title>GA Gaming Key System</title>
        <style>
            body { background: #0f1016; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }
            .btn { background: linear-gradient(45deg, #ff0000, #ff7300, #00ffd5); padding: 15px 30px; color: white; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>🔑 HỆ THỐNG KEY GÀ GAMING</h1>
        <p>Bấm vào nút bên dưới để vượt link lấy key bản quyền 24h.</p>
        <a href="/get-key" class="btn">LẤY KEY QUA VƯỢT LINK 4M</a>
    </body>
    </html>
    """

@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    api_token_4m = "67d2f114875f8e29865d1fa9"
    
    # Tạo mã phiên bảo mật độc nhất
    sec_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    session['bypass_token'] = sec_token
    
    # Link callback buộc phải kèm theo mã token bảo mật
    target_callback_url = f"{domain_site}/claim-key?t={sec_token}"
    api_4m_url = f"https://link4m.com/api?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    
    try:
        req = urllib.request.Request(api_4m_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success':
                short_url = res_data.get('shortenedUrl') or res_data.get('url')
                return redirect(short_url)
    except Exception as e:
        print(f"Lỗi tạo link 4M: {e}")

    # Nếu API Link4M lỗi, báo lỗi trực tiếp, TUYỆT ĐỐI KHÔNG cấp key lậu
    return """
    <html>
    <head><meta charset="UTF-8"><title>Lỗi</title></head>
    <body style="background:#0f1016; color:white; text-align:center; padding-top:50px; font-family:sans-serif;">
        <h2 style="color:#ff4757;">⚠️ HỆ THỐNG VƯỢT LINK ĐANG BẬN</h2>
        <p>Không thể khởi tạo link từ Link4M. Vui lòng quay lại thử lại sau ít phút!</p>
        <a href="/" style="color:#00ffd5; text-decoration:none; font-weight:bold;">← Quay Về Trang Chủ</a>
    </body>
    </html>
    """

@app.route('/claim-key')
def claim_key():
    client_token = request.args.get('t')
    server_token = session.get('bypass_token')
    
    # BẢO MẬT: Nếu không có token hoặc token không khớp -> Chặn thẳng tay, không cho nhận key!
    if not client_token or not server_token or client_token != server_token:
        return """
        <html>
        <head><meta charset="UTF-8"><title>Cảnh Báo</title></head>
        <body style="background:#0f1016; color:white; text-align:center; padding-top:50px; font-family:sans-serif;">
            <h2 style="color:#ff4757;">🚫 CẢNH BÁO: BẠN CHƯA VƯỢT LINK!</h2>
            <p>Hệ thống phát hiện bạn truy cập trái phép mà không hoàn thành vượt link 4M.</p>
            <a href="/" style="color:#00ffd5; text-decoration:none; font-weight:bold;">← Quay Lại Vượt Link Ngay</a>
        </body>
        </html>
        """
    
    # Xóa token sau khi đã cấp key thành công để chống spam dùng lại link cũ
    session.pop('bypass_token', None)
    
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
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Claim Key</title>
        <style>
            body {{ background: #0f1016; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }}
            .key-box {{ background: #181a25; border: 2px solid #ff0000; padding: 20px; display: inline-block; border-radius: 10px; color: #2ed573; font-size: 24px; font-weight: bold; margin: 20px 0; }}
            .btn {{ background: #ff4757; padding: 10px 20px; color: white; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <h1 style="color: #2ed573;">🎉 VƯỢT LINK THÀNH CÔNG!</h1>
        <p>Key bản quyền 24h của bạn:</p>
        <div class="key-box">{new_key}</div><br>
        <a href="/" class="btn">← Quay Về Trang Chủ</a>
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
