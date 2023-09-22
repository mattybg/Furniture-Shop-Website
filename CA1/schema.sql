DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);



DROP TABLE IF EXISTS products;

CREATE TABLE products 
(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image TEXT
);

INSERT INTO products (name, price, description, image)
VALUES
    ('Oak Chair', '109.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From the Oakie Doakie signature collection.', 'oakchair.jpg'),
   ('Oak Round Table', '309.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From the Oakie Doakie signature collection.', 'oakrtable.jpg'),
   ('Oak Drawer','229.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From the Oakie Doakie signature collection.', 'oakdrawer.jpg'),
   ('Oak Wardrobe', '289.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakwardrobe.jpg'),
   ('Oak TV Unit', '209.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oaktvunit.jpg'),
   ('Oak Cabinet', '189.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakcabinet.jpg'),
   ('Oak Dining Table', '459.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakdiningtable.jpg'),
   ('Oak Display Cabinet', '259.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakdisplaycabinet.jpg'),
   ('Oak Desk', '229.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From the Oakie Doakie signature collection.', 'oakdesk.jpg'),
   ('Oak Dining Chair', '159.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakdiningchair.jpg'),
   ('Oak Stool', '84.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From the Oakie Doakie signature collection.', 'oakstool.jpg'),
   ('Oak BedFrame', '319.99', 'Handcrafted, from our home to yours. Made with 100% Irish Oak. From Oakie Doakie newest collection', 'oakbedframe.jpg')
;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders 
(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id TEXT NOT NULL,
    total_price REAL NOT NULL,
    status TEXT
);


-- foreign key table link idea credit: https://www.youtube.com/watch?v=f7oYCzKuv-w
