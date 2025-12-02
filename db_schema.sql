-- Table 1: Banks
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(150)
);

-- Table 2: Reviews
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score REAL,
    source VARCHAR(50)
);
INSERT INTO banks (bank_name, app_name)
VALUES 
    ('CBE', 'CBE Mobile Banking'),
    ('BOA', 'Bank of Abyssinia'),
    ('Dashen', 'Dashen Bank');
SELECT COUNT(*) FROM reviews;
