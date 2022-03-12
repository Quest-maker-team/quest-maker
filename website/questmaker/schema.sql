--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

-- Started on 2022-03-12 20:03:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3437 (class 1262 OID 16394)
-- Name: questmaker; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE questmaker WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1251';


ALTER DATABASE questmaker OWNER TO postgres;

\connect questmaker

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16484)
-- Name: answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    question_id integer NOT NULL,
    answer_text text NOT NULL
);


ALTER TABLE public.answer OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16483)
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.answer ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 212 (class 1259 OID 16440)
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    id integer NOT NULL,
    email character varying(100),
    login character varying(100) NOT NULL,
    hash_password bytea NOT NULL,
    status_id integer NOT NULL
);


ALTER TABLE public.author OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16439)
-- Name: author_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.author ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 16426)
-- Name: author_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author_status (
    id integer NOT NULL,
    status character varying(100) NOT NULL
);


ALTER TABLE public.author_status OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16425)
-- Name: author_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.author_status ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.author_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16582)
-- Name: directions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.directions (
    id integer NOT NULL,
    cur_place_id integer,
    next_place_id integer,
    description text
);


ALTER TABLE public.directions OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16581)
-- Name: directions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.directions ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.directions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 224 (class 1259 OID 16518)
-- Name: files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files (
    id integer NOT NULL,
    type_of_object_id integer NOT NULL,
    object_id integer NOT NULL,
    url_for_file text NOT NULL,
    type_of_file character varying NOT NULL
);


ALTER TABLE public.files OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16517)
-- Name: files_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.files ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.files_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 16505)
-- Name: hints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hints (
    id integer NOT NULL,
    question_id integer NOT NULL,
    hint_text text NOT NULL,
    fine real NOT NULL
);


ALTER TABLE public.hints OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16504)
-- Name: hints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.hints ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hints_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 236 (class 1259 OID 16622)
-- Name: history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    quest_id integer NOT NULL,
    is_finished boolean NOT NULL,
    last_place_id integer,
    final_score real NOT NULL
);


ALTER TABLE public.history OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16621)
-- Name: history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 16461)
-- Name: object_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object_type (
    id integer NOT NULL,
    object_type character varying NOT NULL
);


ALTER TABLE public.object_type OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16460)
-- Name: object_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.object_type ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.object_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 16568)
-- Name: place; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.place (
    id integer NOT NULL,
    place_name character varying NOT NULL,
    coord point NOT NULL,
    quest_id integer NOT NULL,
    description text,
    time_open timestamp without time zone,
    time_close time without time zone,
    points real NOT NULL,
    fine real NOT NULL,
    radius double precision NOT NULL
);


ALTER TABLE public.place OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16567)
-- Name: place_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.place ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 232 (class 1259 OID 16595)
-- Name: possible_answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.possible_answers (
    id integer NOT NULL,
    question_id integer NOT NULL,
    possible_ans_text text NOT NULL
);


ALTER TABLE public.possible_answers OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16594)
-- Name: possible_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.possible_answers ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.possible_answers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 16547)
-- Name: quest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quest (
    id integer NOT NULL,
    title character varying NOT NULL,
    author_id integer NOT NULL,
    description text NOT NULL,
    key_word character varying,
    tags text,
    time_open timestamp without time zone NOT NULL,
    time_close timestamp without time zone NOT NULL,
    lead_time interval NOT NULL
);


ALTER TABLE public.quest OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16546)
-- Name: quest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.quest ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.quest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 16492)
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question (
    id integer NOT NULL,
    place_id integer NOT NULL,
    question_text text NOT NULL,
    points real NOT NULL,
    fine real NOT NULL,
    type integer NOT NULL
);


ALTER TABLE public.question OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16491)
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.question ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 16475)
-- Name: question_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_type (
    id integer NOT NULL,
    question_type character varying NOT NULL
);


ALTER TABLE public.question_type OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16474)
-- Name: question_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.question_type ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.question_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 234 (class 1259 OID 16608)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    telegram_id text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16607)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3413 (class 0 OID 16484)
-- Dependencies: 218
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3407 (class 0 OID 16440)
-- Dependencies: 212
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3405 (class 0 OID 16426)
-- Dependencies: 210
-- Data for Name: author_status; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3425 (class 0 OID 16582)
-- Dependencies: 230
-- Data for Name: directions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3419 (class 0 OID 16518)
-- Dependencies: 224
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3417 (class 0 OID 16505)
-- Dependencies: 222
-- Data for Name: hints; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3431 (class 0 OID 16622)
-- Dependencies: 236
-- Data for Name: history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3409 (class 0 OID 16461)
-- Dependencies: 214
-- Data for Name: object_type; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3423 (class 0 OID 16568)
-- Dependencies: 228
-- Data for Name: place; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3427 (class 0 OID 16595)
-- Dependencies: 232
-- Data for Name: possible_answers; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3421 (class 0 OID 16547)
-- Dependencies: 226
-- Data for Name: quest; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3415 (class 0 OID 16492)
-- Dependencies: 220
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3411 (class 0 OID 16475)
-- Dependencies: 216
-- Data for Name: question_type; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3429 (class 0 OID 16608)
-- Dependencies: 234
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 217
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.answer_id_seq', 1, false);


