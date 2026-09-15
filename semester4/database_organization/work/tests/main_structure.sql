CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR(255) NOT NULL,
    restaurant_cuisine VARCHAR(100) NOT NULL,
    restaurant_address TEXT NOT NULL,
    restaurant_rating NUMERIC(2,1) CHECK (restaurant_rating >= 0 AND restaurant_rating <= 5)
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_full_name VARCHAR(255) NOT NULL,
    customer_delivery_address TEXT NOT NULL,
    customer_payment_info TEXT NOT NULL
);

CREATE TABLE couriers (
    courier_id SERIAL PRIMARY KEY,
    courier_full_name VARCHAR(255) NOT NULL,
    courier_vehicle_type VARCHAR(50) NOT NULL,
    courier_availability_status VARCHAR(30) NOT NULL
        CHECK(courier_availability_status IN ('available', 'busy', 'offline')),
    courier_district VARCHAR(100) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    order_restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    order_courier_id INTEGER REFERENCES couriers(courier_id) ON DELETE SET NULL,
    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_delivery_time TIMESTAMP,
    order_status VARCHAR(30) NOT NULL
        CHECK(order_status IN ('created', 'confirmed', 'preparing', 'on_the_way', 'delivered', 'cancelled')),
    order_total_amount NUMERIC(10,2) NOT NULL CHECK (order_total_amount >= 0)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    order_item_name VARCHAR(255) NOT NULL,
    order_item_quantity INTEGER NOT NULL CHECK(order_item_quantity > 0),
    order_item_price NUMERIC(10,2) NOT NULL CHECK(order_item_price >= 0)
);