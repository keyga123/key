@app.route('/get-key')
def get_key():
    domain_site = "https://gagaming-key-system.onrender.com"
    api_token_4m = "67d2f114875f8e29865d1fa9"
    
    target_callback_url = f"{domain_site}/claim-key"
    api_4m_url = f"https://link4m.com/api?api={api_token_4m}&url={urllib.parse.quote(target_callback_url)}"
    
    try:
        req = urllib.request.Request(api_4m_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'success' or res_data.get('shortenedUrl'):
                short_url = res_data.get('shortenedUrl') or res_data.get('url')
                return redirect(short_url)
            else:
                # Nếu API 4M trả về lỗi, hiện thông báo chứ ko cho nhận key gian lận
                content = f"""
                <div class="card rgb-box" style="text-align: center;">
                    <h2 class="rgb-text" style="color: var(--primary);">⚠️ LỖI TẠO LINK VƯỢT</h2>
                    <p style="color: var(--text-secondary);">Không thể kết nối tới hệ thống Link4M. Phản hồi từ API: {res_data}</p>
                    <a href="/" class="btn rgb-btn" style="max-width: 250px; margin-top: 20px;">← Quay Về Trang Chủ</a>
                </div>
                """
                return render_template_string(BASE_HTML, content=content)
    except Exception as e:
        content = f"""
        <div class="card rgb-box" style="text-align: center;">
            <h2 class="rgb-text" style="color: var(--primary);">⚠️ LỖI KẾT NỐI HỆ THỐNG</h2>
            <p style="color: var(--text-secondary);">Không thể tạo link vượt do lỗi mạng: {e}</p>
            <a href="/" class="btn rgb-btn" style="max-width: 250px; margin-top: 20px;">← Quay Về Trang Chủ</a>
        </div>
        """
        return render_template_string(BASE_HTML, content=content)
