from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

app = Flask(__name__)
app.secret_key = 'dev-secret-for-local'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    positions = ['Software Engineer', 'Payroll Accountant', 'Product Manager', 'Other']
    return render_template('index.html', positions=positions)

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    position = request.form.get('position', '')
    accept = request.form.get('accept')

    errors = []
    if not name:
        errors.append('Name is required')
    if not email:
        errors.append('Email is required')
    if not phone:
        errors.append('Phone is required')
    if not accept:
        errors.append('You must accept the terms')

    file = request.files.get('resume')
    if not file or file.filename == '':
        errors.append('Resume is required')
    elif not allowed_file(file.filename):
        errors.append('Invalid file type')

    if errors:
        for e in errors:
            flash(e)
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    flash('Form submitted successfully!')
    return redirect(url_for('index'))

@app.route('/api/apply', methods=['POST'])
def api_apply():
    data = request.json or {}
    required = ['name', 'email', 'phone', 'position', 'accept']
    missing = [r for r in required if not data.get(r)]
    if missing:
        return jsonify({'ok': False, 'missing': missing}), 400
    return jsonify({'ok': True, 'message': 'received'}), 200

if __name__ == '__main__':
    app.run(debug=True)