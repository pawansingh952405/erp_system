CREATE TABLE Vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    rating NUMERIC(2, 1)
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    stock_level INT DEFAULT 0
);

CREATE TABLE PurchaseOrders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR(100) UNIQUE NOT NULL,
    vendor_id INT REFERENCES Vendors(id),
    total_amount NUMERIC(12, 2) DEFAULT 0.00,
    status VARCHAR(50) DEFAULT 'Draft'
);

CREATE TABLE PurchaseOrderItems (
    id SERIAL PRIMARY KEY,
    po_id INT REFERENCES PurchaseOrders(id),
    product_id INT REFERENCES Products(id),
    quantity INT NOT NULL,
    price_at_purchase NUMERIC(10, 2) NOT NULL
);
INSERT INTO vendors (name, contact, rating) 
VALUES ('IV Innovations Pvt Ltd', 'contact@ivinnovations.com', 5.0);

INSERT INTO Vendors (name, contact, rating) VALUES ('Global Supplies Ltd', '999-000-111', 4.5);





INSERT INTO products (name, sku, unit_price, stock_level) 
VALUES 
('Gaming Laptop', 'LAP-001', 1200.00, 10),
('Wireless Mouse', 'MOU-002', 25.50, 50),
('Mechanical Keyboard', 'KEY-003', 75.00, 20);