<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Include the configuration file
include 'config.php';

// Database connection
$conn = new mysqli($host, $dbUsername, $dbPassword, $dbName);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize and validate input
    $username = trim($_POST['username']);
    $email = filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL);
    $password = password_hash(trim($_POST['password']), PASSWORD_DEFAULT);

    if (!$email) {
        exit("Error: Invalid email address.");
    }

    // Check if username already exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        exit("Error: Username already taken. Choose another.");
    }

    // Check if email already exists
    $stmt_email = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $stmt_email->bind_param("s", $email);
    $stmt_email->execute();
    $stmt_email->store_result();

    if ($stmt_email->num_rows > 0) {
        exit("Error: Email already registered. Choose another.");
    }

    // Insert new user
    $stmt_insert = $conn->prepare("INSERT INTO users (username, email, password) VALUES (?, ?, ?)");
    $stmt_insert->bind_param("sss", $username, $email, $password);

    if ($stmt_insert->execute()) {
        header("Location: welcome.php"); // Redirect to welcome page after successful signup
        exit;
    } else {
        exit("Error: Unable to register at this time. Try again later.");
    }

    // Close statements
    $stmt->close();
    $stmt_email->close();
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
</head>
<body>
  <div>
    <h2>Sign Up</h2>
    <form action="signup.php" method="post">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required>

      <label for="email">Email:</label>
      <input type="email" id="email" name="email" required>

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>

      <button type="submit">Sign Up</button>
    </form>
  </body>
</html>
