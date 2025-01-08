-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS addresses;
CREATE TABLE addresses (
address_id INTEGER NOT NULL, 
address VARCHAR NOT NULL, 
town VARCHAR NOT NULL, 
state VARCHAR NOT NULL, 
lga VARCHAR NOT NULL, 
landmark VARCHAR, 
user_id INTEGER, 
PRIMARY KEY (address_id), 
FOREIGN KEY(user_id) REFERENCES users (user_id)
);
INSERT INTO addresses(address_id,address,town,state,lga,landmark,user_id) VALUES(1,'Odili road','Port Harcourt','Rivers','Port Harcourt','by Aeroplan',1),(2,'13 Town Hall road, Woji','Portharourt','Rivers','Port Harcourt','',2),(3,'Stadium road','Portharourt','Rivers','Port Harcourt','',3);