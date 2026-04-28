-- Active: 1776252443178@@dpg-d7fn6gf7f7vs73a59ae0-a.virginia-postgres.render.com@5432
-- Active: 1776252443178@@dpg-d7fn6gf7f7vs73a59ae0-a.virginia-postgres.render.com@5432
CREATE TABLE IF NOT EXISTS urls (
        id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        name VARCHAR(255) UNIQUE NOT NULL,
        created_at DATE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS url_checks (
        id SERIAL PRIMARY KEY,
        url_id INT REFERENCES urls (id) NOT NULL,
        status_code INT,
        h1 text,
        title text NOT NULL,
        description text,
        created_at DATE DEFAULT CURRENT_TIMESTAMP
);