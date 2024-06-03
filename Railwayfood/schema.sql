
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);


INSERT INTO products (name, price) VALUES ('Product 1', 10.99);
INSERT INTO products (name, price) VALUES ('Product 2', 20.49);
INSERT INTO products (name, price) VALUES ('Product 3', 15.79);


CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
