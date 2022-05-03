-- PostgreSQL database questmaker initialization


DROP TABLE IF EXISTS statuses CASCADE;
CREATE TABLE statuses (
    status_id SERIAL PRIMARY KEY,
    status_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS authors CASCADE;
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    email CHARACTER VARYING(100) UNIQUE NOT NULL,
    name CHARACTER VARYING(100) NOT NULL,
    password VARCHAR(200) NOT NULL,
    status_id INTEGER NOT NULL REFERENCES statuses (status_id) ON DELETE RESTRICT,
    avatar_url TEXT
);

DROP TABLE IF EXISTS quests CASCADE;
CREATE TABLE quests (
    quest_id SERIAL PRIMARY KEY,
    title CHARACTER VARYING NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors (author_id) ON DELETE CASCADE,
    description TEXT,
    keyword VARCHAR(8),
    password CHARACTER VARYING(100),
    cover_url TEXT,
    time_open TIMESTAMP WITHOUT TIME ZONE,
    time_close TIMESTAMP WITHOUT TIME ZONE,
    lead_time INTERVAL,
    hidden BOOLEAN NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL
);

DROP TABLE IF EXISTS drafts;
CREATE TABLE drafts (
    draft_id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES authors (author_id) ON DELETE CASCADE,
    container BYTEA,
    quest_id INTEGER  DEFAULT NULL REFERENCES quests (quest_id)  ON DELETE CASCADE
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
    tag_name CHARACTER VARYING(100) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS quest_tags CASCADE;
CREATE TABLE quest_tags (
    quest_tag_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags (tag_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS file_types CASCADE;
CREATE TABLE file_types (
    f_type_id SERIAL PRIMARY KEY,
    f_type_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS files CASCADE;
CREATE TABLE files (
    f_id SERIAL PRIMARY KEY,
    url_for_file TEXT NOT NULL,
    f_type_id INTEGER NOT NULL REFERENCES file_types (f_type_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS quest_files CASCADE;
CREATE TABLE quest_files (
    entry_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS question_types CASCADE;
CREATE TABLE question_types (
    q_type_id SERIAL PRIMARY KEY,
    q_type_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS questions CASCADE;
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quests (quest_id) ON DELETE CASCADE,
    question_text TEXT,
    q_type_id INTEGER NOT NULL REFERENCES question_types (q_type_id) ON DELETE RESTRICT,
    pos_x INTEGER DEFAULT 0,
    pos_y INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS hints CASCADE;
CREATE TABLE hints (
    hint_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    hint_text TEXT NOT NULL,
    fine REAL NOT NULL DEFAULT 0.0
);

DROP TABLE IF EXISTS hint_files CASCADE;
CREATE TABLE hint_files (
    entry_id SERIAL PRIMARY KEY,
    hint_id INTEGER NOT NULL REFERENCES hints (hint_id) ON DELETE CASCADE,
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS answer_options CASCADE;
CREATE TABLE answer_options (
    option_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    points REAL NOT NULL DEFAULT 0.0,
    next_question_id INTEGER REFERENCES questions (question_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS movements CASCADE;
CREATE TABLE movements (
    movement_id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL REFERENCES places (place_id) ON DELETE RESTRICT,
    question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    next_question_id INTEGER NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS histories CASCADE;
CREATE TABLE histories (
    history_id SERIAL PRIMARY KEY,
    telegram_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL REFERENCES quests(quest_id) ON DELETE CASCADE,
    is_finished BOOLEAN NOT NULL,
    last_question_id INTEGER REFERENCES questions (question_id) ON DELETE SET NULL,
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
    f_id INTEGER NOT NULL REFERENCES files (f_id) ON DELETE RESTRICT
);

INSERT INTO statuses(status_id, status_name)
VALUES
    (0, 'author'),
    (1, 'moderator');

INSERT INTO file_types(f_type_id, f_type_name)
VALUES
    (0, 'image'),
    (1,'audio'),
    (2, 'video');

INSERT INTO question_types(q_type_id, q_type_name)
VALUES
    (0, 'open'),
    (1, 'choice'),
    (2, 'movement'),
    (3, 'start'),
    (4, 'end');

DROP VIEW IF EXISTS quests_catalog;
CREATE VIEW quests_catalog AS
        SELECT quest_id, title, author, description, keyword,
        1 * ratings.one_star_amount + 2 * ratings.two_star_amount +
        3 * ratings.three_star_amount + 4 * ratings.four_star_amount + 5 * ratings.five_star_amount AS rating,
        time_open, time_close, cover_url
        FROM quests
        JOIN authors USING (author_id)
        JOIN ratings USING (quest_id)
        WHERE NOT hidden AND published;
