-- Create database
CREATE DATABASE IF NOT EXISTS academiX_dev_db;
CREATE USER IF NOT EXISTS 'academix_user'@'localhost' IDENTIFIED BY 'academix';
GRANT ALL PRIVILEGES ON academiX_dev_db.* TO 'academix_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'academix_user'@'localhost';
FLUSH PRIVILEGES;