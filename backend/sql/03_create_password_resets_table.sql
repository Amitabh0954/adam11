CREATE TABLE password_resets (
    token VARCHAR(255) PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    expires_at TIMESTAMP NOT NULL
);