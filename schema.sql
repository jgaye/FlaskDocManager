DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user(username, password) VALUES ('Alice', 'flask1');
INSERT INTO user(username, password) VALUES ('Bob', 'flask2');
INSERT INTO user(username, password) VALUES ('Charly', 'flask3');