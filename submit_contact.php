<?php
// submit_contact.php
header('Content-Type: application/json');

// Database configuration
$host = 'localhost';
// We'll use a default database name 'nightround_db'
$dbname = 'nightround_db';
$username = 'root';
// Default XAMPP password is empty
$password = '';

try {
    // 1. Connect to MySQL (without selecting db first)
    $pdo = new PDO("mysql:host=$host", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 2. Create database if it doesn't exist
    $pdo->exec("CREATE DATABASE IF NOT EXISTS `$dbname`");
    $pdo->exec("USE `$dbname`");

    // 3. Create table if it doesn't exist
    $pdo->exec("CREATE TABLE IF NOT EXISTS contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        company VARCHAR(255),
        message TEXT,
        submitted_at DATETIME
    )");

    // 4. Get JSON POST data sent by fetch()
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if (!$data) {
        throw new Exception('Invalid JSON data received.');
    }

    // 5. Insert data into our `contacts` table
    $stmt = $pdo->prepare("INSERT INTO contacts (first_name, last_name, email, company, message, submitted_at) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->execute([
        $data['firstName'] ?? '',
        $data['lastName'] ?? '',
        $data['email'] ?? '',
        $data['company'] ?? '',
        $data['message'] ?? '',
        $data['submittedAt'] ?? date('Y-m-d H:i:s')
    ]);

    // 6. Send success response back to the frontend
    echo json_encode(['status' => 'success', 'message' => 'Form Submitted Successfully!!!!.']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => 'Database error: ' . $e->getMessage()]);
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}
?>