-- File will contain creating tables requests

DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL,
    hash_password VARCHAR(100) NOT NULL,
    email VARCHAR(50),
    status_id INTEGER
);