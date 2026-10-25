import base64
import urllib.parse
from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

# Giao diện HTML đơn giản để test trực tiếp trên web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Flask Link Resolver & Bypass</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f4f4f9; }
        .container { max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"] { width: 80%; padding: 10px; margin-right: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        pre { background: #eee; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Hệ Thống Bóc Tách Link & Bypass</h2>
        <form method="POST" action="/resolve">
            <input type="text" name="url" placeholder="Dán link rút gọn hoặc link cần bóc tách vào đây..." required>
            <button type="submit">Bóc Tách</button>
        </form>
        {% if result %}
            <h3>Kết quả:</h3>
            <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
  return render_template_string(HTML_TEMPLATE, result=None)


@app.route("/resolve", methods=["POST"])
def resolve_link():
  target_url = request.form.get("url")
  if not target_url:
    return render_template_string(
        HTML_TEMPLATE, result="Lỗi: Chưa nhập URL!"
    )

  redirect_chain = []
  final_url = target_url
  decoded_data = {}

  try:
    # 1. Theo dõi chuỗi HTTP Redirects
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    session = requests.Session()
    response = session.get(
        target_url, headers=headers, allow_redirects=True, timeout=10
    )

    # Lưu lại lịch sử các bước nhảy
    for resp in response.history:
      redirect_chain.append(
          {"status_code": resp.status_code, "url": resp.url}
      )

    final_url = response.url

    # 2. Phân tích các tham số Query String trong link đích
    parsed_url = urllib.parse.urlparse(final_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Thử quét xem có tham số nào bị mã hóa Base64 bên trong không để tự động giải mã
    for key, values in query_params.items():
      for val in values:
        try:
          # Thử decode base64 nếu chuỗi hợp lệ
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

    # Đóng gói kết quả trả về
    result_data = {
        "input_url": target_url,
        "redirect_chain": redirect_chain,
        "final_destination": final_url,
        "query_parameters": query_params,
        "base64_decoded_links": decoded_data,
    }

    import json

    formatted_result = json.dumps(result_data, indent=4, ensure_ascii=False)
    return render_template_string(HTML_TEMPLATE, result=formatted_result)

  except Exception as e:
    return render_template_string(
        HTML_TEMPLATE, result=f"Lỗi khi xử lý link: {str(e)}"
    )


if __name__ == "__main__":
  app.run(debug=True, port=5000)
