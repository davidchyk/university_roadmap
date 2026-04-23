-- Лабораторна робота №4
-- Тема: Analytical SQL Queries / OLAP
-- Перед запуском рекомендовано виконати lab2/db.sql і lab3/lab3_dml.sql

-- 1. Агрегація: кількість повідомлень за ролями
SELECT
    role_m,
    COUNT(*) AS messages_count
FROM messages
GROUP BY role_m
ORDER BY role_m;

-- 2. Агрегація + GROUP BY: кількість чатів і повідомлень за країнами
SELECT
    u.country,
    COUNT(DISTINCT c.chat_id) AS chats_count,
    COUNT(m.message_id) AS messages_count,
    ROUND(COUNT(m.message_id)::numeric / NULLIF(COUNT(DISTINCT c.chat_id), 0), 2) AS avg_messages_per_chat
FROM users AS u
LEFT JOIN chats AS c ON c.owner_user_id = u.user_id
LEFT JOIN messages AS m ON m.chat_id = c.chat_id
GROUP BY u.country
ORDER BY messages_count DESC, u.country;

-- 3. Агрегація + HAVING: статистика вкладень тільки для чатів, де вони є
SELECT
    c.chat_id,
    c.title,
    COUNT(a.attachment_id) AS attachments_count,
    COALESCE(SUM(a.size_bytes), 0) AS total_attachment_bytes,
    ROUND(AVG(a.size_bytes)::numeric, 2) AS avg_attachment_bytes,
    MIN(a.size_bytes) AS min_attachment_bytes,
    MAX(a.size_bytes) AS max_attachment_bytes
FROM chats AS c
LEFT JOIN messages AS m ON m.chat_id = c.chat_id
LEFT JOIN attachments AS a ON a.message_id = m.message_id
GROUP BY c.chat_id, c.title
HAVING COUNT(a.attachment_id) > 0
ORDER BY total_attachment_bytes DESC;

-- 4. Агрегація JSONB-параметрів: кількість генерацій та середня temperature за моделями
SELECT
    am.model_name,
    am.model_version,
    COUNT(g.generation_id) AS generation_count,
    ROUND(AVG((g.parameters ->> 'temperature')::numeric), 2) AS avg_temperature,
    MAX((g.parameters ->> 'max_tokens')::integer) AS max_tokens_limit
FROM ai_models AS am
LEFT JOIN generations AS g ON g.model_id = am.model_id
GROUP BY am.model_id, am.model_name, am.model_version
HAVING COUNT(g.generation_id) > 0
ORDER BY generation_count DESC, am.model_name, am.model_version;

-- 5. INNER JOIN: повна історія повідомлень з власником чату
SELECT
    u.user_name,
    c.title AS chat_title,
    m.role_m,
    m.content_m,
    m.created_at
FROM users AS u
INNER JOIN chats AS c ON c.owner_user_id = u.user_id
INNER JOIN messages AS m ON m.chat_id = c.chat_id
ORDER BY c.chat_id, m.created_at;

-- 6. LEFT JOIN: всі користувачі, включно з тими, хто ще не має чатів
SELECT
    u.user_id,
    u.user_name,
    COALESCE(c.title, 'no chat') AS chat_title,
    c.created_at AS chat_created_at
FROM users AS u
LEFT JOIN chats AS c ON c.owner_user_id = u.user_id
ORDER BY u.user_id, c.chat_id;

-- 7. FULL JOIN: моделі та пов'язані генерації, включно з моделями без генерацій
SELECT
    am.model_id,
    am.model_name,
    am.model_version,
    g.generation_id,
    g.message_id
FROM ai_models AS am
FULL JOIN generations AS g ON g.model_id = am.model_id
ORDER BY am.model_id NULLS LAST, g.generation_id;

-- 8. Підзапит у SELECT: час останнього повідомлення та кількість повідомлень у кожному чаті
SELECT
    c.chat_id,
    c.title,
    (
        SELECT MAX(m.created_at)
        FROM messages AS m
        WHERE m.chat_id = c.chat_id
    ) AS last_message_at,
    (
        SELECT COUNT(*)
        FROM messages AS m
        WHERE m.chat_id = c.chat_id
    ) AS message_count
FROM chats AS c
ORDER BY c.chat_id;

-- 9. Підзапит у WHERE EXISTS: чати, де є відповідь моделі сімейства GPT
SELECT
    c.chat_id,
    c.title
FROM chats AS c
WHERE EXISTS (
    SELECT 1
    FROM messages AS m
    JOIN generations AS g ON g.message_id = m.message_id
    JOIN ai_models AS am ON am.model_id = g.model_id
    WHERE m.chat_id = c.chat_id
      AND am.model_name = 'GPT'
)
ORDER BY c.chat_id;

-- 10. Підзапит у HAVING: користувачі, які мають повідомлень більше за середнє по користувачах
SELECT
    u.user_id,
    u.user_name,
    COUNT(m.message_id) AS message_count
FROM users AS u
JOIN chats AS c ON c.owner_user_id = u.user_id
JOIN messages AS m ON m.chat_id = c.chat_id
GROUP BY u.user_id, u.user_name
HAVING COUNT(m.message_id) > (
    SELECT AVG(per_user.message_count)
    FROM (
        SELECT COUNT(m2.message_id) AS message_count
        FROM users AS u2
        LEFT JOIN chats AS c2 ON c2.owner_user_id = u2.user_id
        LEFT JOIN messages AS m2 ON m2.chat_id = c2.chat_id
        GROUP BY u2.user_id
    ) AS per_user
)
ORDER BY message_count DESC, u.user_name;
