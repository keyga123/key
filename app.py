import base64
import json
import random
import urllib.parse
from flask import Flask, render_template_string, request, send_file
import io
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>GA GAMING - File Toolkit (Upload & Download)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f9; }
        .container { max-width: 750px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"], input[type="file"] { width: 100%; padding: 10px; margin: 5px 0 15px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button.blue { background: #007bff; }
        button.purple { background: #6f42c1; }
        button.orange { background: #fd7e14; }
        button:hover { opacity: 0.9; }
        pre { background: #eee; padding: 10px; border-radius: 4px; overflow-x: auto; font-family: monospace; max-height: 200px; white-space: pre-wrap; word-break: break-all; }
        .section { margin-bottom: 25px; border-bottom: 1px solid #ddd; padding-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 GA GAMING - Toolkit Upload & Download File 🔥</h2>
        
        <!-- 1. Bóc Tách Link -->
        <div class="section">
            <h3>1. Bóc Tách & Giải Mã Link</h3>
            <form method="POST" action="/resolve">
                <input type="text" name="url" placeholder="Nhập link cần bóc tách..." required>
                <button type="submit" class="blue">Bóc Tách Link</button>
            </form>
            {% if link_result %}
                <p><b>Kết quả:</b></p>
                <pre>{{ link_result }}</pre>
            {% endif %}
        </div>

        <!-- 2. Lua V9999 Obfuscator (Upload File -> Download File) -->
        <div class="section">
            <h3>2. Lua V9999 Obfuscator (Tải file lên & Nhận file về)</h3>
            <form method="POST" action="/obfuscate-lua" enctype="multipart/form-data">
                <input type="file" name="lua_file" accept=".lua" required>
                <button type="submit" class="purple">Mã Hóa & Tải File Lua V9999</button>
            </form>
        </div>

        <!-- 3. Python V9999 Obfuscator (Upload File -> Download File) -->
        <div class="section">
            <h3>3. Python V9999 Obfuscator (Tải file lên & Nhận file về)</h3>
            <form method="POST" action="/obfuscate-python" enctype="multipart/form-data">
                <input type="file" name="py_file" accept=".py" required>
                <button type="submit" class="orange">Mã Hóa & Tải File Python V9999</button>
            </form>
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
  return render_template_string(HTML_TEMPLATE, link_result=None)


@app.route("/resolve", methods=["POST"])
def resolve_link():
  target_url = request.form.get("url")
  redirect_chain = []
  final_url = target_url
  decoded_data = {}
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    session = requests.Session()
    response = session.get(
        target_url, headers=headers, allow_redirects=True, timeout=10
    )
    for resp in response.history:
      redirect_chain.append(
          {"status_code": resp.status_code, "url": resp.url}
      )
    final_url = response.url

    parsed_url = urllib.parse.urlparse(final_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    for key, values in query_params.items():
      for val in values:
        try:
          padding = "=" * (-len(val) % 4)
          decoded_bytes = base64.b64decode(val + padding)
          decoded_str = decoded_bytes.decode("utf-8")
          if (
              decoded_str.startswith("http://")
              or decoded_str.startswith("https://")
          ):
            decoded_data[key] = decoded_str
        except Exception:
          pass

    result_data = {
        "input_url": target_url,
        "redirect_chain": redirect_chain,
        "final_destination": final_url,
        "query_parameters": query_params,
        "base64_decoded_links": decoded_data,
    }
    return render_template_string(
        HTML_TEMPLATE,
        link_result=json.dumps(result_data, indent=4, ensure_ascii=False),
    )
  except Exception as e:
    return render_template_string(HTML_TEMPLATE, link_result=f"Lỗi: {str(e)}")


@app.route("/obfuscate-lua", methods=["POST"])
def obfuscate_lua():
  uploaded_file = request.files.get("lua_file")
  if not uploaded_file:
    return "Lỗi: Chưa chọn file Lua!", 400

  filename = uploaded_file.filename
  source_code = uploaded_file.read().decode("utf-8", errors="ignore")

  opcodes = [random.randint(1000, 9999) for _ in range(len(source_code))]
  opcode_map = "{" + ",".join(map(str, opcodes)) + "}"
  key = random.randint(10, 99)

  encoded = [
      str(ord(char) ^ key ^ (opcodes[i] % 255))
      for i, char in enumerate(source_code)
  ]
  payload = "{" + ",".join(encoded) + "}"

  v9999_template = f"""--[[ 👑 GA GAMING V9999 - LUA VM OBFUSCATOR 👑 ]]
local _k = {key}
local _op = {opcode_map}
local _p = {payload}
local _buf = ""

for _i = 1, #_p do
    local _byte = bit32.bxor(_p[_i], bit32.bxor(_k, (_op[_i] % 255)))
    _buf = _buf .. string.char(_byte)
end

local _run = loadstring or load
local _env = getfenv and getfenv() or _G
local _c = _run(_buf)
if setfenv then setfenv(_c, _env) end
pcall(_c)
"""

  out_filename = filename.replace(".lua", "_v9999.lua")
  if not out_filename.endswith("_v9999.lua"):
    out_filename += "_v9999.lua"

  file_stream = io.BytesIO(v9999_template.encode("utf-8"))
  return send_file(
      file_stream,
      as_attachment=True,
      download_name=out_filename,
      mimetype="text/plain",
  )


@app.route("/obfuscate-python", methods=["POST"])
def obfuscate_python():
  uploaded_file = request.files.get("py_file")
  if not uploaded_file:
    return "Lỗi: Chưa chọn file Python!", 400

  filename = uploaded_file.filename
  source_code = uploaded_file.read().decode("utf-8", errors="ignore")

  opcodes = [random.randint(1000, 9999) for _ in range(len(source_code))]
  opcode_map = "[" + ",".join(map(str, opcodes)) + "]"
  key = random.randint(10, 99)

  encoded = [
      str(ord(char) ^ key ^ (opcodes[i] % 255))
      for i, char in enumerate(source_code)
  ]
  payload = "[" + ",".join(encoded) + "]"

  py_template = f"""# -*- coding: utf-8 -*-
# 👑 GA GAMING V9999 - PYTHON VM OBFUSCATOR 👑
_k = {key}
_op = {opcode_map}
_p = {payload}
_buf = ""

for _i in range(len(_p)):
    _byte = _p[_i] ^ _k ^ (_op[_i] % 255)
    _buf += chr(_byte)

exec(_buf)
"""

  out_filename = filename.replace(".py", "_v9999.py")
  if not out_filename.endswith("_v9999.py"):
    out_filename += "_v9999.py"

  file_stream = io.BytesIO(py_template.encode("utf-8"))
  return send_file(
      file_stream,
      as_attachment=True,
      download_name=out_filename,
      mimetype="text/plain",
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
