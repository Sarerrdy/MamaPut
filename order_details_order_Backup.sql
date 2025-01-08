-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS order_details;
CREATE TABLE order_details (
order_details_id INTEGER NOT NULL, 
quantity INTEGER NOT NULL, 
discount FLOAT, 
price FLOAT NOT NULL, 
menu_id INTEGER, 
order_id INTEGER, 
PRIMARY KEY (order_details_id), 
FOREIGN KEY(menu_id) REFERENCES menus (menu_id), 
FOREIGN KEY(order_id) REFERENCES orders (order_id)
);
INSERT INTO order_details(order_details_id,quantity,discount,price,menu_id,order_id) VALUES(1,1,0,800,3,1),(2,3,0,500,1,2),(3,1,0,500,2,2),(4,1,0,250,4,3),(5,1,0,800,3,3),(6,1,0,600,5,3),(7,1,0,600,5,4),(8,2,0,500,1,5),(9,2,0,500,1,6),(10,4,0,600,5,7),(11,4,0,800,3,8);