from flask import Flask, render_template, request
import os
from main import kyc_check

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', results=None)

@app.route('/check', methods=['POST'])
def check():
    file = request.files['photo']
    if file.filename == '':
        return render_template('index.html', results=None)
    path = os.path.join(UPLOAD_FOLDER, 'current.jpg')
    file.save(path)
    results = kyc_check(path)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
