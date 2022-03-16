/*PostgreSQL database questmaker initialization */

DROP TABLE IF EXISTS author_statuses;
CREATE TABLE author_statuses (
    status_id SERIAL PRIMARY KEY,
    status CHARACTER VARYING(100) NOT NULL
);

DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(100),
    login CHARACTER VARYING(100) NOT NULL,
    hash_password BYTEA NOT NULL,
    status_id INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES author_statuses (status_id) ON DELETE CASCADE	
);

DROP TABLE IF EXISTS quests; 
CREATE TABLE quests (
    quest_id SERIAL PRIMARY KEY,
    title CHARACTER VARYING NOT NULL,
    author_id INTEGER NOT NULL FOREIGN KEY REFERENCES authors (author_id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    key_word CHARACTER VARYING(100),
    tags TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    time_close TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    lead_time INTERVAL NOT NULL
);

DROP TABLE IF EXISTS places; 
CREATE TABLE places (
    place_id SERIAL PRIMARY KEY,
    place_name CHARACTER VARYING NOT NULL,
    coord POINT,
    quest_id INTEGER NOT NULL FOREIGN KEY REFERENCES quests (quest_id) ON DELETE CASCADE,
    description TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE,
    time_close TIMESTAMP WITHOUT TIME ZONE,
    points REAL NOT NULL,
    fine REAL NOT NULL,
    radius DOUBLE PRECISION
);

DROP TABLE IF EXISTS directions; 
CREATE TABLE directions (
    direction_id SERIAL PRIMARY KEY,
    cur_place_id INTEGER FOREIGN KEY REFERENCES places (place_id) ON DELETE CASCADE,
    next_place_id INTEGER FOREIGN KEY REFERENCES places (place_id) ON DELETE CASCADE,
    description TEXT,
);

DROP TABLE IF EXISTS object_types; 
CREATE TABLE object_types (
    object_type_id SERIAL PRIMARY KEY,
    object_type CHARACTER VARYING NOT NULL
);

DROP TABLE IF EXISTS files; 
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    type_of_object_id INTEGER NOT NULL FOREIGN KEY REFERENCES object_types (object_type_id) ON DELETE CASCADE,
    --an implicit link
    object_id INTEGER NOT NULL, 
    url_for_file TEXT NOT NULL,
    type_of_file CHARACTER VARYING NOT NULL
);

DROP TABLE IF EXISTS question_types; 
CREATE TABLE question_types (
    questions_type_id SERIAL PRIMARY KEY,
    questions_type CHARACTER VARYING NOT NULL
);

DROP TABLE IF EXISTS questions; 
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL FOREIGN KEY REFERENCES places (place_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    points REAL NOT NULL,
    fine REAL NOT NULL,
    type_id INTEGER NOT NULL FOREIGN KEY REFERENCES questions_type (questions_type_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS possible_answers; 
CREATE TABLE possible_answers (
    possible_ans_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES questions (question_id) ON DELETE CASCADE,
    possible_ans_text TEXT NOT NULL
);

DROP TABLE IF EXISTS hints;
CREATE TABLE hints (
    hint_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES questions (question_id) ON DELETE CASCADE,
    hint_text TEXT NOT NULL,
    fine REAL NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    telegram_id TEXT NOT NULL
);

DROP TABLE IF EXISTS history;
CREATE TABLE history (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY REFERENCES users (user_id) ON DELETE CASCADE,
    quest_id INTEGER NOT NULL FOREIGN KEY REFERENCES quests (quest_id) ON DELETE CASCADE,
    is_finished BOOLEAN NOT NULL,
    last_place_id INTEGER FOREIGN KEY REFERENCES places (place_id) ON DELETE CASCADE,
    final_score REAL NOT NULL
);

DROP TABLE IF EXISTS answers;
CREATE TABLE answers (
    answer_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL FOREIGN KEY REFERENCES questions (question_id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
);


