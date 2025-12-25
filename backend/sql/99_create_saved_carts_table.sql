CREATE TABLE saved_carts (
    user_id INT PRIMARY KEY REFERENCES users(id),
    cart JSONB NOT NULL
);