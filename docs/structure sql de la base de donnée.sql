
CREATE TABLE IF NOT EXISTS users (
  username VARCHAR(30) UNIQUE NOT NULL, /*nom d'utilisateur*/
  password VARCHAR(512) NOT NULL, /*mot de passe de l'utilisateur (haché et salé pour des raisons de sécurité)*/
  email VARCHAR(50) UNIQUE NOT NULL, /*adresse email de l'utilisateur*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date d'inscription de l'utilisateur*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (username, email)
);

CREATE TABLE IF NOT EXISTS book (
  title VARCHAR(50) NOT NULL, /*titre du livre*/
  author VARCHAR(50) NOT NULL, /*auteur(s) du livre*/
  publisher VARCHAR(50), /*éditeur du livre*/
  publication_date DATE, /*date de publication du livre*/
  synopsis TEXT, /*résumé du livre*/
  language VARCHAR(15), /*langue du livre*/
  cover_url VARCHAR(255), /*image de couverture du livre (chemin d'accès vers l'image)*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date d'inscription du livre*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (title, author)
);

CREATE TABLE IF NOT EXISTS book_list (
  name VARCHAR(50) NOT NULL, /*titre/nom de la liste*/
  user_id INT NOT NULL, /*id de l'utilisateur qui à créer la liste*/
  description TEXT, /*description de la liste*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (name),
  FOREIGN KEY (user_id) REFERENCES users(username, email)
);

CREATE TABLE IF NOT EXISTS book_list_book (
  book_id INT NOT NULL, /*identifiant du livre (clé étrangère)*/
  book_list_id INT NOT NULL, /*identifiant de la liste (clé étrangère)*/
  book_added_date DATE, /*date d'ajout du livre dans la liste*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (book_id, book_list_id),
  FOREIGN KEY (book_id) REFERENCES book(title, author),
  FOREIGN KEY (book_list_id) REFERENCES book_list(name)
);

CREATE TABLE IF NOT EXISTS serie (
  name VARCHAR(50) NOT NULL, /*titre/name de la série*/
  description TEXT, /*description de la série*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS book_serie (
  book_id INT NOT NULL, /*identifiant du livre (clé étrangère)*/
  serie_id INT NOT NULL, /*identifiant de la série (clé étrangère)*/
  number_in_serie INT NOT NULL, /*position du livre dans la série*/
  notes TEXT, /*notes/description de la série de livre*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (book_id, serie_id, number_in_serie),
  FOREIGN KEY (book_id) REFERENCES book(title, author),
  FOREIGN KEY (serie_id) REFERENCES serie(name)
);

CREATE TABLE IF NOT EXISTS serie_part (
  serie_id INT NOT NULL, /*identifiant de la série (clé étrangère)*/
  part_name VARCHAR(50) NOT NULL, /*titre/name de la partie de la série*/
  part_number INT NOT NULL, /*numéro de la partie dans la série*/
  description TEXT, /*description des partie de la série*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (serie_id, part_name, part_number),
  FOREIGN KEY (serie_id) REFERENCES serie(name)
);

CREATE TABLE IF NOT EXISTS borrowed_book (
  id_borrowed_book INT AUTO_INCREMENT NOT NULL, /*identifiant unique de l'emprunt*/
  user_id INT NOT NULL, /*identifiant de l'utilisateur qui a emprunté le livre (clé étrangère)*/
  book_id INT NOT NULL, /*identifiant du livre emprunté (clé étrangère)*/
  borrowed_date DATE NOT NULL, /*date d'emprunt du livre*/
  return_date DATE, /*date de retour prévue du livre*/
  returned_date DATE, /*date de retour effective du livre (peut être null si le livre n'a pas encore été retourné)*/
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, /*date de création*/
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, /*date de mise à jour*/
  PRIMARY KEY (id_borrowed_book),
  FOREIGN KEY (user_id) REFERENCES users(username, email),
  FOREIGN KEY (book_id) REFERENCES book(title, author)
);
