<?php
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Include the configuration file
include 'config.php';
// Include PHPMailer
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
require 'vendor/autoload.php';

// Generate CSRF token
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// Database connection
$conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check CSRF token
    if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        exit("Error: Invalid CSRF token.");
    }

    // Sanitize and validate input
    $username = trim($_POST['username']);
    $email = filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL);
    $password = password_hash(trim($_POST['password']), PASSWORD_DEFAULT);

    if (!$email) {
        exit("Error: Invalid email address.");
    }

    // Check if username or email already exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE username = ? OR email = ?");
    $stmt->bind_param("ss", $username, $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        exit("Error: Username or email already taken. Choose another.");
    }

    // Insert new user with inactive status
    $activation_code = bin2hex(random_bytes(16));
    $stmt_insert = $conn->prepare("INSERT INTO users (username, email, password, activation_code, status) VALUES (?, ?, ?, ?, 'inactive')");
    $stmt_insert->bind_param("ssss", $username, $email, $password, $activation_code);

    if ($stmt_insert->execute()) {
        // Send activation email using PHPMailer
        $mail = new PHPMailer(true);
        try {
            //Server settings
            $mail->isSMTP();
            $mail->Host = 'smtp.mailprovider.com'; // Change this to your mail provider's SMTP server
            $mail->SMTPAuth = true;
            $mail->Username = 'info@oforha.ai'; // Change this to your email
            $mail->Password = ''; // Change this to your email password
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS; // Enable SSL encryption
            $mail->Port = 465; // Change this to your mail provider's SMTP port

            //Recipients
            $mail->setFrom('no-reply@oforha.ai', 'Mailer');
            $mail->addAddress($email);

            //Content
            $mail->isHTML(true);
            $mail->Subject = 'Activate your account';
            $activation_link = "http://oforha.ai/activate.php?code=$activation_code"; // Ensure this URL is correct
            $mail->Body = "Click the following link to activate your account: <a href='$activation_link'>$activation_link</a>";

            $mail->send();
            exit("Success: Registration successful. Please check your email to activate your account.");
        } catch (Exception $e) {
            error_log("Error: Unable to send activation email. Mailer Error: {$mail->ErrorInfo}");
            exit("Error: Unable to send activation email. Try again later.");
        }
    } else {
        exit("Error: Unable to register at this time. Try again later.");
    }

    // Close statements
    $stmt->close();
    $stmt_insert->close();
}

// Close connection
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign Up</title>
  <link rel="stylesheet" href="style.css">
  <script>
    function validateForm() {
      const password = document.getElementById('password').value;
      if (password.length < 6) {
        alert('Password must be at least 6 characters long.');
        return false;
      }
      return true;
    }
  </script>
</head>
<body>
  <div class="container">
    <h2>Sign Up</h2>
    <form action="signup.php" method="post" onsubmit="return validateForm();">
      <input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>

      <label for="email">Email:</label>
      <input type="email" id="email" name="email" required>

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>

      <button type="submit">Sign Up</button>
    </form>
  </div>
</body>
</html>
