-- PostgreSQL database questmaker initialization

--create database db and connect to it, because it is impossible 
--to drop the database while there is a connection to it
CREATE DATABASE db;
\connect db;
--DROP DATABASE IF EXISTS questmaker;

CREATE DATABASE questmaker;
\connect questmaker;
drop db;

CREATE TABLE Author_statuses (
    status_id SERIAL PRIMARY KEY,
    status CHARACTER VARYING(100) NOT NULL
);

CREATE TABLE Authors (
    author_id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(100),
    login CHARACTER VARYING(100) NOT NULL,
    hash_password BYTEA NOT NULL,
    status_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES Author_statuses (status_id) ON DELETE CASCADE	
);

CREATE TABLE Quests (
    quest_id SERIAL PRIMARY KEY,
    title CHARACTER VARYING NOT NULL,
    author_id INTEGER NOT NULL FOREIGN KEY REFERENCES Authors(author_id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    key_word CHARACTER VARYING(100),
    tags TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    time_close TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    lead_time INTERVAL NOT NULL
);

CREATE TABLE Places (
    place_id SERIAL PRIMARY KEY,
    place_name CHARACTER VARYING NOT NULL,
    coord POINT NOT NULL,
    quest_id INTEGER NOT NULL FOREIGN KEY REFERENCES Quests (quest_id) ON DELETE CASCADE,
    description TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE,
    time_close TIMESTAMP WITHOUT TIME ZONE,
    points REAL NOT NULL,
    fine REAL NOT NULL,
    radius DOUBLE PRECISION NOT NULL
);

CREATE TABLE Directions (
    direction_id SERIAL PRIMARY KEY,
    cur_place_id INTEGER FOREIGN KEY REFERENCES Places (place_id) ON DELETE CASCADE,
    next_place_id INTEGER FOREIGN KEY REFERENCES Places (place_id) ON DELETE CASCADE,
    description TEXT,
);


CREATE TABLE Object_types (
    object_type_id SERIAL PRIMARY KEY,
    object_type CHARACTER VARYING NOT NULL
);

CREATE TABLE Files (
    file_id SERIAL PRIMARY KEY,
    type_of_object_id INTEGER NOT NULL FOREIGN KEY REFERENCES Object_types (object_type_id) ON DELETE CASCADE,
    --an implicit link
    object_id INTEGER NOT NULL, 
    url_for_file TEXT NOT NULL,
    type_of_file CHARACTER VARYING NOT NULL
);

CREATE TABLE Question_types (
    questions_type_id SERIAL PRIMARY KEY,
    questions_type CHARACTER VARYING NOT NULL
);

CREATE TABLE Questions (
    question_id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL FOREIGN KEY REFERENCES Places (place_id) ON DELETE CASCADE,
    question_TEXT TEXT NOT NULL,
    points REAL NOT NULL,
    fine REAL NOT NULL,
    type_id INTEGER NOT NULL FOREIGN KEY REFERENCES Questions_type (questions_type_id) ON DELETE CASCADE
);


CREATE TABLE Possible_answers (
    possible_ans_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES Questions (question_id) ON DELETE CASCADE,
    possible_ans_TEXT TEXT NOT NULL
);

CREATE TABLE Hints (
    hint_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES Questions (question_id) ON DELETE CASCADE,
    hint_TEXT TEXT NOT NULL,
    fine REAL NOT NULL
);


CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    telegram_id TEXT NOT NULL
);

CREATE TABLE History (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY REFERENCES Users (user_id) ON DELETE CASCADE,
    quest_id INTEGER NOT NULL FOREIGN KEY REFERENCES Quests(quest_id) ON DELETE CASCADE,
    is_finished BOOLEAN NOT NULL,
    last_place_id INTEGER FOREIGN KEY REFERENCES Places (place_id) ON DELETE CASCADE,
    final_score REAL NOT NULL
);


CREATE TABLE Answers (
    answer_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES Questions(question_id) ON DELETE CASCADE,
    answer_TEXT TEXT NOT NULL,
);


