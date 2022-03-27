/*test#1*/


INSERT INTO authors VALUES (0,'hermitage@mail.ru','Главный Музей Страны','password_hash',0,
'http://www.saint-petersburg.com/images/museums/hermitage-museum/state-hermitage-museum-in-st-petersburg.jpg');
INSERT INTO quests VALUES (0,'По залам Эрмитажа',0,'
Главный музейный комплекс включает в себя шесть связанных между собой зданий — Зимний дворец, Запасной дом Зимнего дворца, Малый Эрмитаж, Большой (Старый) Эрмитаж, Новый Эрмитаж и Эрмитажный театр. В них открыты для посещения 365 залов. Также в распоряжении музея находятся Главный штаб, Музей Императорского фарфорового завода, реставрационно-хранительский центр «Старая Деревня» и Меншиковский дворец.
Общая площадь помещений (зданий) Государственного Эрмитажа составляет 233 345 м², экспозиционно-выставочная площадь — 100 000 м².
Свою историю музей начинал с коллекции произведений искусства, приобретённых в частном порядке российской императрицей Екатериной II в 1764 году. Первоначально это собрание размещалось в специальном дворцовом флигеле — Эрмитаже (от фр. ermitage — место уединения, келья, приют отшельника, затворничество; ныне Малый Эрмитаж) — откуда и закрепилось общее название будущего музея. В 1852 году из сильно разросшейся коллекции был сформирован и открыт для посещения публичный музей, расположившийся в специально для этого построенном здании Нового Эрмитажа.
Современный Государственный Эрмитаж представляет собой сложный музейный комплекс. Основная экспозиционная часть музея занимает пять зданий, расположенных вдоль набережной реки Невы, главным из которых принято считать Зимний дворец, также музею принадлежат Восточное крыло Главного штаба на Дворцовой площади, Меншиковский дворец на другой стороне Невы, фондохранилище в «Старой Деревне» и другие здания.
Коллекция музея насчитывает около трёх миллионов произведений искусства и памятников мировой культуры, собранных начиная с каменного века и до нашего столетия. В составе коллекции — живопись, графика, скульптура и предметы прикладного искусства, археологические находки и нумизматический материал.
В 2013 году Государственный Эрмитаж вошёл в число двадцати самых посещаемых художественных музеев мира. По результатам 2018 года он занял 9-е место по посещаемости среди музеев мира (в 2018 году там побывали 4,2 миллиона человек)[7]. В 2019 году Эрмитаж принял 4 956 524 посетителя, заняв восьмое место среди самых посещаемых художественных музеев мира.
',NULL,'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Winter_Palace_Panorama_4.jpg/548px-Winter_Palace_Panorama_4.jpg',
'2011-01-01 00:00:00','2022-01-01 00:00:00','6 months','false');

--fake place
--INSERT INTO places VALUES (0,(0,0), CURRENT_TIMESTAMP(),CURRENT_TIMESTAMP())+'INTERVAL (1 HOUR)',1000);
--Зимний дворец
INSERT INTO places VALUES (0,'(59.940925, 30.312946)', '2001-08-12 09:00','2001-08-12 19:00',26.5);
--Малый Эрмитаж
INSERT INTO places VALUES (1,'(59.940742, 30.316448)', '2001-08-12 09:00','2001-08-12 19:00',15.7);
--Большой Эрмитаж
INSERT INTO places VALUES (2,'(59.942178, 30.316193)', '2001-08-12 09:00','2001-08-12 20:00',50.3);
--Новый Эрмитаж
INSERT INTO places VALUES (3,'(59.941711, 30.316884)', '2001-08-12 09:00','2001-08-12 19:00',48);
--Эрмитажный театр
INSERT INTO places VALUES (4,'(59.942345, 30.316612)', '2001-08-12 09:00','2001-08-12 19:00',15.6);

INSERT INTO tags VALUES (0,0,'educational');
INSERT INTO tags VALUES (1,0,'historical');

