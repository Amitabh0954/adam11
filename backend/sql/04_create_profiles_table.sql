CREATE TABLE profiles (
    user_id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);