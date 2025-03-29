<?php
session_start();

// Check if the user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}

$username = $_SESSION['username'];
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <div class="container">
      <nav>
        <div class="logo-placeholder">LOGO</div>
        <ul>
          <li><a href="index.html">HOME</a></li>
          <li><a href="about.html">ABOUT</a></li>
          <li><a href="contact.html">CONTACT</a></li>
          <li><a href="blog.html">BLOG</a></li>
          <li><a href="logout.php" class="logout-button">LOGOUT</a></li>
        </ul>
      </nav>
      <h1>Welcome, <?php echo htmlspecialchars($username); ?>!</h1>
      <p class="subtitle">Thank you for signing up. Explore the future of intelligent systems with us.</p>
    </div>
  </header>

  <main class="container">
    <section>
      <h2>Getting Started</h2>
      <p>Here are some resources to help you get started:</p>
      <ul>
        <li><a href="blog.html">Read our latest blog posts</a></li>
        <li><a href="about.html">Learn more about our mission</a></li>
        <li><a href="contact.html">Get in touch with us</a></li>
      </ul>
    </section>
  </main>

  <footer>
    <div class="container">
      <p>&copy; 2025 AI Insights. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>