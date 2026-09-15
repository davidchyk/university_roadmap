-- Лабораторна робота №5
-- Перетворення схеми lab2 до нормалізованого варіанта 3NF.
-- Скрипт розрахований на запуск після lab2/db.sql.

BEGIN;

-- 1. Винесення країн з users.country у довідник countries.
CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO countries (country_name)
SELECT DISTINCT country
FROM users
ORDER BY country;

ALTER TABLE users
ADD COLUMN country_id INTEGER;

UPDATE users AS u
SET country_id = c.country_id
FROM countries AS c
WHERE c.country_name = u.country;

ALTER TABLE users
ALTER COLUMN country_id SET NOT NULL;

ALTER TABLE users
ADD CONSTRAINT fk_users_country
FOREIGN KEY (country_id) REFERENCES countries(country_id);

ALTER TABLE users
DROP COLUMN country;

-- 2. Винесення сімейства моделі з ai_models.model_name у довідник.
CREATE TABLE ai_model_families (
    family_id SERIAL PRIMARY KEY,
    family_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO ai_model_families (family_name)
SELECT DISTINCT model_name
FROM ai_models
ORDER BY model_name;

ALTER TABLE ai_models
ADD COLUMN family_id INTEGER;

UPDATE ai_models AS am
SET family_id = f.family_id
FROM ai_model_families AS f
WHERE f.family_name = am.model_name;

ALTER TABLE ai_models
ALTER COLUMN family_id SET NOT NULL;

ALTER TABLE ai_models
ADD CONSTRAINT fk_ai_models_family
FOREIGN KEY (family_id) REFERENCES ai_model_families(family_id);

ALTER TABLE ai_models
ADD CONSTRAINT uq_ai_models_family_version
UNIQUE (family_id, model_version);

ALTER TABLE ai_models
DROP COLUMN model_name;

-- 3. Нормалізація JSONB parameters у generations.
CREATE TABLE generation_parameters (
    generation_id INTEGER NOT NULL REFERENCES generations(generation_id) ON DELETE CASCADE,
    parameter_name VARCHAR(40) NOT NULL,
    parameter_value NUMERIC(12, 4) NOT NULL,
    PRIMARY KEY (generation_id, parameter_name)
);

INSERT INTO generation_parameters (generation_id, parameter_name, parameter_value)
SELECT
    g.generation_id,
    p.key,
    p.value::numeric
FROM generations AS g
CROSS JOIN LATERAL jsonb_each_text(g.parameters) AS p(key, value);

ALTER TABLE generations
DROP COLUMN parameters;

COMMIT;
