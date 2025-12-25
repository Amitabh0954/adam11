CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    price FLOAT NOT NULL CHECK (price > 0),
    description TEXT NOT NULL,
    category VARCHAR(255),
    attributes JSONB
);