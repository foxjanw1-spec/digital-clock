import os

# إعدادات التطبيق
SECRET_KEY = 'your_secret_key_here' # يجب تغيير هذا في الإنتاج
ADMIN_PASSWORD = 'ab200631' # كلمة المرور الخاصة بالمسؤول
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # حد أقصى لحجم الملف 16 ميجابايت