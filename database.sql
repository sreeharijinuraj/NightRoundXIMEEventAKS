CREATE DATABASE IF NOT EXISTS `nightround_db`;
USE `nightround_db`;

CREATE TABLE IF NOT EXISTS `contacts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(100),
    `last_name` VARCHAR(100),
    `email` VARCHAR(255),
    `company` VARCHAR(255),
    `message` TEXT,
    `submitted_at` DATETIME
);
