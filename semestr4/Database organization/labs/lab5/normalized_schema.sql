-- Лабораторна робота №5
-- Фінальна схема бази даних у 3NF.

DROP TABLE IF EXISTS generation_parameters CASCADE;
DROP TABLE IF EXISTS generations CASCADE;
DROP TABLE IF EXISTS attachments CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS ai_models CASCADE;
DROP TABLE IF EXISTS ai_model_families CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TYPE IF EXISTS message_role CASCADE;

CREATE TYPE message_role AS ENUM ('user', 'ai_model');

CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    second_name VARCHAR(80) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email LIKE '%@%'),
    country_id INTEGER NOT NULL REFERENCES countries(country_id),
    created_at DATE NOT NULL
);

CREATE TABLE ai_model_families (
    family_id SERIAL PRIMARY KEY,
    family_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE ai_models (
    model_id SERIAL PRIMARY KEY,
    family_id INTEGER NOT NULL REFERENCES ai_model_families(family_id),
    model_version VARCHAR(20) NOT NULL,
    UNIQUE (family_id, model_version)
);

CREATE TABLE chats (
    chat_id SERIAL PRIMARY KEY,
    owner_user_id INTEGER NOT NULL REFERENCES users(user_id),
    title VARCHAR(50) NOT NULL DEFAULT 'chat',
    created_at DATE NOT NULL
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL REFERENCES chats(chat_id),
    role_m message_role NOT NULL,
    content_m TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE attachments (
    attachment_id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL REFERENCES messages(message_id),
    file_name VARCHAR(50) NOT NULL,
    size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
    path_a TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL
);

CREATE TABLE generations (
    generation_id SERIAL PRIMARY KEY,
    model_id INTEGER NOT NULL REFERENCES ai_models(model_id),
    message_id INTEGER NOT NULL UNIQUE REFERENCES messages(message_id),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE generation_parameters (
    generation_id INTEGER NOT NULL REFERENCES generations(generation_id) ON DELETE CASCADE,
    parameter_name VARCHAR(40) NOT NULL,
    parameter_value NUMERIC(12, 4) NOT NULL,
    PRIMARY KEY (generation_id, parameter_name)
);

CREATE OR REPLACE FUNCTION check_generation_message_role()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM messages
        WHERE message_id = NEW.message_id
          AND role_m = 'ai_model'
    ) THEN
        RAISE EXCEPTION 'Generation can reference only ai_model messages';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_generation_message_role
BEFORE INSERT OR UPDATE ON generations
FOR EACH ROW
EXECUTE FUNCTION check_generation_message_role();

INSERT INTO countries (country_name)
VALUES
    ('Ukraine'),
    ('USA'),
    ('Poland'),
    ('Belarus');

INSERT INTO users (first_name, second_name, user_name, email, country_id, created_at)
VALUES
    ('Artem', 'Davydchuk', 'artemdavydchuk', 'artem@gmail.com', 1, '2026-03-21'),
    ('Дмитро', 'Дубров', 'dubrov', 'dubrov@gmail.com', 1, '2026-03-20'),
    ('Max', 'Brown', 'maxbrown', 'max@gmail.com', 2, '2026-03-19'),
    ('Ilya', 'Lokotosh', 'lol', 'valorant@gmail.com', 3, '2026-03-18'),
    ('Ivan', 'Pedrenko', 'ivan_pedrenko', 'ivan_goida@gmail.com', 4, '2026-03-17');

INSERT INTO ai_model_families (family_name)
VALUES
    ('GPT'),
    ('Claude'),
    ('Llama'),
    ('DeepSeek');

INSERT INTO ai_models (family_id, model_version)
VALUES
    (1, '4o'),
    (1, '4.1'),
    (2, '3.7'),
    (3, '3.1'),
    (4, 'V3');

INSERT INTO chats (owner_user_id, title, created_at)
VALUES
    (1, 'Hello', '2026-03-21'),
    (1, 'nice', '2026-03-21'),
    (2, 'AI Discussion', '2026-03-20'),
    (3, 'Database Lab', '2026-03-19'),
    (5, 'Project Notes', '2026-03-18');

INSERT INTO messages (chat_id, role_m, content_m, created_at)
VALUES
    (1, 'user', 'Hello, how are you?', '2026-03-21 10:00:00'),
    (1, 'ai_model', 'I am fine, thank you. How can I help you?', '2026-03-21 10:00:05'),
    (2, 'user', 'Explain JOIN in SQL.', '2026-03-21 11:00:00'),
    (2, 'ai_model', 'JOIN is used to combine rows from two or more tables', '2026-03-21 11:00:06'),
    (3, 'user', 'What model are you?', '2026-03-20 09:15:00');

INSERT INTO attachments (message_id, file_name, size_bytes, path_a, uploaded_at)
VALUES
    (1, 'question.txt', 1024, '/files/question.txt', '2026-03-21 10:00:10'),
    (3, 'sql_notes.pdf', 204800, '/files/sql_notes.pdf', '2026-03-21 11:00:15'),
    (5, 'model_info.docx', 51200, '/files/model_info.docx', '2026-03-20 09:16:00');

INSERT INTO generations (model_id, message_id, created_at)
VALUES
    (1, 2, '2026-03-21 10:00:05'),
    (1, 4, '2026-03-21 11:00:06');

INSERT INTO generation_parameters (generation_id, parameter_name, parameter_value)
VALUES
    (1, 'temperature', 0.7),
    (1, 'max_tokens', 200),
    (1, 'top_p', 0.9),
    (2, 'temperature', 0.5),
    (2, 'max_tokens', 300),
    (2, 'top_p', 0.95);
