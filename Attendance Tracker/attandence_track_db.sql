-- =========================================
-- ATTENDANCE TRACKER DATABASE SETUP
-- =========================================

-- Create database
CREATE DATABASE attendance_db;

-- Use the database
USE attendance_db;

-- =============================
-- 1️⃣ Table: students
-- =============================
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    department VARCHAR(50),
    semester VARCHAR(20),
    contact VARCHAR(15),
    email VARCHAR(100)
);

-- =============================
-- 2️⃣ Table: attendance
-- =============================
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late') DEFAULT 'Absent',
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- =============================
-- 3️⃣ Table: admin (for login system)
-- =============================
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- =============================
-- Sample Admin Account
-- =============================
INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');  -- You can encrypt this later in Python

-- =============================
-- Sample Students Data
-- =============================
INSERT INTO students (name, roll_no, department, semester, contact, email)
VALUES
('Rahul Sharma', 'CS101', 'Computer Science', '5th', '9876543210', 'rahul@example.com'),
('Priya Patel', 'CS102', 'Computer Science', '5th', '9876501234', 'priya@example.com'),
('Amit Verma', 'CS103', 'Computer Science', '5th', '9876505678', 'amit@example.com'),
('Sneha Gupta', 'CS104', 'Computer Science', '5th', '9876509876', 'sneha@example.com'),
('Rohit Mehta', 'CS105', 'Computer Science', '5th', '9876512345', 'rohit@example.com'),
('Anjali Singh', 'CS106', 'Computer Science', '5th', '9876523456', 'anjali@example.com'),
('Vivek Nair', 'CS107', 'Computer Science', '5th', '9876534567', 'vivek@example.com'),
('Pooja Yadav', 'CS108', 'Computer Science', '5th', '9876545678', 'pooja@example.com'),
('Arjun Reddy', 'CS109', 'Computer Science', '5th', '9876556789', 'arjun@example.com'),
('Kiran Kumar', 'CS110', 'Computer Science', '5th', '9876567890', 'kiran@example.com');

-- =============================
-- Sample Attendance Records
-- =============================
INSERT INTO attendance (student_id, date, status)
VALUES
(1, '2025-10-27', 'Present'),
(2, '2025-10-27', 'Absent'),
(3, '2025-10-27', 'Present'),
(4, '2025-10-27', 'Late'),
(5, '2025-10-27', 'Present'),
(6, '2025-10-27', 'Present'),
(7, '2025-10-27', 'Absent'),
(8, '2025-10-27', 'Late'),
(9, '2025-10-27', 'Present'),
(10, '2025-10-27', 'Present'),

(1, '2025-10-28', 'Present'),
(2, '2025-10-28', 'Present'),
(3, '2025-10-28', 'Absent'),
(4, '2025-10-28', 'Present'),
(5, '2025-10-28', 'Late'),
(6, '2025-10-28', 'Present'),
(7, '2025-10-28', 'Present'),
(8, '2025-10-28', 'Absent'),
(9, '2025-10-28', 'Present'),
(10, '2025-10-28', 'Present'),

(1, '2025-10-29', 'Present'),
(2, '2025-10-29', 'Absent'),
(3, '2025-10-29', 'Present'),
(4, '2025-10-29', 'Late'),
(5, '2025-10-29', 'Present'),
(6, '2025-10-29', 'Present'),
(7, '2025-10-29', 'Absent'),
(8, '2025-10-29', 'Late'),
(9, '2025-10-29', 'Present'),
(10, '2025-10-29', 'Present');




