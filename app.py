from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

# Database lưu trữ Key và HWID
keys_db = {}

TOKEN_LINK4M = "67d2f1b7f42a7c6c275420ab"

# --- TRANG CHỦ RENDER: NHẬN REQUEST TỪ BLOGGER VÀ GỌI API LINK4M SERVER-SIDE ---
@app.route('/')
def index():
    # URL đích sau khi người dùng vượt link xong sẽ quay về trang nhận key
    target_url = "https://gagaming-key-system.onrender.com/claim-key"
    
    # Endpoint API chính thức chuẩn của Link4M
    api_url = f"https://link4m.com/api?api={TOKEN_LINK4M}&url={urllib.parse.quote(target_url)}"

    try:
        # Python gọi ngầm sang Link4M (Né hoàn toàn CORS và lỗi trình duyệt)
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            
            # Lấy link rút gọn chuẩn từ JSON trả về của Link4M
            short_url = res_data.get('shortenedUrl') or res_data.get('url')
            if res_data.get('status') == 'success' and short_url:
                return redirect(short_url)
    except Exception as e:
        print(f"Lỗi gọi API Link4M: {e}")

    # Fallback dự phòng: Nếu gọi API lỗi thì trỏ thẳng về trang nhận key để không bị kẹt
    return redirect('/claim-key')

# --- TRANG NHẬN KEY VÀ SAO CHÉP 1 CHẠM ---
@app.route('/claim-key')
def claim_key():
    p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_key = f"GA-{p1}-{p2}"
    
    expiry_time = datetime.now().timestamp() + (24 * 3600)
    keys_db[new_key] = {
        "expiry": expiry_time,
        "hwid": None,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nhận Key Thành Công - GA Gaming</title>
        <style>
            body {{
                background-color: #0d0e15;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: #161822;
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
                color: #00ffcc;
                margin-bottom: 10px;
            }}
            p {{
                color: #8b9bb4;
                font-size: 14px;
                margin-bottom: 20px;
            }}
            .key-box {{
                background: #0d0e15;
                border: 1px dashed #00ffcc;
                padding: 15px;
                border-radius: 10px;
                color: #00ffcc;
                font-size: 20px;
                font-weight: bold;
                word-break: break-all;
                margin-bottom: 20px;
            }}
            .btn-copy {{
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
            }}
            .btn-copy:hover {{
                opacity: 0.9;
                transform: translateY(-2px);
            }}
            #toast {{
                font-size: 13px;
                color: #00ffcc;
                height: 15px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎉 VƯỢT LINK THÀNH CÔNG!</h1>
            <p>Mã key bản quyền 24h của bạn:</p>
            <div class="key-box" id="keyText">{new_key}</div>
            <button onclick="copyKey()" class="btn-copy">📋 SAO CHÉP KEY</button>
            <div id="toast"></div>
        </div>

        <script>
            function copyKey() {{
                const text = document.getElementById('keyText').innerText;
                navigator.clipboard.writeText(text).then(() => {{
                    document.getElementById('toast').innerText = "Đã sao chép key vào bộ nhớ tạm!";
                    setTimeout(() => {{ document.getElementById('toast').innerText = ""; }}, 3000);
                }}).catch(() => {{
                    alert("Không thể sao chép tự động, vui lòng copy thủ công!");
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html_content

# --- API XÁC THỰC KEY VÀ KHÓA THIẾT BỊ (HWID) CHO SCRIPT ROBLOX ---
@app.route('/api/check-key', methods=['POST'])
def api_check_key():
    data = request.json or request.form
    key = data.get('key', '').strip()
    hwid = data.get('hwid', '').strip()
    now_ts = datetime.now().timestamp()
    
    if not key or not hwid:
        return jsonify({'success': False, 'message': 'Thiếu tham số key hoặc HWID!'})
        
    key_info = keys_db.get(key)
    if not key_info:
        return jsonify({'success': False, 'message': 'Key không tồn tại!'})
        
    if now_ts > key_info['expiry']:
        return jsonify({'success': False, 'message': 'Key đã hết hạn sử dụng!'})
        
    if key_info['hwid'] is None:
        key_info['hwid'] = hwid
    elif key_info['hwid'] != hwid:
        return jsonify({'success': False, 'message': 'Key này đã được sử dụng trên thiết bị khác!'})
        
    return jsonify({
        'success': True, 
        'message': 'Key hợp lệ và khớp thiết bị!', 
        'expires_at': datetime.fromtimestamp(key_info['expiry']).strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
