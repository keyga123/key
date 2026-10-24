@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    api_token_4m = "67d2f114875f8e29865d1fa9"
    
    # Tạo URL callback chuyển hướng thẳng tới trang nhận key
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

    # Chuyển hướng thẳng sang link 4M vừa tạo
    return redirect(bypass_link)
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
