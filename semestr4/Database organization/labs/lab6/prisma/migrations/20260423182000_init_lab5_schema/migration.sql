-- Initial schema imported from lab5 normalized design.

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
