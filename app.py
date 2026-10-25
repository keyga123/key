from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template_string, request, session, url_for
import requests
import random
import string

app = Flask(__name__)
app.secret_key = 'cloud_gmail_api_secret_v2'

# --- DATABASE TÀI KHOẢN ---
users_db = {
    'admin': {
        'password': '123',
        'role': 'admin',
        'balance': 999999,
        'is_vip': True,
        'vip_expiry': datetime.now().timestamp() + (365 * 86400)
    },
    'player1': {
        'password': '123',
        'role': 'user',
        'balance': 50000,
        'is_vip': False,
        'vip_expiry': 0
    }
}

# Lưu danh sách email thực tế do user tạo (liên kết với Cloud 1SecMail)
cloud_inboxes = []

BASE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Gmail Ảo - Nhận OTP Thật</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f1016;
            --card-bg: #181a25;
            --border-color: #2a2d3d;
            --primary: #ff4757;
            --primary-hover: #ff6b81;
            --accent: #ffa502;
            --success: #2ed573;
            --text-main: #ffffff;
            --text-secondary: #a4b0be;
        }

        body.theme-red { --primary: #ff4757; --primary-hover: #ff6b81; --accent: #ffa502; }
        body.theme-green { --primary: #2ed573; --primary-hover: #26af5f; --accent: #00d2d3; }
        body.theme-blue { --primary: #1e90ff; --primary-hover: #3742fa; --accent: #ff6b81; }
        body.theme-purple { --primary: #9b59b6; --primary-hover: #8e44ad; --accent: #f1c40f; }

        @keyframes rgb-border {
            0% { border-color: #ff0000; box-shadow: 0 0 10px rgba(255,0,0,0.4); }
            50% { border-color: #00ff00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
            100% { border-color: #0000ff; box-shadow: 0 0 10px rgba(0,0,255,0.4); }
        }

        body.theme-rgb .rgb-box { border: 2px solid #ff0000 !important; animation: rgb-border 6s infinite; }
        body.theme-rgb .rgb-btn { background: linear-gradient(45deg, #ff0000, #ff7300, #48ff00, #00ffd5, #002bff, #ff00c8) !important; color: white !important; }
        body:not(.theme-rgb) .rgb-box { border: 2px solid var(--primary) !important; }
        body:not(.theme-rgb) .rgb-btn { background: var(--primary) !important; color: white !important; }
        body:not(.theme-rgb) .rgb-btn:hover { background: var(--primary-hover) !important; }

        body { background-color: var(--bg-color); color: var(--text-main); font-family: 'Poppins', sans-serif; margin: 0; padding: 0; }
        header { background: rgba(24, 26, 37, 0.95); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); flex-wrap: wrap; gap: 10px; }
        .logo { font-size: 20px; font-weight: 700; color: var(--primary); text-decoration: none; }
        .container { padding: 30px 20px; max-width: 900px; margin: auto; }
        .card { background: var(--card-bg); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
        .btn { border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; text-align: center; display: inline-block; text-decoration: none; transition: 0.2s; }
        input, select { width: 100%; padding: 12px; margin: 10px 0; background: #12131c; border: 1px solid var(--border-color); color: white; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        .alert { background: rgba(255,71,87,0.15); border: 1px solid var(--primary); color: #ff6b81; padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center; font-weight: 500; }
        .email-box { background: #12131c; border: 2px dashed var(--primary); padding: 15px; border-radius: 8px; text-align: center; font-size: 18px; font-weight: bold; color: var(--success); margin: 15px 0; word-break: break-all; }
    </style>
</head>
<body id="bodyTag" class="theme-rgb">
    <header>
        <a href="/" class="logo">⚡ CLOUD GMAIL & OTP THẬT</a>
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <select id="themeSelect" onchange="changeTheme(this.value)" style="width: auto; padding: 6px 10px; background: #181a25; color: white; border-radius: 6px; margin: 0;">
                <option value="theme-rgb">🌈 RGB 7 Màu</option>
                <option value="theme-red">🔴 Đỏ Gaming</option>
                <option value="theme-green">🟢 Xanh Lá</option>
                <option value="theme-blue">🔵 Xanh Dương</option>
                <option value="theme-purple">🟣 Tím Neon</option>
            </select>
            {% if 'username' in session %}
                {% set u = users_db[session['username']] %}
                <span style="background: rgba(46,213,115,0.15); border: 1px solid var(--success); color: var(--success); padding: 6px 12px; border-radius: 6px; font-size: 13px;">{{ session['username'] }} ({{ "Admin" if u['role']=='admin' else ("VIP" if u['is_vip'] else "Thường") }})</span>
                {% if u['role'] == 'admin' %}
                    <a href="/admin" class="btn rgb-btn" style="padding: 6px 12px; font-size: 13px;">⚙️ Admin</a>
                {% elif not u['is_vip'] %}
                    <a href="/upgrade-vip" class="btn rgb-btn" style="padding: 6px 12px; font-size: 13px; background: var(--accent) !important;">👑 Lên VIP (20k)</a>
                {% endif %}
                <a href="/logout" class="btn" style="background: #747d8c; color: white; padding: 6px 12px; font-size: 13px;">Thoát</a>
            {% else %}
                <a href="/login" class="btn rgb-btn" style="padding: 6px 12px; font-size: 13px;">Đăng nhập</a>
                <a href="/register" class="btn" style="background: #334155; color: white; padding: 6px 12px; font-size: 13px;">Đăng ký</a>
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
    <script>
        function changeTheme(themeName) {
            document.getElementById('bodyTag').className = themeName;
            localStorage.setItem('mail_theme', themeName);
        }
        window.onload = function() {
            let savedTheme = localStorage.getItem('mail_theme');
            if(savedTheme) {
                document.getElementById('bodyTag').className = savedTheme;
                document.getElementById('themeSelect').value = savedTheme;
            }
        }
    </script>
</body>
</html>
"""

def fetch_cloud_messages(email_addr):
  try:
    parts = email_addr.split('@')
    if len(parts) != 2: return []
    login, domain = parts[0], parts[1]
    url = f"https://www.1secmail.com/api/1v1/?action=getMessages&login={login}&domain={domain}"
    res = requests.get(url, timeout=5)
    if res.status_code == 200:
      msgs = res.json()
      formatted_msgs = []
      for m in msgs:
        # Lấy nội dung chi tiết từng thư
        msg_id = m.get('id')
        detail_url = f"https://www.1secmail.com/api/1v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
        detail_res = requests.get(detail_url, timeout=5)
        body_text = "Không đọc được nội dung"
        if detail_res.status_code == 200:
          body_text = detail_res.json().get('textBody', detail_res.json().get('body', ''))
        
        formatted_msgs.append({
            'sender': m.get('from'),
            'subject': m.get('subject'),
            'snippet': body_text[:150] + '...',
            'time': m.get('date')
        })
      return formatted_msgs
  except Exception as e:
    print(f"Lỗi lấy thư cloud: {e}")
  return []

@app.route('/')
def index():
  user_info = None
  my_emails = []
  if 'username' in session:
    uname = session['username']
    user_info = users_db.get(uname)
    my_emails = [b for b in cloud_inboxes if b['owner'] == uname or user_info['role'] == 'admin']
  else:
    if 'guest_email' not in session:
      # Lấy mail thật ngẫu nhiên từ cloud 1secmail
      try:
        res = requests.get("https://www.1secmail.com/api/1v1/?action=genRandomMailbox&count=1", timeout=5)
        if res.status_code == 200 and res.json():
          g_email = res.json()[0]
        else:
          rand_str = ''.join(random.choices(string.ascii_lowercase, k=8))
          g_email = f"{rand_str}@1secmail.com"
      except:
        g_email = f"guest_test@1secmail.com"
      
      session['guest_email'] = g_email
      cloud_inboxes.append({
          'email': g_email,
          'owner': 'guest',
          'is_permanent': False,
          'created_at': datetime.now().timestamp()
      })
    
    g_email = session['guest_email']
    my_emails = [b for b in cloud_inboxes if b['email'] == g_email]

  emails_render = ''
  for box in my_emails:
    # Lấy tin nhắn thực tế từ cloud api
    live_messages = fetch_cloud_messages(box['email'])
    
    remaining_time = "Vĩnh viễn (VIP/Admin)" if box['is_permanent'] else "10 phút (Khách)"
    status_color = "var(--success)" if box['is_permanent'] else "var(--accent)"
    
    msgs_html = ''
    if not live_messages:
      msgs_html = '<p style="color: var(--text-secondary); font-size: 13px; margin: 5px 0;">Đang chờ tin nhắn / mã OTP từ bên ngoài gửi đến...</p>'
    else:
      for m in live_messages:
        msgs_html += f'<div style="background: #12131c; padding: 10px; border-radius: 6px; margin-top: 8px; border: 1px solid var(--border-color); font-size: 13px;"><p style="margin: 0 0 4px 0; color: var(--accent);"><b>Từ:</b> {m["sender"]} <span style="float: right; color: var(--text-secondary);">{m["time"]}</span></p><p style="margin: 0 0 4px 0; color: white;"><b>Tiêu đề:</b> {m["subject"]}</p><p style="margin: 0; color: var(--text-secondary);"><b>Nội dung:</b> {m["snippet"]}</p></div>'

    emails_render += f'<div class="card rgb-box"><div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;"><div><h3 style="margin: 0; color: var(--success);">📧 {box["email"]}</h3><small style="color: {status_color};">Loại: <b>{remaining_time}</b> | Chủ sở hữu: {box["owner"]}</small></div><div style="display: flex; gap: 8px;"><button onclick="location.reload();" class="btn" style="background: #1e293b; color: var(--success); padding: 6px 12px; font-size: 12px; border: 1px solid var(--success);">🔄 Làm Mới</button><button onclick="navigator.clipboard.writeText(\'{box["email"]}\'); alert(\'Đã copy email!\');" class="btn rgb-btn" style="padding: 6px 12px; font-size: 12px;">📋 Copy</button></div></div><div style="margin-top: 12px;">{msgs_html}</div></div>'

  create_section = ''
  if 'username' in session and (user_info['is_vip'] or user_info['role'] == 'admin'):
    # Lấy danh sách domain thật từ 1secmail để user tạo tùy chỉnh
    try:
      domains_res = requests.get("https://www.1secmail.com/api/1v1/?action=getDomainList", timeout=5)
      domains = domains_res.json() if domains_res.status_code == 200 else ['1secmail.com', '1secmail.org', 'wwjmp.com']
    except:
      domains = ['1secmail.com', '1secmail.org']
    
    domain_options = ''.join([f'<option value="{d}">@{d}</option>' for d in domains])

    create_section = f'''
        <div class="card rgb-box">
            <h3 style="margin-top:0; color: var(--primary);">👑 Tạo Cloud Gmail Vĩnh Viễn Tùy Chỉnh</h3>
            <form action="/tao-email-vinh-vien" method="POST">
                <label style="font-size: 13px; color: var(--text-secondary);">Nhập tên email muốn tạo:</label>
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    <input type="text" name="custom_name" placeholder="VD: shopacc, myname..." required style="flex: 2; min-width: 150px;">
                    <select name="custom_domain" style="flex: 1; min-width: 130px; margin: 0;">
                        {domain_options}
                    </select>
                </div>
                <button type="submit" class="btn rgb-btn" style="margin-top: 12px;">TẠO CLOUD GMAIL VĨNH VIỄN</button>
            </form>
        </div>
        '''
  elif 'username' in session:
    create_section = '<div class="card rgb-box" style="text-align: center;"><p style="margin:0;">Bạn đang dùng tài khoản Thường. Muốn tạo Gmail vĩnh viễn và tùy chỉnh tên, hãy <a href="/upgrade-vip" style="color: var(--accent); font-weight: bold;">Nâng cấp VIP (20k/tháng)</a>!</p></div>'
  else:
    create_section = '<div class="card rgb-box" style="text-align: center;"><p style="margin:0;">Bạn đang dùng hộp thư <b>10 phút miễn phí</b>. <a href="/login" style="color: var(--primary); font-weight: bold;">Đăng nhập</a> để mở khóa tính năng VIP vĩnh viễn!</p></div>'

  content = f'''
    <div style="text-align: center; margin-bottom: 25px;">
        <h2 class="rgb-text" style="margin-bottom: 5px;">HỆ THỐNG CLOUD GMAIL THÔNG MINH</h2>
        <p style="color: var(--text-secondary); font-size: 13px;">Nhận mã OTP thực tế từ các trang web bên ngoài!</p>
    </div>
    {create_section}
    <div style="margin: 20px 0 10px 0;">
        <h3 style="margin: 0;">📥 Hộp Thư Đang Hoạt Động</h3>
    </div>
    {emails_render}
    '''
  return render_template_string(BASE_HTML, content=content, users_db=users_db)


@app.route('/tao-email-vinh-vien', methods=['POST'])
def tao_email_vinh-vien():
  if 'username' not in session: return redirect(url_for('login'))
  uname = session['username']
  user = users_db[uname]
  
  if not user['is_vip'] and user['role'] != 'admin':
    flash('Bạn cần lên VIP để tạo Cloud Gmail vĩnh viễn!')
    return redirect(url_for('index'))

  custom_name = request.form.get('custom_name', '').strip().lower()
  custom_domain = request.form.get('custom_domain', '1secmail.com').strip()
  clean_name = "".join([c for c in custom_name if c.isalnum() or c in '_-'])
  
  if not clean_name:
    flash('Tên email không hợp lệ!')
    return redirect(url_for('index'))

  email_addr = f"{clean_name}@{custom_domain}"
  
  exists = next((b for b in cloud_inboxes if b['email'] == email_addr), None)
  if exists:
    flash('Địa chỉ email này đã tồn tại trên hệ thống cloud!')
  else:
    cloud_inboxes.append({
        'email': email_addr,
        'owner': uname,
        'is_permanent': True,
        'created_at': datetime.now().timestamp()
    })
    flash(f'Tạo thành công Cloud Gmail: {email_addr}')

  return redirect(url_for('index'))


@app.route('/upgrade-vip')
def upgrade_vip():
  if 'username' not in session: return redirect(url_for('login'))
  uname = session['username']
  user = users_db[uname]
  if user['is_vip']:
    flash('Bạn đã là VIP rồi!')
    return redirect(url_for('index'))
  if user['balance'] < 20000:
    flash('Số dư không đủ 20.000đ để nâng cấp VIP!')
    return redirect(url_for('index'))

  user['balance'] -= 20000
  user['is_vip'] = True
  flash('🎉 Nâng cấp VIP thành công! Bạn được quyền tạo Cloud Gmail vĩnh viễn.')
  return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    u = request.form['username']
    p = request.form['password']
    if u in users_db and users_db[u]['password'] == p:
      session['username'] = u
      flash('Đăng nhập thành công!')
      return redirect(url_for('index'))
    flash('Sai tài khoản hoặc mật khẩu!')
  content = '<div class="card rgb-box" style="max-width: 400px; margin: auto;"><h2 class="rgb-text" style="text-align: center;">ĐĂNG NHẬP</h2><form method="POST"><input type="text" name="username" placeholder="Tài khoản..." required><input type="password" name="password" placeholder="Mật khẩu..." required><button type="submit" class="btn rgb-btn" style="margin-top: 15px;">ĐĂNG NHẬP</button></form><div style="text-align: center; margin-top: 15px;"><a href="/" style="color: var(--text-secondary); font-size: 13px; text-decoration: none;">← Quay về</a></div></div>'
  return render_template_string(BASE_HTML, content=content, users_db=users_db)


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    u = request.form['username'].strip()
    p = request.form['password'].strip()
    if not u or not p: flash('Điền đầy đủ thông tin!')
    elif u in users_db: flash('Tài khoản đã tồn tại!')
    else:
      users_db[u] = {'password': p, 'role': 'user', 'balance': 50000, 'is_vip': False, 'vip_expiry': 0}
      flash('Đăng ký thành công! Đã tặng sẵn 50k test.')
      return redirect(url_for('login'))
  content = '<div class="card rgb-box" style="max-width: 400px; margin: auto;"><h2 class="rgb-text" style="text-align: center;">ĐĂNG KÝ</h2><form method="POST"><input type="text" name="username" placeholder="Tài khoản mới..." required><input type="password" name="password" placeholder="Mật khẩu..." required><button type="submit" class="btn rgb-btn" style="margin-top: 15px;">ĐĂNG KÝ</button></form><div style="text-align: center; margin-top: 15px;"><a href="/" style="color: var(--text-secondary); font-size: 13px; text-decoration: none;">← Quay về</a></div></div>'
  return render_template_string(BASE_HTML, content=content, users_db=users_db)


@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


@app.route('/admin')
def admin():
  if 'username' not in session or users_db[session['username']]['role'] != 'admin':
    flash('Không có quyền truy cập!')
    return redirect(url_for('index'))

  emails_table = ''
  for b in cloud_inboxes:
    emails_table += f'<div style="background: #12131c; padding: 10px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; border: 1px solid var(--border-color);"><p style="margin:0;"><b>Email:</b> <span style="color: var(--success);">{b["email"]}</span> | <b>Chủ sở hữu:</b> {b["owner"]} | <b>Loại:</b> {"Vĩnh viễn" if b["is_permanent"] else "10 phút"}</p></div>'

  content = f'''
    <div class="card rgb-box" style="border: 1px solid var(--primary);">
        <h2 class="rgb-text" style="margin-top:0;">⚙️ TRANG QUẢN TRỊ ADMIN</h2>
        <h3 style="color: var(--accent);">Tất Cả Cloud Email Đang Hoạt Động ({len(cloud_inboxes)})</h3>
        {emails_table if emails_table else "<p>Chưa có hộp thư nào.</p>"}
        <div style="margin-top: 20px;"><a href="/" class="btn rgb-btn">← Quay về trang chủ</a></div>
    </div>
    '''
  return render_template_string(BASE_HTML, content=content, users_db=users_db)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
