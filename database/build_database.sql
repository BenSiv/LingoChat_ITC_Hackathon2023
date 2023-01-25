/*
Creating new database to store information from LingoChat app.
*/

-- Initilizing database
CREATE DATABASE lingochat;

USE lingochat;

-- Initilizing tables
CREATE TABLE Users (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255),
    age int,
    email varchar(255),
    password varchar(255),
    photo varchar(255), -- url
    PRIMARY KEY (id)
);

CREATE TABLE Interests (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Users_Interests (
    id int NOT NULL AUTO_INCREMENT,
    user_id int,
    interests_id int,
    rating int,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (interests_id) REFERENCES Interests(id)
);

CREATE TABLE Chat_rooms (
    id int NOT NULL AUTO_INCREMENT,
    active tinyint,
    top_interest_id int,
    feature_vector int,
    PRIMARY KEY (id),
    FOREIGN KEY (top_interest_id) REFERENCES Interests(id)
);

CREATE TABLE User_chat (
    id int NOT NULL AUTO_INCREMENT,
    chat_id int,
    user_id int,
    join_timestamp date,
    leave_timestamp date,
    PRIMARY KEY (id),
    FOREIGN KEY (chat_id) REFERENCES Chat_rooms(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

SHOW TABLES;
