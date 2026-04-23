-- Лабораторна робота №3
-- Тема: SQL Data Manipulation / OLTP
-- Перед запуском потрібно виконати lab2/db.sql

BEGIN;

-- 1. SELECT: отримати користувачів з України
SELECT
    user_id,
    user_name,
    email,
    country,
    created_at
FROM users
WHERE country = 'Ukraine'
ORDER BY created_at DESC;

-- 2. SELECT + JOIN: переглянути історію повідомлень у першому чаті
SELECT
    c.chat_id,
    c.title,
    m.message_id,
    m.role_m,
    m.content_m,
    m.created_at
FROM chats AS c
JOIN messages AS m ON m.chat_id = c.chat_id
WHERE c.chat_id = 1
ORDER BY m.created_at;

-- 3. SELECT + JOIN + WHERE: знайти вкладення розміром понад 50 KB
SELECT
    a.attachment_id,
    a.file_name,
    a.size_bytes,
    m.message_id,
    c.title AS chat_title
FROM attachments AS a
JOIN messages AS m ON m.message_id = a.message_id
JOIN chats AS c ON c.chat_id = m.chat_id
WHERE a.size_bytes > 50000
ORDER BY a.size_bytes DESC;

-- 4. INSERT: додати нового користувача, чат, повідомлення, відповідь моделі,
-- запис генерації та вкладення до користувацького повідомлення
WITH new_user AS (
    INSERT INTO users (first_name, second_name, user_name, email, country, created_at)
    VALUES ('Daria', 'Koval', 'daria_koval', 'daria.koval@gmail.com', 'Ukraine', '2026-04-23')
    RETURNING user_id
),
new_chat AS (
    INSERT INTO chats (owner_user_id, title, created_at)
    SELECT user_id, 'Normalization questions', '2026-04-23'
    FROM new_user
    RETURNING chat_id
),
user_msg AS (
    INSERT INTO messages (chat_id, role_m, content_m, created_at)
    SELECT
        chat_id,
        'user',
        'Can you explain database normalization?',
        '2026-04-23 12:00:00'
    FROM new_chat
    RETURNING message_id, chat_id
),
ai_msg AS (
    INSERT INTO messages (chat_id, role_m, content_m, created_at)
    SELECT
        chat_id,
        'ai_model',
        'Normalization reduces redundancy and update anomalies.',
        '2026-04-23 12:00:04'
    FROM user_msg
    RETURNING message_id
),
new_generation AS (
    INSERT INTO generations (model_id, message_id, parameters, created_at)
    SELECT
        2,
        message_id,
        '{"temperature": 0.6, "max_tokens": 180, "top_p": 0.9}',
        '2026-04-23 12:00:04'
    FROM ai_msg
    RETURNING generation_id
),
new_attachment AS (
    INSERT INTO attachments (message_id, file_name, size_bytes, path_a, uploaded_at)
    SELECT
        message_id,
        'normalization_request.txt',
        4096,
        '/files/normalization_request.txt',
        '2026-04-23 12:00:01'
    FROM user_msg
    RETURNING attachment_id
)
SELECT
    new_user.user_id,
    new_chat.chat_id,
    user_msg.message_id AS user_message_id,
    ai_msg.message_id AS ai_message_id,
    new_generation.generation_id,
    new_attachment.attachment_id
FROM new_user
JOIN new_chat ON TRUE
JOIN user_msg ON TRUE
JOIN ai_msg ON TRUE
JOIN new_generation ON TRUE
JOIN new_attachment ON TRUE;

-- 5. SELECT-перевірка: показати доданий діалог
SELECT
    u.user_name,
    c.title,
    m.role_m,
    m.content_m,
    g.parameters
FROM users AS u
JOIN chats AS c ON c.owner_user_id = u.user_id
JOIN messages AS m ON m.chat_id = c.chat_id
LEFT JOIN generations AS g ON g.message_id = m.message_id
WHERE u.user_name = 'daria_koval'
ORDER BY m.created_at;

-- 6. UPDATE: змінити назву створеного чату
UPDATE chats AS c
SET title = 'SQL normalization practice'
FROM users AS u
WHERE u.user_id = c.owner_user_id
  AND u.user_name = 'daria_koval'
  AND c.title = 'Normalization questions'
RETURNING c.chat_id, c.title;

-- 7. UPDATE JSONB: змінити параметр temperature у записі генерації
UPDATE generations AS g
SET parameters = jsonb_set(g.parameters, '{temperature}', '0.4'::jsonb)
FROM messages AS m
JOIN chats AS c ON c.chat_id = m.chat_id
JOIN users AS u ON u.user_id = c.owner_user_id
WHERE g.message_id = m.message_id
  AND u.user_name = 'daria_koval'
RETURNING g.generation_id, g.parameters;

-- 8. DELETE: безпечно видалити тимчасове вкладення, не видаляючи повідомлення
DELETE FROM attachments AS a
USING messages AS m
JOIN chats AS c ON c.chat_id = m.chat_id
JOIN users AS u ON u.user_id = c.owner_user_id
WHERE a.message_id = m.message_id
  AND u.user_name = 'daria_koval'
  AND a.file_name = 'normalization_request.txt'
RETURNING a.attachment_id, a.file_name;

-- 9. Фінальна перевірка кількості рядків у таблицях
SELECT 'users' AS table_name, COUNT(*) AS rows_count FROM users
UNION ALL
SELECT 'ai_models', COUNT(*) FROM ai_models
UNION ALL
SELECT 'chats', COUNT(*) FROM chats
UNION ALL
SELECT 'messages', COUNT(*) FROM messages
UNION ALL
SELECT 'attachments', COUNT(*) FROM attachments
UNION ALL
SELECT 'generations', COUNT(*) FROM generations
ORDER BY table_name;

COMMIT;
