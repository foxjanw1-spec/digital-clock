from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import uuid
from werkzeug.utils import secure_filename
from config import ADMIN_PASSWORD, UPLOAD_FOLDER, MAX_CONTENT_LENGTH, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# تأكد من وجود مجلد uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# قائمة بجميع الملفات (مثالي للعرض العام)
# في تطبيق حقيقي، ستُستخدم قاعدة بيانات
uploaded_files = []

@app.route('/')
def index():
    """الصفحة العامة"""
    return render_template('index.html', files=uploaded_files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('كلمة المرور غير صحيحة.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """لوحة التحكم"""
    if not session.get('logged_in'):
        flash('يجب تسجيل الدخول أولاً.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html', files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    """رفع الملف"""
    if not session.get('logged_in'):
        flash('يجب تسجيل الدخول أولاً.', 'error')
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('لا يوجد ملف مرفوع.', 'error')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('لم يتم اختيار ملف.', 'error')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        # إضافة معرف فريد لتجنب تكرار الأسماء
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        # إضافة الملف إلى القائمة (في تطبيق حقيقي استخدم قاعدة بيانات)
        uploaded_files.append({'name': filename, 'path': unique_filename})
        flash(f'تم رفع الملف "{filename}" بنجاح!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج بنجاح.', 'info')
    return redirect(url_for('index'))

# روت لتحميل الملفات (يمكن الوصول إليها من قبل الزوار)
@app.route('/uploads/<path:filename>')
def download_file(filename):
    """تحميل ملف (يمكن الوصول إليه من قبل الزوار)"""
    # يُفضل أن تُستخدم خادم الملفات مثل Nginx في الإنتاج
    # لكن هنا نستخدم Flask لسهولة العرض
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return "الملف غير موجود.", 404


if __name__ == '__main__':
    app.run(debug=True)