--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 211
-- Name: author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.author_id_seq', 1, false);


--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 209
-- Name: author_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.author_status_id_seq', 1, false);


--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 229
-- Name: directions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.directions_id_seq', 1, false);


--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 223
-- Name: files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.files_id_seq', 1, false);


--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 221
-- Name: hints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hints_id_seq', 1, false);


--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 235
-- Name: history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.history_id_seq', 1, false);


--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 213
-- Name: object_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.object_type_id_seq', 1, false);


--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 227
-- Name: place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.place_id_seq', 1, false);


--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 231
-- Name: possible_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.possible_answers_id_seq', 1, false);


--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 225
-- Name: quest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quest_id_seq', 1, false);


--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 219
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_id_seq', 1, false);


--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 215
-- Name: question_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_type_id_seq', 1, false);


--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 233
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- TOC entry 3238 (class 2606 OID 16490)
-- Name: answer answer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_pkey PRIMARY KEY (id);


--
-- TOC entry 3232 (class 2606 OID 16446)
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (id);


--
-- TOC entry 3230 (class 2606 OID 16430)
-- Name: author_status author_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author_status
    ADD CONSTRAINT author_status_pkey PRIMARY KEY (id);


--
-- TOC entry 3250 (class 2606 OID 16588)
-- Name: directions directions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directions
    ADD CONSTRAINT directions_pkey PRIMARY KEY (id);


--
-- TOC entry 3244 (class 2606 OID 16524)
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- TOC entry 3242 (class 2606 OID 16511)
-- Name: hints hints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hints
    ADD CONSTRAINT hints_pkey PRIMARY KEY (id);


--
-- TOC entry 3256 (class 2606 OID 16626)
-- Name: history history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history
    ADD CONSTRAINT history_pkey PRIMARY KEY (id);


--
-- TOC entry 3234 (class 2606 OID 16467)
-- Name: object_type object_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_type
    ADD CONSTRAINT object_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3248 (class 2606 OID 16574)
-- Name: place place_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.place
    ADD CONSTRAINT place_pkey PRIMARY KEY (id);


--
-- TOC entry 3252 (class 2606 OID 16601)
-- Name: possible_answers possible_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_answers
    ADD CONSTRAINT possible_answers_pkey PRIMARY KEY (id);


--
-- TOC entry 3246 (class 2606 OID 16553)
-- Name: quest quest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quest
    ADD CONSTRAINT quest_pkey PRIMARY KEY (id);


--
-- TOC entry 3240 (class 2606 OID 16498)
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- TOC entry 3236 (class 2606 OID 16481)
-- Name: question_type question_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_type
    ADD CONSTRAINT question_type_pkey PRIMARY KEY (id);


--
-- TOC entry 3254 (class 2606 OID 16614)
-- Name: users user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3261 (class 2606 OID 16554)
-- Name: quest fk_author_quest; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quest
    ADD CONSTRAINT fk_author_quest FOREIGN KEY (author_id) REFERENCES public.author(id);


--
-- TOC entry 3257 (class 2606 OID 16447)
-- Name: author fk_author_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT fk_author_status FOREIGN KEY (status_id) REFERENCES public.author_status(id);


--
-- TOC entry 3263 (class 2606 OID 16589)
-- Name: directions fk_link_cur_place; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directions
    ADD CONSTRAINT fk_link_cur_place FOREIGN KEY (cur_place_id) REFERENCES public.place(id);


--
-- TOC entry 3260 (class 2606 OID 16525)
-- Name: files fk_object_type_to_file; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT fk_object_type_to_file FOREIGN KEY (type_of_object_id) REFERENCES public.object_type(id);


--
-- TOC entry 3262 (class 2606 OID 16575)
-- Name: place fk_place_owner; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.place
    ADD CONSTRAINT fk_place_owner FOREIGN KEY (quest_id) REFERENCES public.quest(id);


--
-- TOC entry 3264 (class 2606 OID 16602)
-- Name: possible_answers fk_possible_ans_to_question; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_answers
    ADD CONSTRAINT fk_possible_ans_to_question FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 3259 (class 2606 OID 16512)
-- Name: hints fk_question_hint; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hints
    ADD CONSTRAINT fk_question_hint FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- TOC entry 3258 (class 2606 OID 16499)
-- Name: question fk_question_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_question_type FOREIGN KEY (type) REFERENCES public.question_type(id);


-- Completed on 2022-03-12 20:03:35

--
-- PostgreSQL database dump complete
--

