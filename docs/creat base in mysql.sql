-- Création de la base de données
CREATE DATABASE IF NOT EXISTS bibliotheque_personnelle;
USE bibliotheque_personnelle;

-- Création des tables et insertion des données initiales

-- Table users
CREATE TABLE IF NOT EXISTS users (
  id_users INT AUTO_INCREMENT NOT NULL,
  username VARCHAR(30) UNIQUE NOT NULL,
  password VARCHAR(512) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_users)
  UNIQUE (username, email)
);

INSERT INTO users (username, password, email) VALUES
('user1', 'password1', 'user1@email.com'),
('user2', 'password2', 'user2@email.com');

-- Table book
CREATE TABLE IF NOT EXISTS book (
  id_book INT AUTO_INCREMENT NOT NULL,
  title VARCHAR(50) NOT NULL,
  author VARCHAR(50) NOT NULL,
  publisher VARCHAR(50),
  publication_date DATE,
  synopsis TEXT,
  language VARCHAR(15),
  cover_url VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_book),
  UNIQUE (title, author)
);

INSERT INTO book (title, author, publisher, publication_date, synopsis, language, cover_url) VALUES
('Book 1', 'Author 1', 'Publisher 1', '2023-01-01', 'Synopsis for Book 1', 'English', 'cover1.jpg'),
('Book 2', 'Author 2', 'Publisher 2', '2023-02-01', 'Synopsis for Book 2', 'English', 'cover2.jpg');

-- Table book_list
CREATE TABLE IF NOT EXISTS book_list (
  id_book_list INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  user_id INT NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_book_list),
  FOREIGN KEY (user_id) REFERENCES users(id_users),
  UNIQUE (name, user_id)
);

INSERT INTO book_list (name, user_id, description) VALUES
('List 1', 1, 'Description for List 1'),
('List 2', 2, 'Description for List 2');

-- Table book_list_book
CREATE TABLE IF NOT EXISTS book_list_book (
  book_id INT NOT NULL,
  book_list_id INT NOT NULL,
  book_added_date DATE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (book_id, book_list_id),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  FOREIGN KEY (book_list_id) REFERENCES book_list(id_book_list)
  UNIQUE (book_id, book_list_id)
);

INSERT INTO book_list_book (book_id, book_list_id, book_added_date) VALUES
(1, 1, '2023-01-15'),
(2, 2, '2023-02-15');

-- Table serie
CREATE TABLE IF NOT EXISTS serie (
  id_serie INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_serie),
  UNIQUE (name)
);

INSERT INTO serie (name, description) VALUES
('Serie 1', 'Description for Serie 1'),
('Serie 2', 'Description for Serie 2');

-- Table book_serie
CREATE TABLE IF NOT EXISTS book_serie (
  book_id INT NOT NULL,
  serie_id INT NOT NULL,
  number_in_serie INT NOT NULL,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (book_id, serie_id, number_in_serie),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  FOREIGN KEY (serie_id) REFERENCES serie(id_serie),
  UNIQUE (book_id, serie_id, number_in_serie)
);

INSERT INTO book_serie (book_id, serie_id, number_in_serie, notes) VALUES
(1, 1, 1, 'Notes for Book 1 in Serie 1'),
(2, 2, 1, 'Notes for Book 2 in Serie 2');

-- Table serie_part
CREATE TABLE IF NOT EXISTS serie_part (
  id_serie_part INT AUTO_INCREMENT NOT NULL,
  serie_id INT NOT NULL,
  part_name VARCHAR(50) NOT NULL,
  part_number INT NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_serie_part),
  FOREIGN KEY (serie_id) REFERENCES serie(id_serie),
  UNIQUE (serie_id, part_name, part_number)
);

INSERT INTO serie_part (serie_id, part_name, part_number, description) VALUES
(1, 'Part 1 of Serie 1', 1, 'Description of part 1 in Serie 1'),
(2, 'Part 1 of Serie 2', 1, 'Description of part 1 in Serie 2');

-- Table borrowed_book
CREATE TABLE IF NOT EXISTS borrowed_book (
  id_borrowed_book INT AUTO_INCREMENT NOT NULL,
  user_id INT NOT NULL,
  book_id INT NOT NULL,
  borrowed_date DATE NOT NULL,
  return_date DATE,
  returned_date DATE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_borrowed_book),
  FOREIGN KEY (user_id) REFERENCES users(id_users),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  UNIQUE (user_id, book_id, borrowed_date)
);

INSERT INTO borrowed_book (user_id, book_id, borrowed_date, return_date, returned_date) VALUES
(1, 1, '2023-01-01', '2023-01-15', '2023-01-10'),
(2, 2, '2023-02-01', '2023-02-15', '2023-02-10');