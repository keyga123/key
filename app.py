from datetime import datetime, timedelta
from flask import Flask, flash, jsonify, redirect, render_template_string, request, session, url_for
import random
import string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)
app.secret_key = 'key_system_secure_v1'

# Database giả lập lưu trữ Key
keys_db = {
    "GA-GAMING-VIP-2026": {
        "expiry": (datetime.now() + timedelta(days=30)).timestamp(),
        "ip": "all",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
}

ADMIN_USER = "admin"
ADMIN_PASS = "123"

BASE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Key Bản Quyền - GA Gaming</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f1016;
            --card-bg: #181a25;
            --border-color: #2a2d3d;
            --primary: #ff4757;
            --success: #2ed573;
            --text-main: #ffffff;
            --text-secondary: #a4b0be;
        }
        
        @keyframes rgb-rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }

        @keyframes rgb-border {
            0% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255,0,0,0.4); }
            50% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
            100% { border-color: #0000ff; box-shadow: 0 0 10px rgba(0,0,255,0.4); }
        }

        @keyframes rgb-anim {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .rgb-box {
            border: 2px solid #ff0000 !important;
            animation: rgb-border 6s infinite;
        }

        .rgb-btn {
            background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000) !important;
            background-size: 400% !important;
            animation: rgb-anim 8s linear infinite !important;
            color: white !important;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }

        .rgb-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.6) !important;
        }

        .rgb-text {
            background: linear-gradient(to right, #ff4757, #ffa502, #2ed573, #1e90ff, #70a1ff, #ff6b81);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rgb-rainbow 6s linear infinite;
            font-weight: 700;
        }

        body { background-color: var(--bg-color); color: var(--text-main); font-family: 'Poppins', sans-serif; margin: 0; padding: 0; }
        header { background: rgba(24, 26, 37, 0.95); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); }
        .container { padding: 40px 20px; max-width: 800px; margin: auto; }
        .card { background: var(--card-bg); border-radius: 14px; padding: 25px; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
        .btn { padding: 12px 20px; border-radius: 8px; display: inline-block; text-decoration: none; text-align: center; width: 100%; box-sizing: border-box; }
        input { width: 100%; padding: 12px 15px; margin: 10px 0; background: #12131c; border: 1px solid var(--border-color); color: white; border-radius: 8px; box-sizing: border-box; }
        .alert { background: rgba(255,71,87,0.15); border: 1px solid var(--primary); color: #ff6b81; padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center; }
    </style>
</head>
<body>
    <header>
        <a href="/" class="logo rgb-text" style="font-size: 20px; text-decoration: none;">🔑 GA GAMING KEY SYSTEM</a>
        <div>
            {% if session.get('admin') %}
                <a href="/admin" class="rgb-btn btn" style="padding: 8px 15px; font-size: 13px;">⚙️ Quản Trị</a>
                <a href="/logout" style="color: #a4b0be; text-decoration: none; margin-left: 15px; font-size: 13px;">Thoát</a>
            {% else %}
                <a href="/admin-login" class="rgb-btn btn" style="padding: 8px 15px; font-size: 13px;">Admin Login</a>
            {% endif %}
        </div>
    </header>
    <div class="container">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    content = f"""
    <div class="card rgb-box" style="text-align: center;">
        <h1 class="rgb-text">HỆ THỐNG CẤP KEY TỰ ĐỘNG</h1>
        <p style="color: var(--text-secondary);">Vượt link qua Link4M để nhận key bản quyền 24h sử dụng tool/script.</p>
        <div style="margin: 30px 0;">
            <a href="/get-key" class="btn rgb-btn" style="font-size: 18px; max-width: 300px;">LẤY KEY QUA VƯỢT LINK</a>
        </div>
        <p style="font-size: 12px; color: var(--text-secondary);">IP của bạn: <b style="color: #70a1ff;">{user_ip}</b></p>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    api_token_4m = "67d2f114875f8e29865d1fa9"
    
    # Tạo URL callback chuyển hướng trực tiếp tới trang nhận key
    target_callback_url = f"{domain_site}/claim-key"
    api_4m_url = f"https://link4m.com/api?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    
    bypass_link = target_callback_url
    try:
        req = urllib.request.Request(api_4m_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success':
                bypass_link = res_data.get('shortenedUrl', target_callback_url)
    except Exception as e:
        print(f"Lỗi tạo link 4M: {e}")

    # Chuyển hướng người dùng sang link 4M để vượt link
    return redirect(bypass_link)

@app.route('/claim-key')
def claim_key():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Sinh key mới 24h mỗi khi truy cập trang này
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_key = f"GA-{part1}-{part2}"
    
    expiry_time = datetime.now().timestamp() + (24 * 3600)
    keys_db[new_key] = {
        "expiry": expiry_time,
        "ip": user_ip,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    content = f"""
    <div class="card rgb-box" style="text-align: center;">
        <h2 class="rgb-text">🎉 VƯỢT LINK THÀNH CÔNG!</h2>
        <p style="color: var(--text-secondary);">Cảm ơn bạn đã hoàn thành vượt link. Đây là key bản quyền 24h của bạn:</p>
        <div style="background: #12131c; padding: 20px; border-radius: 10px; border: 1px solid var(--border-color); margin: 20px 0;">
            <code style="font-size: 22px; color: var(--success); font-weight: bold; word-break: break-all;">{new_key}</code>
        </div>
        <a href="/" class="btn rgb-btn" style="max-width: 250px;">← Quay Về Trang Chủ</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

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

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Sai tài khoản hoặc mật khẩu admin!')
    content = """
    <div class="card rgb-box" style="max-width: 400px; margin: auto;">
        <h2 class="rgb-text" style="text-align: center;">ĐĂNG NHẬP ADMIN</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Tài khoản..." required>
            <input type="password" name="password" placeholder="Mật khẩu..." required>
            <button type="submit" class="btn rgb-btn" style="margin-top: 15px;">ĐĂNG NHẬP</button>
        </form>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
        
    now_ts = datetime.now().timestamp()
    rows_html = ""
    for k, info in keys_db.items():
        status = '<span style="color: var(--success);">Đang hoạt động</span>' if info['expiry'] > now_ts else '<span style="color: var(--primary);">Hết hạn</span>'
        exp_date = datetime.fromtimestamp(info['expiry']).strftime('%d/%m/%Y %H:%M')
        rows_html += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding: 10px 0; font-size: 13px;">
            <div>
                <b>{k}</b><br>
                <small style="color: var(--text-secondary);">IP: {info['ip']} | Hết hạn: {exp_date}</small><br>
                {status}
            </div>
            <a href="/admin/delete-key/{k}" style="color: var(--primary); text-decoration: none; font-weight: bold;">[Xóa]</a>
        </div>
        """
        
    content = f"""
    <div class="card rgb-box">
        <h2 class="rgb-text">⚙️ QUẢN LÝ HỆ THỐNG KEY</h2>
        <div style="background: #12131c; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <form action="/admin/add-key" method="POST">
                <input type="text" name="custom_key" placeholder="Nhập key tùy chỉnh (hoặc để trống tự sinh)">
                <input type="number" name="days" placeholder="Số ngày sử dụng (VD: 1 hoặc 30)" required>
                <button type="submit" class="btn rgb-btn" style="margin-top: 10px;">TẠO / THÊM KEY THỦ CÔNG</button>
            </form>
        </div>
        <h3 style="color: var(--accent);">Danh Sách Key Hiện Tại ({len(keys_db)})</h3>
        <div style="max-height: 350px; overflow-y: auto;">
            {rows_html if rows_html else '<p>Chưa có key nào.</p>'}
        </div>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/admin/add-key', methods=['POST'])
def admin_add_key():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    custom_key = request.form.get('custom_key', '').strip()
    days = int(request.form.get('days', 1))
    
    if not custom_key:
        part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        custom_key = f"GA-{part1}-{part2}"
        
    expiry_time = datetime.now().timestamp() + (days * 86400)
    keys_db[custom_key] = {
        "expiry": expiry_time,
        "ip": "all",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    flash(f'Đã tạo key thành công: {custom_key}')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-key/<key_str>')
def admin_delete_key(key_str):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if key_str in keys_db:
        del keys_db[key_str]
        flash('Đã xóa key thành công!')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
