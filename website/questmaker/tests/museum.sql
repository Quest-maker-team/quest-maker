/*test#1*/


INSERT INTO authors (email,name, password, status_id, avatar_url) VALUES ('hermitage@mail.ru','Главный Музей Страны','password_hash',0,
'http://www.saint-petersburg.com/images/museums/hermitage-museum/state-hermitage-museum-in-st-petersburg.jpg');
INSERT INTO quests (title, author_id, description, password, cover_url, time_open, time_close, lead_time,  hidden) VALUES ('По залам Эрмитажа',1,
'Главный музейный комплекс включает в себя шесть связанных между собой зданий — Зимний дворец, Запасной дом Зимнего дворца, Малый Эрмитаж, Большой (Старый) Эрмитаж, Новый Эрмитаж и Эрмитажный театр. В них открыты для посещения 365 залов. Также в распоряжении музея находятся Главный штаб, Музей Императорского фарфорового завода, реставрационно-хранительский центр «Старая Деревня» и Меншиковский дворец.
Общая площадь помещений (зданий) Государственного Эрмитажа составляет 233 345 м², экспозиционно-выставочная площадь — 100 000 м².
Свою историю музей начинал с коллекции произведений искусства, приобретённых в частном порядке российской императрицей Екатериной II в 1764 году. Первоначально это собрание размещалось в специальном дворцовом флигеле — Эрмитаже (от фр. ermitage — место уединения, келья, приют отшельника, затворничество; ныне Малый Эрмитаж) — откуда и закрепилось общее название будущего музея. В 1852 году из сильно разросшейся коллекции был сформирован и открыт для посещения публичный музей, расположившийся в специально для этого построенном здании Нового Эрмитажа.
Современный Государственный Эрмитаж представляет собой сложный музейный комплекс. Основная экспозиционная часть музея занимает пять зданий, расположенных вдоль набережной реки Невы, главным из которых принято считать Зимний дворец, также музею принадлежат Восточное крыло Главного штаба на Дворцовой площади, Меншиковский дворец на другой стороне Невы, фондохранилище в «Старой Деревне» и другие здания.
Коллекция музея насчитывает около трёх миллионов произведений искусства и памятников мировой культуры, собранных начиная с каменного века и до нашего столетия. В составе коллекции — живопись, графика, скульптура и предметы прикладного искусства, археологические находки и нумизматический материал.
В 2013 году Государственный Эрмитаж вошёл в число двадцати самых посещаемых художественных музеев мира. По результатам 2018 года он занял 9-е место по посещаемости среди музеев мира (в 2018 году там побывали 4,2 миллиона человек)[7]. В 2019 году Эрмитаж принял 4 956 524 посетителя, заняв восьмое место среди самых посещаемых художественных музеев мира.'
,'password','https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Winter_Palace_Panorama_4.jpg/548px-Winter_Palace_Panorama_4.jpg',
'2011-01-01 00:00:00','2022-01-01 00:00:00','6 months','false');

--Зимний дворец
INSERT INTO places (coords, time_open, time_close, radius) VALUES ('(59.940925, 30.312946)', '2001-08-12 09:00','2001-08-12 19:00',26.5);
--Малый Эрмитаж
INSERT INTO places (coords, time_open, time_close, radius) VALUES ('(59.940742, 30.316448)', '2001-08-12 09:00','2001-08-12 19:00',15.7);
--Большой Эрмитаж
INSERT INTO places (coords, time_open, time_close, radius) VALUES ('(59.942178, 30.316193)', '2001-08-12 09:00','2001-08-12 20:00',50.3);
--Новый Эрмитаж
INSERT INTO places (coords, time_open, time_close, radius) VALUES ('(59.941711, 30.316884)', '2001-08-12 09:00','2001-08-12 19:00',48);
--Эрмитажный театр
INSERT INTO places (coords, time_open, time_close, radius) VALUES ('(59.942345, 30.316612)', '2001-08-12 09:00','2001-08-12 19:00',15.6);

INSERT INTO tags (quest_id, tag_name) VALUES (1,'educational');
INSERT INTO tags (quest_id, tag_name) VALUES (1,'historical');


INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Идите к Зимнему Дворцу',3);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'В каком году был основан Зимний дворец?',0);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Кто архитектор?',1);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'На каком из представленых изображений находится правитель России по указу которого был построен Русский музей?',1);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Двиньтесь к Малому Эрмитажу',2);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Двиньтесь к Большому Эрмитажу',2);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Двиньтесь к Новому Эрмитажу',2);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'В какие годы строился Малый Эрмитаж? Укажите годы через дефис.',0);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'В какие годы строился Большой Эрмитаж? Укажите годы через дефис.',0);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'В какие годы строился Новый Эрмитаж? Укажите годы через дефис.',0);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Двиньтесь к Эрмитажному театру',2);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'В каком году был основан Эрмитажный театр?',0);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Понравился ли квест?',1);
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES (1,'Квест закончен',4);

INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (1,'',0,2);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (2,'1754',10,3);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (3,'Андрей Воронихин',-5,4);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (3,'Огюст Монферран',-5,4);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (3,'Франческо Растрелли',5,4);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (3,'Карл Росси',-5,4);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (4,'1',-1,5);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (4,'2',-1,6);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (4,'3',3,7);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (8,'1764—1775',10,11);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (9,'1771—1787',10,11);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (10,'1842—1851',10,11);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (5,'',3,8);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (6,'',3,9);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (7,'',3,10);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (11,'',3,12);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (12,'skip',0,13);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (12,'1782',3,13);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (13,'да',100,14);
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (13,'нет',-100,14);


INSERT INTO movements (question_id, place_id, next_question_id) VALUES (1,1,2);
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (5,2,8);
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (6,3,9);
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (7,4,10);
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (11,5,12);


INSERT INTO files (url_for_file, f_type_id) VALUES ('https://upload.wikimedia.org/wikipedia/commons/0/0e/Elizabeth_of_Russia_by_V.Eriksen.jpg',0);
INSERT INTO files (url_for_file, f_type_id) VALUES ('https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Mikola_II_%28cropped%29-2.jpg/548px-Mikola_II_%28cropped%29-2.jpg',0);
INSERT INTO files (url_for_file, f_type_id) VALUES ('https://azbyka.ru/days/storage/images/icons-of-saints/2280/p1ann1j7utlc61pgcs2p1gle1olc4.jpg',0);
INSERT INTO files (url_for_file, f_type_id) VALUES ('https://habrastorage.org/getpro/habr/post_images/a42/97b/c0b/a4297bc0b36fbf9878dd6173c0f0fbb4.jpg',0);

INSERT INTO question_files (f_id, question_id) VALUES (1,4);
INSERT INTO question_files (f_id, question_id) VALUES (2,4);
INSERT INTO question_files (f_id, question_id) VALUES (3,4);

INSERT INTO hints (question_id, hint_text, fine) VALUES (2,'Здание основано в шестидесятые годы 18 века.',1.0);
INSERT INTO hints (question_id, hint_text, fine) VALUES (13,'Правильный ответ - да',50.0);

INSERT INTO hint_files (f_id, hint_id) VALUES (4,2);


INSERT INTO ratings(quest_id) VALUES (1);








