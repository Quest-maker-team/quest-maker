DROP TABLE IF EXISTS status CASCADE;
CREATE TABLE status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS block_type CASCADE;
CREATE TABLE block_type (
    block_type_id SERIAL PRIMARY KEY,
    block_type_name VARCHAR(50) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS media_type CASCADE;
CREATE TABLE media_type (
    media_type_id SERIAL PRIMARY KEY,
    media_type_name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO status(status_id, status_name)
VALUES
    (0, 'author'),
    (1, 'moderator');

INSERT INTO block_type(block_type_id, block_type_name)
VALUES
    (0, 'start_block'),
    (1, 'open_question'),
	(2, 'choice_question'),
    (3, 'movement'),
    (4, 'message'),
    (5, 'end_block');

INSERT INTO media_type(media_type_id, media_type_name)
VALUES
    (0, 'image'),
    (1, 'audio'),
    (2, 'video');

DROP TABLE IF EXISTS author CASCADE;
CREATE TABLE author (
    author_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(200) NOT NULL,
	avatar_path TEXT DEFAULT NULL,
    status_id INTEGER NOT NULL REFERENCES status (status_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS quest CASCADE;
CREATE TABLE quest (
    quest_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES author (author_id) ON DELETE CASCADE,
    description TEXT DEFAULT NULL,
    keyword VARCHAR(8) UNIQUE NOT NULL,
    password VARCHAR(100) DEFAULT NULL,
    cover_path TEXT DEFAULT NULL,
    time_open TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    time_close TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    lead_time INTERVAL DEFAULT NULL,
	periodicity INTERVAL DEFAULT NULL,
    hidden BOOLEAN DEFAULT TRUE NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL
);

DROP TABLE IF EXISTS tag CASCADE;
CREATE TABLE tag (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL UNIQUE,
	ref_count INTEGER DEFAULT 0 NOT NULL
);

DROP TABLE IF EXISTS quest_tag CASCADE;
CREATE TABLE quest_tag (
    quest_tag_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quest (quest_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tag (tag_id) ON DELETE RESTRICT
);

DROP TABLE IF EXISTS draft;
CREATE TABLE draft (
    draft_id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES author (author_id) ON DELETE CASCADE,
    container_path BYTEA NOT NULL,
    quest_id INTEGER DEFAULT NULL REFERENCES quest (quest_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS block CASCADE;
CREATE TABLE block (
    block_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL REFERENCES quest (quest_id) ON DELETE CASCADE,
    block_text TEXT NOT NULL,
    block_type_id INTEGER NOT NULL REFERENCES block_type (block_type_id) ON DELETE RESTRICT,
    pos_x REAL NOT NULL DEFAULT 0.0,
    pos_y REAL NOT NULL DEFAULT 0.0,
	next_block_id INTEGER DEFAULT NULL REFERENCES block (block_id) ON DELETE SET NULL
);

DROP TABLE IF EXISTS place CASCADE;
CREATE TABLE place (
    place_id SERIAL PRIMARY KEY,
	block_id INTEGER NOT NULL REFERENCES block (block_id) ON DELETE CASCADE,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
	radius DOUBLE PRECISION NOT NULL,
    time_open TIME WITH TIME ZONE DEFAULT NULL,
    time_close TIME WITH TIME ZONE DEFAULT NULL
);

DROP TABLE IF EXISTS answer_option CASCADE;
CREATE TABLE answer_option (
    option_id SERIAL PRIMARY KEY,
    block_id INTEGER NOT NULL REFERENCES block (block_id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    points REAL NOT NULL DEFAULT 0.0,
    next_block_id INTEGER DEFAULT NULL REFERENCES block (block_id) ON DELETE SET NULL
);

DROP TABLE IF EXISTS hint CASCADE;
CREATE TABLE hint (
    hint_id SERIAL PRIMARY KEY,
    block_id INTEGER NOT NULL REFERENCES block (block_id) ON DELETE CASCADE,
    hint_text TEXT NOT NULL,
    fine REAL NOT NULL DEFAULT 0.0
);

DROP TABLE IF EXISTS block_media CASCADE;
CREATE TABLE block_media (
    media_id SERIAL PRIMARY KEY,
    media_path TEXT NOT NULL,
    media_type_id INTEGER NOT NULL REFERENCES media_type (media_type_id) ON DELETE RESTRICT,
    block_id INTEGER NOT NULL REFERENCES block (block_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS hint_media CASCADE;
CREATE TABLE hint_media (
    media_id SERIAL PRIMARY KEY,
    media_path TEXT NOT NULL,
    media_type_id INTEGER NOT NULL REFERENCES media_type (media_type_id) ON DELETE RESTRICT,
    hint_id INTEGER NOT NULL REFERENCES hint (hint_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS history CASCADE;
CREATE TABLE history (
    history_id SERIAL PRIMARY KEY,
    telegram_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL REFERENCES quest (quest_id) ON DELETE CASCADE,
    is_finished BOOLEAN NOT NULL DEFAULT FALSE,
    last_block_id INTEGER DEFAULT NULL REFERENCES block (block_id) ON DELETE SET NULL,
	start_time TIMESTAMP WITH TIME ZONE NOT NULL,
	complition_time INTERVAL NOT NULL DEFAULT interval '0 second',
    final_score REAL NOT NULL DEFAULT 0.0
);

DROP TABLE IF EXISTS rating CASCADE;
CREATE TABLE rating (
    rating_id SERIAL PRIMARY KEY,
    quest_id INTEGER NOT NULL UNIQUE REFERENCES quest (quest_id) ON DELETE CASCADE,
    one_star_amount INTEGER NOT NULL DEFAULT 0,
    two_star_amount INTEGER NOT NULL DEFAULT 0,
    three_star_amount INTEGER NOT NULL DEFAULT 0,
    four_star_amount INTEGER NOT NULL DEFAULT 0,
    five_star_amount INTEGER NOT NULL DEFAULT 0
);

CREATE OR REPLACE FUNCTION increase_ref_count() RETURNS trigger AS
$$
	BEGIN
		UPDATE tag SET ref_count = ref_count + 1
			WHERE tag_id = NEW.tag_id;
		RETURN NEW;
	END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION decrease_ref_count() RETURNS trigger AS
$$
	BEGIN
		UPDATE tag SET ref_count = ref_count - 1
			WHERE tag_id = OLD.tag_id;
		RETURN OLD;
	END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION remove_useless_tag() RETURNS trigger AS
$$
	BEGIN
		DELETE FROM tag WHERE tag_id = OLD.tag_id;
		RETURN OLD;
	END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER add_quest_tag
	AFTER INSERT
	ON quest_tag
	FOR EACH ROW
	EXECUTE FUNCTION increase_ref_count();


CREATE OR REPLACE TRIGGER remove_quest_tag
	AFTER DELETE
	ON quest_tag
	FOR EACH ROW
	EXECUTE FUNCTION decrease_ref_count();


CREATE OR REPLACE TRIGGER update_ref_count
	AFTER UPDATE
	ON tag
	FOR EACH ROW
	WHEN (OLD.ref_count IS DISTINCT FROM NEW.ref_count AND NEW.ref_count = 0)
	EXECUTE FUNCTION remove_useless_tag();


DROP VIEW IF EXISTS quests_catalog;
CREATE VIEW quests_catalog AS
    SELECT quest_id, title, name AS author, description, keyword,
    one_star_amount, two_star_amount, three_star_amount, four_star_amount, five_star_amount,
    time_open, time_close, cover_path
    FROM quest
    JOIN author USING (author_id)
    JOIN rating USING (quest_id)
    WHERE NOT hidden AND published;
