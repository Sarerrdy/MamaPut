-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS shipping_info;
CREATE TABLE shipping_info (
\tshipping_info_id INTEGER NOT NULL, 
\t"shipping_Method" VARCHAR NOT NULL, 
\tshipping_cost FLOAT NOT NULL, 
\tshipping_status VARCHAR NOT NULL, 
\tshipped_date DATETIME NOT NULL, 
\texpected_delivery_date DATETIME NOT NULL, 
\torder_id INTEGER, 
\taddress_id INTEGER, 
\tPRIMARY KEY (shipping_info_id), 
\tFOREIGN KEY(order_id) REFERENCES orders (order_id), 
\tFOREIGN KEY(address_id) REFERENCES addresses (address_id)
);
INSERT INTO shipping_info(shipping_info_id,shipping_Method,shipping_cost,shipping_status,shipped_date,expected_delivery_date,order_id,address_id) VALUES(1,'express',700,'Pending','2024-12-17 07:52:55','2024-12-17 10:52:55.633313',1,1),(2,'pickup',0,'Pending','2024-12-17 08:31:27','2024-12-17 09:46:27.364829',2,1),(3,'express',700,'Pending','2024-12-17 10:40:02','2024-12-17 13:40:02.847547',3,1),(4,'standard',500,'Pending','2024-12-17 11:04:55','2024-12-17 17:04:55.337625',4,1),(5,'pickup',0,'Pending','2024-12-17 11:22:53','2024-12-17 12:37:53.311818',5,1),(6,'pickup',0,'Pending','2024-12-17 11:24:08','2024-12-17 12:39:08.301407',6,1),(7,'standard',500,'Pending','2024-12-17 11:46:12','2024-12-17 17:46:12.756932',7,1),(8,'pickup',0,'Pending','2024-12-17 11:47:22','2024-12-17 13:02:22.039218',8,1);