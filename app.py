from flask import Flask, redirect, request
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GA Gaming Key System</title>
        <style>
            body { background: #0f1016; color: white; font-family: sans-serif; text-align: center; padding-top: 100px; margin: 0; }
            .btn { background: linear-gradient(45deg, #ff0000, #00ffd5); padding: 15px 30px; color: white; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; }
        </style>
    </head>
    <body>
        <h1>🔑 HỆ THỐNG KEY GA GAMING</h1>
        <p>Bấm vào nút bên dưới để lấy key bản quyền 24h.</p><br>
        <a href="/get-key" class="btn">LẤY KEY QUA LINK4M</a>
    </body>
    </html>
    """

@app.route('/get-key')
def get_key():
    target_url = "https://gagaming-key-system.onrender.com/claim-key"
    token = "67d2f1b7f42a7c6c275420ab"  # Token Link4M của ông
    
    # Quay lại gọi đúng chuẩn API JSON của Link4M
    api_url = f"https://link4m.com/api?api={token}&url={urllib.parse.quote(target_url)}"
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            # Nếu API trả về link rút gọn thành công thì chuyển hướng sang đó
            if res_data.get('status') == 'success' and res_data.get('shortenedUrl'):
                return redirect(res_data.get('shortenedUrl'))
    except Exception as e:
        print(f"Lỗi gọi API: {e}")

    # Nếu có lỗi xảy ra, chuyển hướng trực tiếp về trang nhận key luôn để không bị kẹt
    return redirect(target_url)

@app.route('/claim-key')
def claim_key():
    p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_key = f"GA-{p1}-{p2}"
    
    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thành Công</title>
        <style>
            body {{ background: #0f1016; color: white; font-family: sans-serif; text-align: center; padding-top: 80px; margin: 0; }}
            .key {{ background: #181a25; border: 2px solid #2ed573; padding: 20px; display: inline-block; border-radius: 10px; color: #2ed573; font-size: 24px; font-weight: bold; margin: 20px 0; }}
            .btn {{ background: #ff4757; padding: 10px 20px; color: white; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <h1 style="color: #2ed573;">🎉 VƯỢT LINK THÀNH CÔNG!</h1>
        <p>Key bản quyền 24h của bạn:</p>
        <div class="key">{new_key}</div><br>
        <a href="/" class="btn">← Quay Về Trang Chủ</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
