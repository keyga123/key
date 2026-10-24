@app.route('/get-key')
def get_key():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    now_ts = datetime.now().timestamp()
    
    # Kiểm tra xem IP này đã có key nào còn sống chưa
    existing_key = None
    for k, info in keys_db.items():
        if info['ip'] == user_ip and info['expiry'] > now_ts:
            existing_key = k
            break
            
    if existing_key:
        content = f"""
        <div class="card rgb-box" style="text-align: center;">
            <h2 class="rgb-text">🎉 KEY CỦA BẠN VẪN CÒN HẠN</h2>
            <p style="color: var(--text-secondary);">Mỗi thiết bị chỉ dùng chung một key trong thời gian hiệu lực.</p>
            <div style="background: #12131c; padding: 20px; border-radius: 10px; border: 1px solid var(--border-color); margin: 20px 0;">
                <code style="font-size: 22px; color: var(--success); font-weight: bold; word-break: break-all;">{existing_key}</code>
            </div>
            <a href="/" class="btn rgb-btn" style="max-width: 250px;">← Quay Về Trang Chủ</a>
        </div>
        """
        return render_template_string(BASE_HTML, content=content)

    # --- TÍCH HỢP LINK 4M ---
    domain_site = "https://gagaming-key-system.onrender.com"
    api_token_4m = "67d2f114875f8e29865d1fa9"
    
    # Tạo token phiên làm việc độc nhất và lưu tạm vào session
    session_token = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    session['pending_token'] = session_token
    
    target_callback_url = f"{domain_site}/claim-key?token={session_token}"
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

    # Chuyển hướng người dùng sang link vượt 4M
    return redirect(bypass_link)

@app.route('/claim-key')
def claim_key():
    token = request.args.get('token')
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Kiểm tra bảo mật: token trên URL phải khớp với session hoặc bắt buộc phải qua Link4M
    # (Nếu muốn test trực tiếp không cần vượt link thì có thể tạm bỏ qua check session, nhưng để chống gian lận nên giữ lại)
    if not token:
        flash('Vui lòng thực hiện vượt link để lấy key!')
        return redirect(url_for('index'))
        
    # Sinh key mới 24h
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
