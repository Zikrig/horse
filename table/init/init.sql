CREATE TABLE people (id SERIAL PRIMARY KEY, tg_person INT, name VARCHAR(50), phone VARCHAR(16), description VARCHAR(300), photo VARCHAR(100));
CREATE TABLE task(id SERIAL PRIMARY KEY, tg_person INT, date_of DATE, time_of TIME, descr_client VARCHAR(300), ready BOOL, canceled BOOL);
CREATE TABLE banned(id SERIAL PRIMARY KEY, tg_person INT);
CREATE TABLE admin(id SERIAL PRIMARY KEY, tg_person INT);
