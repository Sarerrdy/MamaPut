-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS user_roles;
CREATE TABLE user_roles (
\tid INTEGER NOT NULL, 
\tuser_id INTEGER NOT NULL, 
\trole_id INTEGER NOT NULL, 
\tPRIMARY KEY (id), 
\tFOREIGN KEY(user_id) REFERENCES users (user_id), 
\tFOREIGN KEY(role_id) REFERENCES roles (role_id)
);
INSERT INTO user_roles(id,user_id,role_id) VALUES(2,2,3),(12,1,1),(16,2,2),(17,3,3);