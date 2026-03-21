DROP TABLE IF EXISTS generations CASCADE;
DROP TABLE IF EXISTS attachments CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS ai_models CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TYPE IF EXISTS message_role CASCADE;

-- Основний скелет

CREATE TYPE message_role AS ENUM ('user', 'ai_model');

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    second_name VARCHAR(80) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE ai_models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    model_version VARCHAR(20) NOT NULL
);

CREATE TABLE chats (
    chat_id SERIAL PRIMARY KEY,
    owner_user_id INTEGER NOT NULL UNIQE REFERENCES users(user_id),
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
    size_bytes BIGINT NOT NULL,
    path_a TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL
);

CREATE TABLE generations (
    generation_id SERIAL PRIMARY KEY,
    model_id INTEGER NOT NULL REFERENCES ai_models(model_id),
    message_id INTEGER NOT NULL UNIQUE REFERENCES messages(message_id),
    parameters JSONB NOT NULL CHECK (jsonb_typeof(parameters) = 'object'),
    created_at TIMESTAMP NOT NULL
);

-- Створення тригера на перевірки ролі

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

-- Вставка значень

INSERT INTO users (first_name, second_name, user_name, email, country, created_at)
VALUES
    ('Artem', 'Davydchuk', 'artemdavydchuk', 'artem@gmail.com', 'Ukraine', '2026-03-21'),
    ('Дмитро', 'Дубров', 'dubrov', 'dubrov@gmail.com', 'Ukraine', '2026-03-20'),
    ('Max', 'Brown', 'maxbrown', 'max@gmail.com', 'USA', '2026-03-19'),
    ('Ilya', 'Lokotosh', 'lol', 'valorant@gmail.com', 'Poland', '2026-03-18'),
    ('Ivan', 'Pedrenko', 'ivan_pedrenko', 'ivan_goida@gmail.com', 'Belarus', '2026-03-17');

INSERT INTO ai_models (model_name, model_version)
VALUES
    ('GPT', '4o'),
    ('GPT', '4.1'),
    ('Claude', '3.7'),
    ('Llama', '3.1'),
    ('DeepSeek', 'V3');

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

INSERT INTO generations (model_id, message_id, parameters, created_at)
VALUES
    (1, 2, '{"temperature": 0.7, "max_tokens": 200, "top_p": 0.9}', '2026-03-21 10:00:05'),
    (1, 4, '{"temperature": 0.5, "max_tokens": 300, "top_p": 0.95}', '2026-03-21 11:00:06');

-- Перевірка вставок

SELECT * FROM generations;