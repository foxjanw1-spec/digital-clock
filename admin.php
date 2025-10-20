<?php
// admin.php - صفحة لوحة التحكم
session_start();

// كلمة المرور الخاصة بالمسؤول
$admin_password = 'ab200631';

// التحقق من تسجيل الدخول
if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
    // إذا لم يتم تسجيل الدخول، اطلب كلمة المرور
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $password = $_POST['password'];
        if ($password === $admin_password) {
            $_SESSION['admin_logged_in'] = true;
            header('Location: dashboard.php'); // إعادة توجيه إلى لوحة التحكم
            exit();
        } else {
            $error_message = 'كلمة المرور غير صحيحة.';
        }
    }
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>لوحة التحكم</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div class="login-container">
            <h2>دخول لوحة التحكم</h2>
            <?php if (isset($error_message)): ?>
                <p class="error"><?php echo $error_message; ?></p>
            <?php endif; ?>
            <form method="POST">
                <label for="password">كلمة المرور:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="دخول">
            </form>
        </div>
    </body>
    </html>
    <?php
    exit(); // إنهاء البرنامج حتى لا يُنفذ الكود التالي
}

// إذا تم تسجيل الدخول بنجاح، عرض لوحة التحكم
?>
<!DOCTYPE html>
<html>
<head>
    <title>لوحة التحكم - موقع الملفات</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>مرحباً بك في لوحة التحكم</h1>
    <p>يمكنك هنا رفع، عرض، وحذف ملفاتك.</p>

    <!-- نموذج رفع الملف -->
    <form action="upload.php" method="post" enctype="multipart/form-data">
        <label for="fileToUpload">اختر ملف:</label>
        <input type="file" name="fileToUpload" id="fileToUpload" required><br><br>
        <input type="submit" value="رفع الملف" name="submit">
    </form>

    <!-- عرض الملفات -->
    <h2>ملفاتك:</h2>
    <!-- هنا سيتم عرض الملفات باستخدام كود PHP -->

    <a href="logout.php">تسجيل الخروج</a>
</body>
</html>