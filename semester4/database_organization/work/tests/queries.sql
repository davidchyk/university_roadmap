INSERT INTO restaurants (
    restaurant_id,
    restaurant_name,
    restaurant_cuisine,
    restaurant_address,
    restaurant_rating
) VALUES
(1, 'MacDonalds', 'American', 'Берестейський просп., 32, Київ, 02000', 3.9),
(2, 'Пузата Хата', 'Ukrainian', 'Берестейський просп., 24, Київ, 04116', 4.4),
(3, 'Сушія', 'Japanese', 'Берестейський просп., 26, Київ, 04116', 4.2);

INSERT INTO customers (
    customer_id,
    customer_full_name,
    customer_delivery_address,
    customer_payment_info
) VALUES
(1, 'Artem Davydchuk', 'вул. Академіка Янгеля, 20, Київ, 02000', 'Visa **** 1234'),
(2, 'Dmytro Dubrov', 'вул. Академіка Янгеля, 20, Київ, 02000', 'MasterCard **** 5678');

INSERT INTO couriers (
    courier_id,
    courier_full_name,
    courier_vehicle_type,
    courier_availability_status,
    courier_district
) VALUES
(1, 'Ivan Pedrenko', 'bicycle', 'available', 'Solomyanskyi'),
(2, 'Andriy Vovk', 'motorbike', 'busy', 'Solomyanskyi');

INSERT INTO orders (
    order_id,
    order_customer_id,
    order_restaurant_id,
    order_courier_id,
    order_time,
    order_delivery_time,
    order_status,
    order_total_amount
) VALUES
(1, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '20 minutes', 'created', 878.00),
(2, 2, 3, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '55 minutes', 'confirmed', 370.00);

INSERT INTO order_items (
    order_item_id,
    order_id,
    order_item_name,
    order_item_quantity,
    order_item_price
) VALUES
(1, 1, 'Double Big Tasty Menu', 2, 414.00),
(2, 1, 'Cheese sauce', 1, 50.00),
(3, 2, 'Philadelphia Roll', 1, 250.00),
(4, 2, 'Miso Soup', 1, 120.00);

--------------------------------------------------
-- INSERT

INSERT INTO customers (
    customer_id,
    customer_full_name,
    customer_delivery_address,
    customer_payment_info
) VALUES
(3, 'Maria Shevchenko', 'вул. Антоновича, 14, Київ, 02000', 'Visa **** 9876');

INSERT INTO order_items (
    order_item_id,
    order_id,
    order_item_name,
    order_item_quantity,
    order_item_price
) VALUES
(5, 2, 'Green Tea', 1, 45.00);

--------------------------------------------------
-- UPDATE

UPDATE couriers
SET courier_availability_status = 'available'
WHERE courier_id = 2;

UPDATE orders
SET order_status = 'delivered',
    order_delivery_time = CURRENT_TIMESTAMP
WHERE order_id = 2;

--------------------------------------------------
-- DELETE

DELETE FROM order_items
WHERE order_item_id = 5;

DELETE FROM customers
WHERE customer_id = 3;

--------------------------------------------------
-- SELECT

SELECT *
FROM couriers
WHERE courier_availability_status = 'available'
  AND courier_district = 'Solomyanskyi';

SELECT *
FROM orders
WHERE order_restaurant_id = 1
  AND DATE(order_time) = CURRENT_DATE;

--------------------------------------------------
-- Додаткові дані для кращої аналітики

INSERT INTO orders (
    order_id,
    order_customer_id,
    order_restaurant_id,
    order_courier_id,
    order_time,
    order_delivery_time,
    order_status,
    order_total_amount
) VALUES
(3, 1, 2, 1, CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days' + INTERVAL '35 minutes', 'delivered', 290.00),
(4, 2, 1, 2, CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days' + INTERVAL '25 minutes', 'delivered', 199.00),
(5, 1, 3, 2, CURRENT_TIMESTAMP - INTERVAL '1 day', NULL, 'cancelled', 430.00),
(6, 2, 2, 1, CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP - INTERVAL '10 days' + INTERVAL '40 minutes', 'delivered', 350.00);

INSERT INTO order_items (
    order_item_id,
    order_id,
    order_item_name,
    order_item_quantity,
    order_item_price
) VALUES
(6, 3, 'Борщ', 1, 120.00),
(7, 3, 'Вареники', 1, 170.00),
(8, 4, 'Big Mac', 1, 129.00),
(9, 4, 'Fries', 1, 70.00),
(10, 5, 'Set Philadelphia', 1, 430.00),
(11, 6, 'Котлета по-київськи', 1, 210.00),
(12, 6, 'Компот', 2, 70.00);

--------------------------------------------------
-- Analytical queries

-- 1. Обчислити загальний дохід за рестораном за місяць
SELECT
    r.restaurant_id,
    r.restaurant_name,
    DATE_TRUNC('month', o.order_time) AS month,
    SUM(o.order_total_amount) AS total_revenue
FROM orders o
JOIN restaurants r
    ON o.order_restaurant_id = r.restaurant_id
WHERE o.order_status = 'delivered'
GROUP BY
    r.restaurant_id,
    r.restaurant_name,
    DATE_TRUNC('month', o.order_time)
ORDER BY
    month,
    total_revenue DESC;

-- 2. Знайти топ-10 ресторанів з найвищим рейтингом та найбільшою кількістю замовлень
SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.restaurant_rating,
    COUNT(o.order_id) AS total_orders
FROM restaurants r
LEFT JOIN orders o
    ON o.order_restaurant_id = r.restaurant_id
GROUP BY
    r.restaurant_id,
    r.restaurant_name,
    r.restaurant_rating
ORDER BY
    r.restaurant_rating DESC,
    total_orders DESC
LIMIT 10;

-- 3. Обчислити середній час доставки за кур'єром
SELECT
    c.courier_id,
    c.courier_full_name,
    AVG(o.order_delivery_time - o.order_time) AS average_delivery_time
FROM couriers c
JOIN orders o
    ON o.order_courier_id = c.courier_id
WHERE o.order_status = 'delivered'
  AND o.order_delivery_time IS NOT NULL
GROUP BY
    c.courier_id,
    c.courier_full_name
ORDER BY
    average_delivery_time;

-- 4. Визначити кур'єрів з найбільшою кількістю скасованих доставок (CTE)
WITH cancelled_deliveries AS (
    SELECT
        c.courier_id,
        c.courier_full_name,
        COUNT(o.order_id) AS cancelled_orders_count
    FROM couriers c
    JOIN orders o
        ON o.order_courier_id = c.courier_id
    WHERE o.order_status = 'cancelled'
    GROUP BY
        c.courier_id,
        c.courier_full_name
)
SELECT
    courier_id,
    courier_full_name,
    cancelled_orders_count
FROM cancelled_deliveries
ORDER BY
    cancelled_orders_count DESC;