from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
import requests
import openpyxl
import io
import os
import json
import time

app = Flask(__name__)
app.secret_key = "super_secret_key"

PAID_FILE = "paid_users.json"
TOKENS_FILE = "tokens.json"

# ----------------- Utility -----------------
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ----------------- Templates -----------------
main_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Data Extractor</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(180deg, #6a11cb, #2575fc);
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            border-radius: 16px;
            padding: 30px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            font-size: 1.4em;
            margin-bottom: 5px;
            color: #222;
        }
        .version {
            font-size: 0.8em;
            color: #666;
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            height: 100px;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
            font-size: 0.9em;
            resize: none;
        }
        input[type="file"], select, button {
            width: 100%;
            margin-top: 10px;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 0.9em;
        }
        button {
            background-color: #2575fc;
            color: #fff;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #1a5ed9;
        }
        footer {
            font-size: 0.75em;
            color: #888;
            margin-top: 20px;
        }
        .flash { color: green; margin-top: 10px; }
        .warn { color: orange; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Automated Data Extractor</h1>
        <div class="version">v2.0 FREEMIUM EDITION</div>

        {% if not paid %}
        <p class="warn">🎁 You have <strong>1 free extraction</strong> to try our service.</p>
        {% endif %}

        <form method="POST" enctype="multipart/form-data">
            <label>URLs to Extract (one per line)</label>
            <textarea name="urls" placeholder="https://api.example.com/data
https://jsonplaceholder.typicode.com/users"></textarea>

            <p>Or Upload URLs File (.txt)</p>
            <input type="file" name="file">

            <label>Export Format</label>
            <select name="format">
                <option value="xlsx">Excel (.xlsx)</option>
                <option value="txt">Text (.txt)</option>
            </select>

            <button type="submit">🎯 Extract Data</button>
        </form>

        {% if not paid %}
        <p class="warn">⚠️ Free extraction used! Unlock unlimited access with a one-time payment.</p>
        <form method="POST" action="/verify_payment">
            <button type="button" onclick="window.location.href='upi://pay?pa=lalsangzuali2@ptaxis&pn=Data Extractor&am=99&cu=INR'">Pay via UPI</button>
            <button type="button" onclick="window.open('https://paypal.me/JoeBta7','_blank')">Pay via PayPal</button>
            <br><br>
            <input type="text" name="txn_id" placeholder="Enter Transaction ID / Code" required>
            <button type="submit">Verify Payment</button>
        </form>
        {% endif %}

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="flash">
                {% for msg in messages %}
                    <p>{{ msg }}</p>
                {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <footer>Made with ❤️ | Data Extractor v2.0 | Professional Edition</footer>
    </div>
</body>
</html>
"""

# ----------------- Routes -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    paid_users = load_json(PAID_FILE)
    user_ip = request.remote_addr
    is_paid = user_ip in paid_users

    if request.method == "POST" and is_paid is False:
        flash("⚠️ Free trial used! Please complete payment to continue.")
        return render_template_string(main_html, paid=is_paid)

    if request.method == "POST":
        urls = request.form.get("urls", "").strip().splitlines()
        file = request.files.get("file")
        export_format = request.form.get("format", "xlsx")

        if file and file.filename.endswith(".txt"):
            urls = file.read().decode("utf-8").splitlines()
        urls = [u.strip() for u in urls if u.strip()]
        if not urls:
            return "No valid URLs provided", 400

        results = []
        for url in urls:
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    results.append({"url": url, "data": res.text[:200]})
                else:
                    results.append({"url": url, "data": f"Error {res.status_code}"})
            except Exception as e:
                results.append({"url": url, "data": str(e)})

        if export_format == "xlsx":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Extracted Data"
            ws.append(["URL", "Response Preview"])
            for r in results:
                ws.append([r["url"], r["data"]])
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name="extracted_data.xlsx")
        else:
            output = io.StringIO()
            for r in results:
                output.write(f"{r['url']}: {r['data']}\n")
            output.seek(0)
            return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name="extracted_data.txt")

    return render_template_string(main_html, paid=is_paid)


@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    txn_id = request.form.get("txn_id", "").strip()
    tokens = load_json(TOKENS_FILE)
    paid = load_json(PAID_FILE)
    user_ip = request.remote_addr

    if txn_id in tokens:
        paid[user_ip] = {"txn_id": txn_id, "timestamp": time.time()}
        save_json(PAID_FILE, paid)
        del tokens[txn_id]
        save_json(TOKENS_FILE, tokens)
        flash("✅ Payment verified successfully! You now have unlimited access.")
    else:
        flash("❌ Invalid Transaction ID. Contact admin for help.")

    return redirect(url_for("index"))

# ----------------- Run -----------------
if __name__ == "__main__":
    is_replit = "REPL_ID" in os.environ or "REPLIT_DB_URL" in os.environ
    port = 5000 if is_replit else 8080
    host = "0.0.0.0"
    print(f"Running in {'Replit Cloud' if is_replit else 'Local iSH'} mode...")
    os.makedirs("output", exist_ok=True)
    app.run(host=host, port=port)