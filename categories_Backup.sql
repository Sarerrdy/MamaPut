-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
category_id INTEGER NOT NULL, 
name VARCHAR NOT NULL, 
category_url VARCHAR NOT NULL, 
PRIMARY KEY (category_id)
);
INSERT INTO categories(category_id,name,category_url) VALUES(1,'Soups','/images/soups-1734384944246.png'),(2,'Fufu','/images/fufu-1734385039117.png'),(3,'Others','/images/others-1734385069577.png'),(4,'Proteins','/images/proteins-1734385101211.png'),(5,'Rice','/images/rice-1734385126433.png');