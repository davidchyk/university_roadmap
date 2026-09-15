-- Add a new table for chat tags and a many-to-many assignment table.

CREATE TABLE chat_tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_tag_assignments (
    chat_id INTEGER NOT NULL REFERENCES chats(chat_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES chat_tags(tag_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chat_id, tag_id)
);