--fake question
INSERT INTO questions VALUES (0,0,'Идите к Зимнему Дворцу',3);
INSERT INTO questions VALUES (1,0,'В каком году был основан Зимний дворец?',0);	
INSERT INTO questions VALUES (2,0,'Кто архитектор?',1);
INSERT INTO questions VALUES (3,0,'На каком из представленых изображений находится правитель России по указу которого был построен Русский музей?',1);
INSERT INTO questions VALUES (4,0,'Двиньтесь к Малому Эрмитажу',2);
INSERT INTO questions VALUES (5,0,'Двиньтесь к Большому Эрмитажу',2);
INSERT INTO questions VALUES (6,0,'Двиньтесь к Новому Эрмитажу',2);	
INSERT INTO questions VALUES (7,0,'В какие годы строился Малый Эрмитаж? Укажите годы через дефис.',0);	
INSERT INTO questions VALUES (8,0,'В какие годы строился Большой Эрмитаж? Укажите годы через дефис.',0);	
INSERT INTO questions VALUES (9,0,'В какие годы строился Новый Эрмитаж? Укажите годы через дефис.',0);	
INSERT INTO questions VALUES (10,0,'Двиньтесь к Эрмитажному театру',2);	
INSERT INTO questions VALUES (11,0,'В каком году был основан Эрмитажный театр?',0);	
INSERT INTO questions VALUES (12,0,'Понравился ли квест?',1);	
INSERT INTO questions VALUES (13,0,'Квест закончен',4);

INSERT INTO answer_options VALUES (0,0,'',0,1);
INSERT INTO answer_options VALUES (1,1,'1754',10,2);
INSERT INTO answer_options VALUES (2,2,'Андрей Воронихин',-5,3);
INSERT INTO answer_options VALUES (3,2,'Огюст Монферран',-5,3);
INSERT INTO answer_options VALUES (4,2,'Франческо Растрелли',5,3);
INSERT INTO answer_options VALUES (5,2,'Карл Росси',-5,3);
INSERT INTO answer_options VALUES (6,3,'1',-1,4);
INSERT INTO answer_options VALUES (7,3,'2',-1,5);
INSERT INTO answer_options VALUES (8,3,'3',3,6);	
INSERT INTO answer_options VALUES (9,7,'1764-1775',10,10);
INSERT INTO answer_options VALUES (10,8,'1771-1787',10,10);
INSERT INTO answer_options VALUES (11,9,'1842-1851',10,10);
INSERT INTO answer_options VALUES (12,4,'',3,7);
INSERT INTO answer_options VALUES (13,5,'',3,8);
INSERT INTO answer_options VALUES (14,6,'',3,9);
INSERT INTO answer_options VALUES (15,10,'',3,11);
INSERT INTO answer_options VALUES (16,11,'skip',0,12);
INSERT INTO answer_options VALUES (17,11,'1782',3,12);
INSERT INTO answer_options VALUES (18,12,'да',100,13);
INSERT INTO answer_options VALUES (19,12,'нет',-100,13);


INSERT INTO movements VALUES (0,0,0,1);
INSERT INTO movements VALUES (1,1,4,7);
INSERT INTO movements VALUES (2,2,5,8);
INSERT INTO movements VALUES (3,3,6,9);
INSERT INTO movements VALUES (4,4,10,11);


INSERT INTO files VALUES (0,'https://upload.wikimedia.org/wikipedia/commons/0/0e/Elizabeth_of_Russia_by_V.Eriksen.jpg',0);
INSERT INTO files VALUES (1,'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Mikola_II_%28cropped%29-2.jpg/548px-Mikola_II_%28cropped%29-2.jpg',0);
INSERT INTO files VALUES (2,'https://cdni.rt.com/files/news/20/43/60/00/aaaa-2.jpg',0);
INSERT INTO files VALUES (3,'https://englishforbeginner.ru/wp-content/uploads/2021/08/scale_1200yvaprol.jpg',0);

INSERT INTO question_files VALUES (0,3,0);
INSERT INTO question_files VALUES (1,3,1);
INSERT INTO question_files VALUES (2,3,2);

INSERT INTO hints VALUES (0,1,'Здание основано в шестидесятые годы 18 века.',1.0);
INSERT INTO hints VALUES (1,12,'Правильный ответ - да',50.0);

INSERT INTO hint_files VALUES (0,1,3);


INSERT INTO ratings(rating_id, quest_id) VALUES (0,0);








