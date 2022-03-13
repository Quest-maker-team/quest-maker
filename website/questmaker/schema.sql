-- File will contain creating tables requests

DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    hash_password VARCHAR(200) NOT NULL,
    email VARCHAR(50),
    status_id INTEGER
);