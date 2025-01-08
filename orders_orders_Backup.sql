-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
order_id INTEGER NOT NULL, 
total_price FLOAT NOT NULL, 
date_ordered DATETIME NOT NULL, 
expected_date_of_delivery DATETIME, 
status VARCHAR NOT NULL, 
user_id INTEGER, 
PRIMARY KEY (order_id), 
FOREIGN KEY(user_id) REFERENCES users (user_id)
);
INSERT INTO orders(order_id,total_price,date_ordered,expected_date_of_delivery,status,user_id) VALUES(1,800,'2024-12-17 08:52:55.632255','2024-12-17 10:52:55.633313','Processing',1),(2,2000,'2024-12-17 09:31:27.363631','2024-12-17 09:46:27.364829','Received',1),(3,1650,'2024-12-17 11:40:02.846508','2024-12-17 13:40:02.847547','Received',1),(4,600,'2024-12-17 12:04:55.336466','2024-12-17 17:04:55.337625','Processing',1),(5,1000,'2024-12-17 12:22:53.310977','2024-12-17 12:37:53.311818','Received',1),(6,1000,'2024-12-17 12:24:08.300778','2024-12-17 12:39:08.301407','Received',1),(7,2400,'2024-12-17 12:46:12.755692','2024-12-17 17:46:12.756932','Received',1),(8,3200,'2024-12-17 12:47:22.038386','2024-12-17 13:02:22.039218','Received',1);