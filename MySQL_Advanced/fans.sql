-- 2. Fans
-- SQL script that creates the table fans

CREATE TABLE IF NOT EXISTS fans (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);

