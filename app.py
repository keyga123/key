from flask import Flask, render_template_string, request, send_file, redirect, url_for, flash
import os
import base64
import urllib.parse

app = Flask(__name__)
app.secret_key = 'ga_gaming_toolkit_secret_key_v9999'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- HỆ THỐNG MÃ HÓA LUA V9999 PRO ---
def lua_v9999_obfuscator(lua_code):
    try:
        # Mã hóa byte string chuẩn chống decompile cho Lua
        encoded_bytes = lua_code.encode('utf-8')
        char_list = ",".join([str(b) for b in encoded_bytes])
        
        obfuscated_script = f"""--[[
    ========================================
       GA GAMING - LUA V9999 OBFUSCATOR PRO
       Protected by Advanced String Encoder
    ========================================
--]]
local _s = string.char({char_list})
local _f, _e = load(_s)
if _f then
    return _f()
else
    error("GA GAMING Runtime Error: " .. tostring(_e))
end
"""
        return obfuscated_script
    except Exception as e:
        return f"-- Lỗi mã hóa Lua: {str(e)}\n" + lua_code

# --- HỆ THỐNG MÃ HÓA PYTHON V9999 ---
def python_v9999_obfuscator(py_code):
    try:
        encoded_bytes = base64.b64encode(py_code.encode('utf-8')).decode('utf-8')
        obfuscated_script = f'''# -*- coding: utf-8 -*-
# GA GAMING - PYTHON V9999 OBFUSCATOR
import base64
_code_enc = "{encoded_bytes}"
exec(base64.b64decode(_code_enc).decode('utf-8'))
'''
        return obfuscated_script
    except Exception as e:
        return py_code

# --- GIAO DIỆN WEB TOOLKIT ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GA GAMING - Toolkit Upload & Download File</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; font-family: 'Poppins', sans-serif; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 700px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h2 { color: #ff4757; font-size: 20px; margin-bottom: 20px; text-align: center; }
        .section { margin-bottom: 25px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        .section label { display: block; font-weight: 600; margin-bottom: 8px; font-size: 14px; }
        input[type="text"], input[type="file"] { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 13px; }
        .btn { background: #3b82f6; color: white; border: none; padding: 10px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 13px; transition: 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn-lua { background: #8b5cf6; }
        .btn-py { background: #f97316; }
        .alert { background: #fee2e2; color: #991b1b; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 13px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 GA GAMING - Toolkit Upload & Download File 🔥</h2>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="alert">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <!-- 1. Bóc Tách & Giải Mã Link -->
        <div class="section">
            <label>1. Bóc Tách & Giải Mã Link</label>
            <form action="/boctach" method="POST">
                <input type="text" name="target_link" placeholder="Nhập link cần bóc tách..." required>
                <button type="submit" class="btn">Bóc Tách Link</button>
            </form>
        </div>

        <!-- 2. Lua V9999 Obfuscator -->
        <div class="section">
            <label>2. Lua V9999 Obfuscator (Tải file lên & Nhận file về)</label>
            <form action="/obfuscate-lua" method="POST" enctype="multipart/form-data">
                <input type="file" name="lua_file" accept=".lua,.txt" required>
                <button type="submit" class="btn btn-lua">Mã Hóa & Tải File Lua V9999</button>
            </form>
        </div>

        <!-- 3. Python V9999 Obfuscator -->
        <div class="section" style="border-bottom: none;">
            <label>3. Python V9999 Obfuscator (Tải file lên & Nhận file về)</label>
            <form action="/obfuscate-py" method="POST" enctype="multipart/form-data">
                <input type="file" name="py_file" accept=".py,.txt" required>
                <button type="submit" class="btn btn-py">Mã Hóa & Tải File Python V9999</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HOME_HTML)

@app.route('/boctach', methods=['POST'])
def boctach():
    link = request.form.get('target_link', '').strip()
    parsed = urllib.parse.unquote(link)
    flash(f'Kết quả bóc tách/giải mã: {parsed}')
    return redirect(url_for('index'))

@app.route('/obfuscate-lua', methods=['POST'])
def obfuscate_lua():
    if 'lua_file' not in request.files:
        flash('Chưa chọn file Lua!')
        return redirect(url_for('index'))
    
    file = request.files['lua_file']
    if file.filename == '':
        flash('Tên file không hợp lệ!')
        return redirect(url_for('index'))
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Đọc nội dung file Lua gốc
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Tiến hành mã hóa bằng Lua V9999 Pro
        obfuscated_content = lua_v9999_obfuscator(content)
        
        # Lưu file kết quả
        out_filename = f"obfuscated_{file.filename}"
        out_path = os.path.join(UPLOAD_FOLDER, out_filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_content)
            
        return send_file(out_path, as_attachment=True)

@app.route('/obfuscate-py', methods=['POST'])
def obfuscate_py():
    if 'py_file' not in request.files:
        flash('Chưa chọn file Python!')
        return redirect(url_for('index'))
    
    file = request.files['py_file']
    if file.filename == '':
        flash('Tên file không hợp lệ!')
        return redirect(url_for('index'))
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        obfuscated_content = python_v9999_obfuscator(content)
        
        out_filename = f"obfuscated_{file.filename}"
        out_path = os.path.join(UPLOAD_FOLDER, out_filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(obfuscated_content)
            
        return send_file(out_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
