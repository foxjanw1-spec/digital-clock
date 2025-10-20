const express = require('express');
const multer = require('multer');
const path = require('path');
const session = require('express-session');

const app = express();
const PORT = process.env.PORT || 3000;

// إعداد multer لرفع الملفات
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname); // تجنب تكرار الأسماء
  }
});
const upload = multer({ storage: storage });

// إعداد الجلسات
app.use(session({
  secret: 'your_secret_key_here', // يجب تغيير هذا في الإنتاج
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false } // يجب تعيين secure: true في HTTPS
}));

// إعداد محرك العرض EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// إعداد مجلد الموارد العامة
app.use(express.static(path.join(__dirname, 'public')));

// إعداد تحليل البيانات
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// كلمة المرور الخاصة بالمسؤول
const ADMIN_PASSWORD = 'ab200631';

// قائمة بجميع الملفات (مثالي للعرض العام)
let uploadedFiles = [];

// Middleware للتحقق من تسجيل الدخول
function requireAuth(req, res, next) {
  if (req.session && req.session.isLoggedIn) {
    next();
  } else {
    res.redirect('/login');
  }
}

// المسارات الرئيسية
app.get('/', (req, res) => {
  // عرض الملفات المشتركة
  res.render('index', { files: uploadedFiles });
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { password } = req.body;
  if (password === ADMIN_PASSWORD) {
    req.session.isLoggedIn = true;
    res.redirect('/dashboard');
  } else {
    res.render('login', { error: 'كلمة المرور غير صحيحة.' });
  }
});

app.get('/dashboard', requireAuth, (req, res) => {
  res.render('dashboard', { files: uploadedFiles });
});

app.post('/upload', requireAuth, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('لا يوجد ملف مرفوع.');
  }
  // إضافة الملف إلى القائمة (في تطبيق حقيقي استخدم قاعدة بيانات)
  uploadedFiles.push({
    name: req.file.originalname,
    path: req.file.filename // اسم الملف على الخادم
  });
  res.redirect('/dashboard');
});

app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
    }
    res.redirect('/');
  });
});

// روت لتحميل الملفات (يمكن الوصول إليها من قبل الزوار)
app.get('/uploads/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, 'uploads', filename);
  res.download(filePath, (err) => {
    if (err) {
      res.status(404).send('الملف غير موجود.');
    }
  });
});

// تشغيل الخادم
app.listen(PORT, () => {
  console.log(`التطبيق يعمل على المنفذ ${PORT}`);
});