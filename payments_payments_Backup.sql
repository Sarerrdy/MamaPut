-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
payment_id INTEGER NOT NULL, 
"payment_Method" VARCHAR NOT NULL, 
amount FLOAT NOT NULL, 
payment_status VARCHAR NOT NULL, 
payment_date DATETIME, 
reference VARCHAR NOT NULL, 
order_id INTEGER, 
PRIMARY KEY (payment_id), 
UNIQUE (reference), 
FOREIGN KEY(order_id) REFERENCES orders (order_id)
);
INSERT INTO payments(payment_id,payment_Method,amount,payment_status,payment_date,reference,order_id) VALUES(1,'paystack',1500,'success','2024-12-17 07:52:55','4e553305-1741-4ec1-8405-6ebb1b4c8167',1),(2,'payondelivery',2000,'Pending','2024-12-17 08:31:27','129a83f8-20cf-439b-a640-aa98bc61fa0c',2),(3,'payondelivery',2350,'Pending','2024-12-17 10:40:02','d19231e4-4231-4ba5-8e71-96d38493a7f0',3),(4,'paystack',1100,'success','2024-12-17 11:04:55','f53348e6-31cf-48ff-a891-f6210b2a5d92',4),(5,'payondelivery',1000,'Pending','2024-12-17 11:22:53','cb3860cd-1e99-4d3a-89a5-31d0c3194f3b',5),(6,'payondelivery',1000,'Pending','2024-12-17 11:24:08','1bd8c72b-7801-455e-8ce9-e39ea0c2cc32',6),(7,'payondelivery',2900,'Pending','2024-12-17 11:46:12','fde8b335-12ad-46aa-bd3b-9fafb4c668d7',7),(8,'paystack',3200,'success','2024-12-17 11:47:22','3eaa7076-0dbe-4641-ad2a-641d119b460d',8);