-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
review_id INTEGER NOT NULL, 
menu_id INTEGER NOT NULL, 
user_id INTEGER NOT NULL, 
rating INTEGER NOT NULL, 
review VARCHAR(500),
user_names VARCHAR(500), 
created_at DATETIME, 
PRIMARY KEY (review_id), 
FOREIGN KEY(menu_id) REFERENCES menus (menu_id), 
FOREIGN KEY(user_id) REFERENCES users (user_id)
);
INSERT INTO reviews(review_id,menu_id,user_id,rating,review,created_at) VALUES(1,1,1,5,'tetst menails llllllllllllllllllllllllllll updaaaaaaaaaaaaaaaatee','2025-01-07 12:18:37.135342'),(2,2,1,5,'do you wanna see my ypdate?','2025-01-07 12:21:25.035043'),(3,3,3,5,'','2025-01-07 12:35:06.360635'),(4,2,3,5,'sweet mama meals','2025-01-07 12:36:45.494551'),(5,1,3,1,'worse ever','2025-01-07 12:37:26.664050'),(6,4,3,5,'testtttt','2025-01-07 12:48:23.749289'),(7,8,3,4,'','2025-01-07 14:06:05.319104'),(8,1,2,4,'i so much love afang','2025-01-07 14:32:55.905359'),(9,2,2,2,'','2025-01-07 14:39:00.338945');