-- PostgreSQL database questmaker initialization


--CREATE DATABASE questmaker;
--\connect questmaker;

DROP  TABLE IF EXISTS statuses CASCADE;
CREATE TABLE statuses (
    status_id SERIAL PRIMARY KEY,
    status CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS authors CASCADE;
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(100)UNIQUE NOT NULL,
    name CHARACTER VARYING(100)  NOT NULL,
    password BYTEA NOT NULL,
    status_id INTEGER NOT NULL REFERENCES statuses (status_id) ON DELETE CASCADE,
    avatar_url TEXT
);

DROP TABLE IF EXISTS quests CASCADE; 
CREATE TABLE quests (
    quest_id SERIAL PRIMARY KEY,
    title CHARACTER VARYING NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors (author_id) ON DELETE CASCADE,
    description TEXT,
    password CHARACTER VARYING(100),
    cover_url TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE,
    time_close TIMESTAMP WITHOUT TIME ZONE,
    lead_time INTERVAL NOT NULL,
    hidden BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS places CASCADE; 
CREATE TABLE places (
    place_id SERIAL PRIMARY KEY,
    coords POINT NOT NULL,
    time_open TIMESTAMP WITHOUT TIME ZONE,
    time_close TIMESTAMP WITHOUT TIME ZONE,
    radius DOUBLE PRECISION NOT NULL
);

DROP TABLE IF EXISTS tags CASCADE;
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    tag_name CHARACTER VARYING(100) NOT NULL
);

DROP TABLE IF EXISTS file_types CASCADE;
CREATE TABLE file_types (
    file_type_id SERIAL PRIMARY KEY,
	q_type_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS files CASCADE; 
CREATE TABLE files (
    f_id SERIAL PRIMARY KEY, 
    url_for_file TEXT NOT NULL,
    file_type_id INTEGER NOT NULL REFERENCES file_types (file_type_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS quest_files CASCADE;
CREATE TABLE quest_files (
    entry_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS questions_types CASCADE;
CREATE TABLE questions_types (
    q_type_id SERIAL PRIMARY KEY,
	q_type_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS questions CASCADE; 
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    question_text TEXT,
    q_type_id INTEGER NOT NULL REFERENCES questions_types (q_type_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS hints CASCADE;
CREATE TABLE hints (
    hint_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL  REFERENCES questions (question_id) ON DELETE CASCADE,
    hint_text TEXT NOT NULL,
    fine REAL NOT NULL DEFAULT 0.0
);

DROP TABLE IF EXISTS hint_files CASCADE;
CREATE TABLE hint_files (
    entry_id SERIAL PRIMARY KEY,
    hint_id INTEGER NOT NULL REFERENCES hints (hint_id) ON DELETE CASCADE,
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS answer_options CASCADE; 
CREATE TABLE answer_options(
    option_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
	points REAL NOT NULL DEFAULT 0.0,
	next_question_id INTEGER REFERENCES questions (question_id)ON DELETE CASCADE
);

DROP TABLE IF EXISTS movements CASCADE; 
CREATE TABLE movements (
    movement_id SERIAL PRIMARY KEY,
    place_id INTEGER REFERENCES places (place_id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
	next_question_id INTEGER REFERENCES questions (question_id)ON DELETE CASCADE
);

DROP TABLE IF EXISTS histories CASCADE;
CREATE TABLE histories (
    history_id SERIAL PRIMARY KEY,
    telegram_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL REFERENCES quests(quest_id) ON DELETE CASCADE,
    is_finished BOOLEAN NOT NULL,
    last_question_id INTEGER REFERENCES questions (question_id) ON DELETE CASCADE,
    final_score REAL NOT NULL DEFAULT 0.0
);

DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL UNIQUE REFERENCES quests (quest_id) ON DELETE CASCADE,
    one_star_amount INTEGER NOT NULL DEFAULT 0,
	two_star_amount INTEGER NOT NULL DEFAULT 0,
	three_star_amount INTEGER NOT NULL DEFAULT 0,
	four_star_amount INTEGER NOT NULL DEFAULT 0,
	five_star_amount INTEGER NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS question_files CASCADE;
CREATE TABLE question_files (
    entry_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE CASCADE
);
