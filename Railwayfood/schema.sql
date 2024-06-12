
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);


INSERT INTO products (name, price) VALUES ('Egg&Slice meat Sandwhich', 15);
INSERT INTO products (name, price) VALUES ('Wanpaku Sandwhich', 12);
INSERT INTO products (name, price) VALUES ('Croissant Egg&Meat', 16);
INSERT INTO products (name, price) VALUES ('Ice cream toast berries', 11);
INSERT INTO products (name, price) VALUES ('Shrimp alfredo', 11);
INSERT INTO products (name, price) VALUES ('Rice&Curry prawn', 17.50);
INSERT INTO products (name, price) VALUES ('Garlic bread bits', 19);
INSERT INTO products (name, price) VALUES ('Honey BBQ boneless Chicken', 19);
INSERT INTO products (name, price) VALUES ('Garlic butter Steak&Potatoes skillet', 20);
INSERT INTO products (name, price) VALUES ('Farfalle with Mushrooms&Caramalized Onions', 18.50);
INSERT INTO products (name, price) VALUES ('Herby lemon Skewers', 12);
INSERT INTO products (name, price) VALUES ('Futomaki fat sushi', 13);


CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);