from flask import Flask, request, jsonify, send_file
import subprocess
import os
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h2>Automated Data Extractor</h2>
    <p>Upload a URLs file (.txt) or paste URLs to extract data from.</p>
    <form action="/extract" method="post" enctype="multipart/form-data">
        <textarea name="urls" rows="5" cols="60" placeholder="Enter URLs, one per line"></textarea><br>
        <input type="file" name="file"><br><br>
        <select name="format">
            <option value="txt">TXT</option>
            <option value="csv">CSV</option>
            <option value="xlsx">Excel</option>
        </select><br><br>
        <button type="submit">Run Extraction</button>
    </form>
    """

@app.route('/extract', methods=['POST'])
def extract():
    urls_text = request.form.get('urls')
    uploaded_file = request.files.get('file')
    export_format = request.form.get('format', 'xlsx')

    urls_file = "urls.txt"

    # If user uploaded a file
    if uploaded_file:
        uploaded_file.save(urls_file)
    elif urls_text:
        with open(urls_file, "w") as f:
            f.write(urls_text)

    # Run your existing extractor script
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_{timestamp}.{export_format}"

    cmd = ["python3", "extractor.py"]
    subprocess.run(cmd)

    # Return the output file (if it exists)
    for file in os.listdir("output"):
        if file.endswith(export_format):
            return send_file(os.path.join("output", file), as_attachment=True)

    return jsonify({"status": "failed", "message": "No output file generated."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
