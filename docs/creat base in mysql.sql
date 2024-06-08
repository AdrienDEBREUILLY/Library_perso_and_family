-- Création de la base de données
DROP DATABASE bibliotheque_perso_and_family;
CREATE DATABASE IF NOT EXISTS bibliotheque_perso_and_family;
USE bibliotheque_perso_and_family;

-- Création des tables et insertion des données initiales

-- Table user
CREATE TABLE IF NOT EXISTS user (
  id_user INT AUTO_INCREMENT NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE,
  username VARCHAR(30) NOT NULL,
  password VARCHAR(512) NOT NULL,
  email VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_user),
  UNIQUE (username, email)
);

--INSERT INTO user (username, password, email) VALUES
--('user1', 'password1', 'user1@email.com'),
--('user2', 'password2', 'user2@email.com');

DELIMITER //
CREATE TRIGGER update_user_updated_at
BEFORE UPDATE
ON user FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_book),
  UNIQUE (title, author)
);

--INSERT INTO book (title, author, publisher, publication_date, synopsis, language, cover_url) VALUES
--('Book 1', 'Author 1', 'Publisher 1', '2023-01-01', 'Synopsis for Book 1', 'English', 'cover1.jpg'),
--('Book 2', 'Author 2', 'Publisher 2', '2023-02-01', 'Synopsis for Book 2', 'English', 'cover2.jpg');

DELIMITER //
CREATE TRIGGER update_book_updated_at
BEFORE UPDATE
ON book FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER set_book_added_date
BEFORE INSERT ON book_list_book
FOR EACH ROW
BEGIN
  SET NEW.book_added_date = CURRENT_DATE;
END;
//
DELIMITER ;

-- Table book_list
CREATE TABLE IF NOT EXISTS book_list (
  id_book_list INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  user_id INT NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_book_list),
  FOREIGN KEY (user_id) REFERENCES user(id_user),
  UNIQUE (name, user_id)
);

--INSERT INTO book_list (name, user_id, description) VALUES
--('List 1', 1, 'Description for List 1'),
--('List 2', 2, 'Description for List 2');

DELIMITER //
CREATE TRIGGER update_book_list_updated_at
BEFORE UPDATE
ON book_list FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

-- Table book_list_book
CREATE TABLE IF NOT EXISTS book_list_book (
  book_id INT NOT NULL,
  book_list_id INT NOT NULL,
  book_added_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (book_id, book_list_id),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  FOREIGN KEY (book_list_id) REFERENCES book_list(id_book_list),
  UNIQUE (book_id, book_list_id)
);

--INSERT INTO book_list_book (book_id, book_list_id, book_added_date) VALUES
--(1, 1, '2023-01-15'),
--(2, 2, '2023-02-15');

DELIMITER //
CREATE TRIGGER update_book_list_book_updated_at
BEFORE UPDATE
ON book_list_book FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

-- Table serie
CREATE TABLE IF NOT EXISTS serie (
  id_serie INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_serie),
  UNIQUE (name)
);

--INSERT INTO serie (name, description) VALUES
--('Serie 1', 'Description for Serie 1'),
--('Serie 2', 'Description for Serie 2');

DELIMITER //
CREATE TRIGGER update_serie_updated_at
BEFORE UPDATE
ON serie FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

-- Table book_serie
CREATE TABLE IF NOT EXISTS book_serie (
  book_id INT NOT NULL,
  serie_id INT NOT NULL,
  number_in_serie INT NOT NULL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (book_id, serie_id, number_in_serie),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  FOREIGN KEY (serie_id) REFERENCES serie(id_serie),
  UNIQUE (book_id, serie_id, number_in_serie)
);

--INSERT INTO book_serie (book_id, serie_id, number_in_serie, notes) VALUES
--(1, 1, 1, 'Notes for Book 1 in Serie 1'),
--(2, 2, 1, 'Notes for Book 2 in Serie 2');

DELIMITER //
CREATE TRIGGER update_book_serie_updated_at
BEFORE UPDATE
ON book_serie FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

-- Table serie_part
CREATE TABLE IF NOT EXISTS serie_part (
  id_serie_part INT AUTO_INCREMENT NOT NULL,
  serie_id INT NOT NULL,
  part_name VARCHAR(50) NOT NULL,
  part_number INT NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_serie_part),
  FOREIGN KEY (serie_id) REFERENCES serie(id_serie),
  UNIQUE (serie_id, part_name, part_number)
);

--INSERT INTO serie_part (serie_id, part_name, part_number, description) VALUES
--(1, 'Part 1 of Serie 1', 1, 'Description of part 1 in Serie 1'),
--(2, 'Part 1 of Serie 2', 1, 'Description of part 1 in Serie 2');

DELIMITER //
CREATE TRIGGER update_serie_part_updated_at
BEFORE UPDATE
ON serie_part FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;

-- Table borrowed_book
CREATE TABLE IF NOT EXISTS borrowed_book (
  id_borrowed_book INT AUTO_INCREMENT NOT NULL,
  user_id INT NOT NULL,
  book_id INT NOT NULL,
  borrowed_date DATE NOT NULL,
  return_date DATE,
  returned_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  PRIMARY KEY (id_borrowed_book),
  FOREIGN KEY (user_id) REFERENCES user(id_user),
  FOREIGN KEY (book_id) REFERENCES book(id_book),
  UNIQUE (user_id, book_id, borrowed_date)
);

--INSERT INTO borrowed_book (user_id, book_id, borrowed_date, return_date, returned_date) VALUES
--(1, 1, '2023-01-01', '2023-01-15', '2023-01-10'),
--(2, 2, '2023-02-01', '2023-02-15', '2023-02-10');

DELIMITER //
CREATE TRIGGER update_borrowed_book_updated_at
BEFORE UPDATE
ON borrowed_book FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END;
//
DELIMITER ;