from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

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
        <title>GA Gaming - Ultimate Key System</title>
        <style>
            :root {
                --bg-color: #0b0c10;
                --card-bg: #1f2833;
                --primary: #66fcf1;
                --success: #45f3ff;
                --text-main: #ffffff;
                --text-sub: #c5c6c7;
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
                padding: 40px 30px;
                border-radius: 24px;
                text-align: center;
                max-width: 420px;
                width: 90%;
                box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            }
            h1 {
                font-size: 26px;
                background: linear-gradient(to right, #66fcf1, #45f3ff, #ff007f);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 12px;
            }
            p {
                color: var(--text-sub);
                font-size: 14px;
                margin-bottom: 30px;
            }
            .btn {
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
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(102, 252, 241, 0.6);
            }
            #loading {
                margin-top: 20px;
                color: #66fcf1;
                font-size: 13px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 GA GAMING VIP</h1>
            <p>Hệ thống tự động hóa vượt link Link4M cấp bản quyền 24h siêu tốc.</p>
            <button onclick="getLink4M()" class="btn">⚡ LẤY KEY NGAY LẬP TỨC</button>
            <div id="loading"></div>
        </div>

        <script>
            async function getLink4M() {
                const loadText = document.getElementById('loading');
                loadText.innerText = "⚡ Đang thiết lập kết nối tối ưu với Link4M...";
                
                const token = "67d2f1b7f42a7c6c275420ab";
                const targetUrl = encodeURIComponent("https://gagaming-key-system.onrender.com/claim-key");
                const apiUrl = `https://link4m.com/api?api=${token}&url=${targetUrl}`;

                try {
                    const response = await fetch(apiUrl);
                    const data = await response.json();
                    
                    if (data.status === 'success' && data.shortenedUrl) {
                        window.location.href = data.shortenedUrl;
                    } else {
                        window.location.href = `https://link4m.com/st?api=${token}&url=${targetUrl}`;
                    }
                } catch (err) {
                    window.location.href = `https://link4m.com/st?api=${token}&url=${targetUrl}`;
                }
            }
        </script>
    </body>
    </html>
    """

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

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nhận Key Thành Công</title>
        <style>
            body {{ background: #0b0c10; color: white; font-family: 'Poppins', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .box {{ background: #1f2833; border: 2px solid #66fcf1; padding: 40px 30px; border-radius: 24px; text-align: center; max-width: 450px; width: 90%; box-shadow: 0 20px 40px rgba(0,0,0,0.8); }}
            h1 {{ color: #66fcf1; font-size: 24px; margin-bottom: 12px; }}
            p {{ color: #c5c6c7; font-size: 14px; margin-bottom: 20px; }}
            .key-box {{ background: #0b0c10; border: 1px dashed #66fcf1; padding: 18px; border-radius: 12px; color: #66fcf1; font-size: 22px; font-weight: bold; word-break: break-all; margin-bottom: 25px; box-shadow: inset 0 0 10px rgba(102, 252, 241, 0.2); }}
            .btn {{ background: #ff007f; color: white; padding: 14px 22px; text-decoration: none; font-weight: bold; border-radius: 12px; display: inline-block; transition: 0.2s; box-shadow: 0 5px 15px rgba(255, 0, 127, 0.4); }}
            .btn:hover {{ opacity: 0.9; transform: translateY(-2px); }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎉 VƯỢT LINK THÀNH CÔNG!</h1>
            <p>Mã key bản quyền 24h tối thượng của bạn:</p>
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
