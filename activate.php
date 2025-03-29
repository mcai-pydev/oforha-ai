<?php
session_start();
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

// Handle activation
if (isset($_GET['code'])) {
    $activation_code = $_GET['code'];

    // Check if activation code is valid
    $stmt = $conn->prepare("SELECT id FROM users WHERE activation_code = ? AND status = 'inactive'");
    $stmt->bind_param("s", $activation_code);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        // Activate user account
        $stmt_update = $conn->prepare("UPDATE users SET status = 'active', activation_code = NULL WHERE activation_code = ?");
        $stmt_update->bind_param("s", $activation_code);

        if ($stmt_update->execute()) {
            exit("Success: Your account has been activated. You can now <a href='login.php'>login</a>.");
        } else {
            exit("Error: Unable to activate your account. Try again later.");
        }
    } else {
        exit("Error: Invalid activation code or account already activated.");
    }

    // Close statements
    $stmt->close();
    $stmt_update->close();
}

// Close connection
$conn->close();
?>