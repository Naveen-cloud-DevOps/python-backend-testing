-- Create database if not exists
CREATE DATABASE IF NOT EXISTS dev;

-- Use the database
USE dev;

-- Create users table if not exists
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);