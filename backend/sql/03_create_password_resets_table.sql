CREATE TABLE password_resets (
    token VARCHAR(32) PRIMARY KEY,
    user_id INT NOT NULL,
    expiry TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);