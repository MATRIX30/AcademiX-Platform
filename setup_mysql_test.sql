-- Create database
CREATE DATABASE IF NOT EXISTS academiX_test_db;
CREATE USER IF NOT EXISTS 'academix_test'@'localhost' IDENTIFIED BY 'academix';
GRANT ALL PRIVILEGES ON academiX_test_db.* TO 'academix_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'academix_test'@'localhost';
FLUSH PRIVILEGES;