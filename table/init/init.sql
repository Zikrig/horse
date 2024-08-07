CREATE TABLE people (id int NOT NULL AUTO_INCREMENT, tg_person INT NOT NULL, name VARCHAR(50), phone VARCHAR(16), description VARCHAR(300), photo VARCHAR(100), PRIMARY KEY (id))
CREATE TABLE task(id int NOT NULL AUTO_INCREMENT, tg_person INT, date_of DATE, time_of TIME, descr_client VARCHAR(300), ready TINYINT(1), canceled TINYINT(1), PRIMARY KEY (id))
CREATE TABLE banned(id int NOT NULL AUTO_INCREMENT, tg_person INT, PRIMARY KEY (id))
CREATE TABLE admin(id int NOT NULL AUTO_INCREMENT, tg_person INT, PRIMARY KEY (id))