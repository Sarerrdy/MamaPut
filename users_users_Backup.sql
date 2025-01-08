-- Database Client dump 8.0.9
-- Host: 127.0.0.1 Database: null

DROP TABLE IF EXISTS users;
CREATE TABLE users (
\tuser_id INTEGER NOT NULL, 
\ttitle VARCHAR NOT NULL, 
\tfirst_name VARCHAR NOT NULL, 
\tlast_name VARCHAR NOT NULL, 
\tgender VARCHAR NOT NULL, 
\temail VARCHAR NOT NULL, 
\tpassword VARCHAR NOT NULL, 
\tphone INTEGER NOT NULL, 
\tjoin_date DATETIME, 
\tuser_url VARCHAR, 
\tPRIMARY KEY (user_id)
);
INSERT INTO users(user_id,title,first_name,last_name,gender,email,password,phone,join_date,user_url) VALUES(1,'mr','Edmond','Ina','male','sarerrdy4live@live.co.uk','scrypt:32768:8:1$5qIBtDo9h71GWbbm$5de9817ea4daf25494bb47d34bed727f5c2421b83cff1a2cbfe8a442cf63f5b73e353f2dd46ac2dc6dc64c04057586fbdc25c1d701fa4c777b9b773cf9cca4ea',7038745740,'2024-12-17 00:51:11.710609',''),(2,'Mr','Sar','Errdy','male','sarerrdy4live@gmail.com','scrypt:32768:8:1$oy5NTIA2brOhCECL$9b558632417384747a76351f1ccbf03d83b27a9ad0d5d3ba749de1d678c4b76a013fb53a61ada7ba5d387605806e0f3d7733f816cad97bc4431b999b68295efd',7038745740,'2024-12-19 21:19:40.955256',''),(3,'mrs','Nneka','Agwu','female','nnekandubuisiagwu@gmail.com','scrypt:32768:8:1$VAe5S1yjPxn7MONI$35d548685fd2f618a7b5f7410871a7820752f7d5387842ae94d4130cee22f7b89c03940f4b2e13dd01690e64b97362b6b8334ea538c4ad167664d20a04d28101',8039340390,'2024-12-21 03:35:30.285455','');