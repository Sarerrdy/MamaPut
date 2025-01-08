-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
\trole_id INTEGER NOT NULL, 
\trole_name VARCHAR NOT NULL, 
\tPRIMARY KEY (role_id), 
\tUNIQUE (role_name)
);
INSERT INTO roles(role_id,role_name) VALUES(1,'SuperAdmin'),(2,'Admin'),(3,'User'),(4,'RestaurantManager'),(5,'Shipper');