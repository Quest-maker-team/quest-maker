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
INSERT INTO questions VALUES (11,0,'В каком году был основан Зимний дворец?',0);	
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
INSERT INTO answer_options VALUES (9,7,'1764—1775',10,10);
INSERT INTO answer_options VALUES (10,8,'1771—1787',10,10);
INSERT INTO answer_options VALUES (11,9,'1842—1851',10,10);
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
INSERT INTO files VALUES (2,'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Alexei_Nikolaevich%2C_Tsarevich_of_Russia.jpg/480px-Alexei_Nikolaevich%2C_Tsarevich_of_Russia.jpg',0);
INSERT INTO files VALUES (3,'data:image/jpeg;base64,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',0);

INSERT INTO question_files VALUES (0,6,0);
INSERT INTO question_files VALUES (1,7,1);
INSERT INTO question_files VALUES (2,8,2);

INSERT INTO hints VALUES (0,1,'Здание основано в шестидесятые годы 18 века.',1.0);
INSERT INTO hints VALUES (1,12,'Правильный ответ - да',50.0);

INSERT INTO hint_files VALUES (0,1,3);


INSERT INTO ratings(rating_id, quest_id) VALUES (0,0);








