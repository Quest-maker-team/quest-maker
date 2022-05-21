/*test#2*/

--author info
INSERT INTO authors (email, name, password, status_id) VALUES ('excursion@gmail.com','Экскурсии','password_hash',
    (SELECT status_id FROM statuses WHERE status_name= 'author'));

--quest info
INSERT INTO quests (title, author_id, description, keyword, password, time_open, time_close, lead_time, hidden) VALUES (
    'Не самые популярные достопримечательности Петербурга',
    (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com'),
    'Это небольшой квест-экскурсия с простыми вопросами и несколькими удаленными друг от друга местами, которые нужно посетить. Места разбиты на три категории, одну из которых Вы выбираете в начале экскурсии. Некоторые места являются музеями и имеют свой режим работы, режим работы указывается в соответствующем сообщении.',
    'abcdefgh', 'password', '2022-04-04 00:00:00','2022-05-10 00:00:00','1 months','false');

--places info
--branch "Temple architecture"
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.8633917835336, 30.472641018135985, 50);
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.955110380034576, 30.323965457609386, 50);
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.98357858314067, 30.255901911586367, 50);
--branch "Yards and layouts"
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.838437946932196, 30.356620326272367, 50);
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.947207872410814, 30.33907173113509, 50);
INSERT INTO places (coord_x, coord_y, time_open, time_close, radius) VALUES (59.88800242957348, 30.330013704191895,
    '2001-08-12 10:00','2001-08-12 19:00', 50);
--branch "Art"
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.92915928108905, 30.359159620821394, 50);
INSERT INTO places (coord_x, coord_y, time_open, time_close, radius) VALUES (59.94366975770656, 30.34102834662633,
    '2001-08-12 11:00','2001-08-12 17:00', 50);
INSERT INTO places (coord_x, coord_y, radius) VALUES (59.95974977958709, 30.28147021404725, 50);

--tags
INSERT INTO tags(tag_name) VALUES ('excursion');
INSERT INTO quest_tags (quest_id, tag_id) VALUES (
    (SELECT quest_id FROM quests
    WHERE title= 'Не самые популярные достопримечательности Петербурга'
    AND author_id = (SELECT author_id FROM authors WHERE email = 'excursion@gmail.com')),
    (SELECT tag_id FROM tags WHERE tag_name = 'excursion'));

--rating
INSERT INTO ratings(quest_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')));

--questions
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Это небольшой квест-экскурсия по малоизвестным местам Петербурга. Он содержит простые вопросы и несколько удаленных друг от друга мест, которые нужно посетить. Часть мест являются музеями и имеют свой режим работы.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'start'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Выберите одно из предложенных направлений.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
--branch "Temple architecture"
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Данная ветка квеста не предполагает посещения храмов, поэтому режим их работы не указывается.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Отправляйтесь по адресу пр. Обуховской Обороны, 235.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Попробуйте угадать название храма по его внешнему виду.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'open'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Следующее место - Петербургская соборная мечеть (Кронверкский пр., 7).',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Соборная мечеть на Горьковской долгое время считалась самой крупной мечетью в нашей стране. Петербургская мечеть — одна из самых больших в Европе, а также считается самой северной в мире. Высота здания достигает 39 метров, а высота минаретов — 48 метров.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Попробуйте угадать, храм какой религии будет следующим.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'open'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Последний пункт этой небольшой экскурсии - Дацан Гунзэчойней (Приморский пр., 91).',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Самый северный на планете буддийский храм был построен в Петербурге в 1909–1915 годы. Проектировкой и возведением здания занимался архитектор Барановский, который тщательно подошёл к работе над проектом. В своём великолепном здании он учёл все тибетские традиции и каноны, что позволило передать атмосферу настоящего буддийского храма.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Вы прошли ветку Храмовая архитектура.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'end'));
--branch "Yards and layouts"
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Отправляйтесь по адресу пр. Космонавтов, 63.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Копия Эйфелевой башни высотой в пятиэтажный дом, Триумфальная арка и даже стеклянная пирамида Лувра — двор жилого комплекса «Гранд Фамилия» в Московском районе летом 2014 стал настоящей резиденцией Парижа в Петербурге. Не хватает разве что шарманщика, запаха жареных каштанов и уютных кафе. Но со временем возможно всё.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Следующее место - совмещенные дворы домов по наб. Фонтанки № 2 и по улице Чайковского № 2/7.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Попробуйте угадать чьими руками создана эта красота.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'open'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Последний пункт этой небольшой экскурсии - Гранд Макет Россия (Цветочная улица, 16Л). Время работы: 10:00-19:00.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Экспозиция музея – самый большой макет России в мире площадью 800 квадратных метров, который является художественным воплощением образа нашей страны: от ее Дальневосточных рубежей до «янтарного» побережья Балтийского моря. Над его созданием трудились круглосуточно в течение пяти лет десятки самых разнообразных специалистов. На макетном поле переданы собирательные образы различных городов и регионов, а в жанровых сценках отображены фактически все виды человеческой деятельности.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Вы прошли ветку Дворы и макеты.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'end'));
--branch "Art"
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Отправляйтесь по адресу арт-центр «Пушкинская,10», Пушкинская ул., 10 (вход с Лиговского пр., 53).',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Этой улицы вы не найдёте на картах города, но она всё-таки есть, хоть и скрыта от глаз непосвящённых за двумя дверями, ведущими в арт-центр «Пушкинская,10». Для всех тех, кому близка пропитанная романтикой лирика легендарных The Beatles, это место станет настоящей Меккой ливерпульской четвёрки в Петербурге. Стены здания украшает жёлтая подводная лодка, барельефы участников группы, а также разнообразные элементы и детали, так или иначе связанные с творчеством коллектива, покорившего сердца миллионов слушателей по всему миру.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Отправляйтесь в Музей прикладного искусства им. А.Л.Штиглица (Соляной пер., 13-15). Время работы: 11:00-17:00.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Барон Александр Людвигович Штиглиц сыскал известность благодаря своей необычной меценатской деятельности, свои честно сколоченные капиталы финансист и промышленник тратил вовсе не на постройку храмов и не на работу журналов или газет, а на развитие российского искусства. Сегодня подобная деятельность может показаться абсурдной, но стоит заметить, что художников и дизайнеров только сейчас начали готовить практически во всех учебных заведениях, а во времена дореволюционной России развитием творчества занимались далеко не многие. Музей прикладного искусства является неотъемлемой частью Санкт-Петербургской государственной художественно-промышленной академии имени А. Л. Штиглица, которую основали по инициативе барона в 1878 году.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Последний пункт этой небольшой экскурсии - самый высокий арт-объект в России (на 2013 год) (фабрика «Красное Знамя», ул. Красного Курсанта, 25).',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'movement'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Петербург ежегодно принимает не один десяток самых разнообразных проектов, посвящённых современному искусству. Немудрено, что после того, как фестивали заканчиваются, в городе остаются весьма необычные арт-объекты. Так, например, в 2013 году проходил фестиваль grаFFFest, в рамках которого у нас появился самый высокий арт-объект в России. Он представляет собой 75-метровую заводскую трубу, но достаточно непростую: художники украсили промышленную трубу иллюзорной графикой, навеянной творчеством известного нидерландского иллюстратора Маурица Эшера. Создавали необычную картину прямо на глазах у интересующейся публики.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'choice'));
INSERT INTO questions (quest_id, question_text, q_type_id) VALUES ((SELECT quest_id FROM quests WHERE
    title= 'Не самые популярные достопримечательности Петербурга' 
    AND author_id= (SELECT author_id FROM authors WHERE email= 'excursion@gmail.com')),
    'Вы прошли ветку Искусство.',
    (SELECT q_type_id FROM question_types WHERE q_type_name= 'end'));

--hints
INSERT INTO hints (question_id, hint_text, fine) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'),
    'Это пасхальная атрибутика.', 1.0);
INSERT INTO hints (question_id, hint_text, fine) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'),
    '', 2.0);
INSERT INTO hints (question_id, hint_text, fine) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать, храм какой религии будет следующим.'),
    'Это пятая по численности религия мира.', 1.0);
INSERT INTO hints (question_id, hint_text, fine) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'),
    '', 1.0);

--answer options
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Это небольшой квест-экскурсия по малоизвестным местам Петербурга. Он содержит простые вопросы и несколько удаленных друг от друга мест, которые нужно посетить. Часть мест являются музеями и имеют свой режим работы.'),
    '', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Выберите одно из предложенных направлений.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Выберите одно из предложенных направлений.'),
    'Храмовая архитектура', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Данная ветка квеста не предполагает посещения храмов, поэтому режим их работы не указывается.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Выберите одно из предложенных направлений.'),
    'Искусство', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу арт-центр «Пушкинская,10», Пушкинская ул., 10 (вход с Лиговского пр., 53).'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Выберите одно из предложенных направлений.'),
    'Дворы и макеты', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу пр. Космонавтов, 63.'));
--branch "Temple architecture"
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Данная ветка квеста не предполагает посещения храмов, поэтому режим их работы не указывается.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу пр. Обуховской Обороны, 235.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Данная ветка квеста не предполагает посещения храмов, поэтому режим их работы не указывается.'),
    'Назад', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Выберите одно из предложенных направлений.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'),
    'Кулич и Пасха', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'),
    'Пасха и Кулич', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'),
    'skip', -1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Следующее место - Петербургская соборная мечеть (Кронверкский пр., 7).'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Соборная мечеть на Горьковской долгое время считалась самой крупной мечетью в нашей стране. Петербургская мечеть — одна из самых больших в Европе, а также считается самой северной в мире. Высота здания достигает 39 метров, а высота минаретов — 48 метров.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать, храм какой религии будет следующим.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать, храм какой религии будет следующим.'),
    'skip', -1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - Дацан Гунзэчойней (Приморский пр., 91).'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать, храм какой религии будет следующим.'),
    'Буддизм', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - Дацан Гунзэчойней (Приморский пр., 91).'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Самый северный на планете буддийский храм был построен в Петербурге в 1909–1915 годы. Проектировкой и возведением здания занимался архитектор Барановский, который тщательно подошёл к работе над проектом. В своём великолепном здании он учёл все тибетские традиции и каноны, что позволило передать атмосферу настоящего буддийского храма.'),
    'Закончить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Вы прошли ветку Храмовая архитектура.'));
--branch "Yards and layouts"
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Копия Эйфелевой башни высотой в пятиэтажный дом, Триумфальная арка и даже стеклянная пирамида Лувра — двор жилого комплекса «Гранд Фамилия» в Московском районе летом 2014 стал настоящей резиденцией Парижа в Петербурге. Не хватает разве что шарманщика, запаха жареных каштанов и уютных кафе. Но со временем возможно всё.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Следующее место - совмещенные дворы домов по наб. Фонтанки № 2 и по улице Чайковского № 2/7.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'),
    'Детей', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'),
    'Учеников', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'),
    'Школьников', 1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'),
    'skip', -1.0,
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - Гранд Макет Россия (Цветочная улица, 16Л). Время работы: 10:00-19:00.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Экспозиция музея – самый большой макет России в мире площадью 800 квадратных метров, который является художественным воплощением образа нашей страны: от ее Дальневосточных рубежей до «янтарного» побережья Балтийского моря. Над его созданием трудились круглосуточно в течение пяти лет десятки самых разнообразных специалистов. На макетном поле переданы собирательные образы различных городов и регионов, а в жанровых сценках отображены фактически все виды человеческой деятельности.'),
    'Закончить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Вы прошли ветку Дворы и макеты.'));
--branch "Art"
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Этой улицы вы не найдёте на картах города, но она всё-таки есть, хоть и скрыта от глаз непосвящённых за двумя дверями, ведущими в арт-центр «Пушкинская,10». Для всех тех, кому близка пропитанная романтикой лирика легендарных The Beatles, это место станет настоящей Меккой ливерпульской четвёрки в Петербурге. Стены здания украшает жёлтая подводная лодка, барельефы участников группы, а также разнообразные элементы и детали, так или иначе связанные с творчеством коллектива, покорившего сердца миллионов слушателей по всему миру.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь в Музей прикладного искусства им. А.Л.Штиглица (Соляной пер., 13-15). Время работы: 11:00-17:00.'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Барон Александр Людвигович Штиглиц сыскал известность благодаря своей необычной меценатской деятельности, свои честно сколоченные капиталы финансист и промышленник тратил вовсе не на постройку храмов и не на работу журналов или газет, а на развитие российского искусства. Сегодня подобная деятельность может показаться абсурдной, но стоит заметить, что художников и дизайнеров только сейчас начали готовить практически во всех учебных заведениях, а во времена дореволюционной России развитием творчества занимались далеко не многие. Музей прикладного искусства является неотъемлемой частью Санкт-Петербургской государственной художественно-промышленной академии имени А. Л. Штиглица, которую основали по инициативе барона в 1878 году.'),
    'Продолжить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - самый высокий арт-объект в России (на 2013 год) (фабрика «Красное Знамя», ул. Красного Курсанта, 25).'));
INSERT INTO answer_options (question_id, option_text, points, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Петербург ежегодно принимает не один десяток самых разнообразных проектов, посвящённых современному искусству. Немудрено, что после того, как фестивали заканчиваются, в городе остаются весьма необычные арт-объекты. Так, например, в 2013 году проходил фестиваль grаFFFest, в рамках которого у нас появился самый высокий арт-объект в России. Он представляет собой 75-метровую заводскую трубу, но достаточно непростую: художники украсили промышленную трубу иллюзорной графикой, навеянной творчеством известного нидерландского иллюстратора Маурица Эшера. Создавали необычную картину прямо на глазах у интересующейся публики.'),
    'Закончить', 0.0,
    (SELECT question_id FROM questions WHERE question_text= 'Вы прошли ветку Искусство.'));

--movements
--branch "Temple architecture"
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу пр. Обуховской Обороны, 235.'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.8633917835336, 30.472641018135985)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Следующее место - Петербургская соборная мечеть (Кронверкский пр., 7).'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.955110380034576, 30.323965457609386)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Соборная мечеть на Горьковской долгое время считалась самой крупной мечетью в нашей стране. Петербургская мечеть — одна из самых больших в Европе, а также считается самой северной в мире. Высота здания достигает 39 метров, а высота минаретов — 48 метров.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - Дацан Гунзэчойней (Приморский пр., 91).'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.98357858314067, 30.255901911586367)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Самый северный на планете буддийский храм был построен в Петербурге в 1909–1915 годы. Проектировкой и возведением здания занимался архитектор Барановский, который тщательно подошёл к работе над проектом. В своём великолепном здании он учёл все тибетские традиции и каноны, что позволило передать атмосферу настоящего буддийского храма.'));
--branch "Yards and layouts"
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу пр. Космонавтов, 63.'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.838437946932196, 30.356620326272367)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Копия Эйфелевой башни высотой в пятиэтажный дом, Триумфальная арка и даже стеклянная пирамида Лувра — двор жилого комплекса «Гранд Фамилия» в Московском районе летом 2014 стал настоящей резиденцией Парижа в Петербурге. Не хватает разве что шарманщика, запаха жареных каштанов и уютных кафе. Но со временем возможно всё.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Следующее место - совмещенные дворы домов по наб. Фонтанки № 2 и по улице Чайковского № 2/7.'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.947207872410814, 30.33907173113509)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - Гранд Макет Россия (Цветочная улица, 16Л). Время работы: 10:00-19:00.'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.88800242957348, 30.330013704191895)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Экспозиция музея – самый большой макет России в мире площадью 800 квадратных метров, который является художественным воплощением образа нашей страны: от ее Дальневосточных рубежей до «янтарного» побережья Балтийского моря. Над его созданием трудились круглосуточно в течение пяти лет десятки самых разнообразных специалистов. На макетном поле переданы собирательные образы различных городов и регионов, а в жанровых сценках отображены фактически все виды человеческой деятельности.'));
--branch "Art"
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь по адресу арт-центр «Пушкинская,10», Пушкинская ул., 10 (вход с Лиговского пр., 53).'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.92915928108905, 30.359159620821394)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Этой улицы вы не найдёте на картах города, но она всё-таки есть, хоть и скрыта от глаз непосвящённых за двумя дверями, ведущими в арт-центр «Пушкинская,10». Для всех тех, кому близка пропитанная романтикой лирика легендарных The Beatles, это место станет настоящей Меккой ливерпульской четвёрки в Петербурге. Стены здания украшает жёлтая подводная лодка, барельефы участников группы, а также разнообразные элементы и детали, так или иначе связанные с творчеством коллектива, покорившего сердца миллионов слушателей по всему миру.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Отправляйтесь в Музей прикладного искусства им. А.Л.Штиглица (Соляной пер., 13-15). Время работы: 11:00-17:00.'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.94366975770656, 30.34102834662633)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Барон Александр Людвигович Штиглиц сыскал известность благодаря своей необычной меценатской деятельности, свои честно сколоченные капиталы финансист и промышленник тратил вовсе не на постройку храмов и не на работу журналов или газет, а на развитие российского искусства. Сегодня подобная деятельность может показаться абсурдной, но стоит заметить, что художников и дизайнеров только сейчас начали готовить практически во всех учебных заведениях, а во времена дореволюционной России развитием творчества занимались далеко не многие. Музей прикладного искусства является неотъемлемой частью Санкт-Петербургской государственной художественно-промышленной академии имени А. Л. Штиглица, которую основали по инициативе барона в 1878 году.'));
INSERT INTO movements (question_id, place_id, next_question_id) VALUES (
    (SELECT question_id FROM questions WHERE question_text= 'Последний пункт этой небольшой экскурсии - самый высокий арт-объект в России (на 2013 год) (фабрика «Красное Знамя», ул. Красного Курсанта, 25).'),
    (SELECT place_id FROM places WHERE coords~= CAST('(59.95974977958709, 30.28147021404725)' AS POINT)),
    (SELECT question_id FROM questions WHERE question_text= 'Петербург ежегодно принимает не один десяток самых разнообразных проектов, посвящённых современному искусству. Немудрено, что после того, как фестивали заканчиваются, в городе остаются весьма необычные арт-объекты. Так, например, в 2013 году проходил фестиваль grаFFFest, в рамках которого у нас появился самый высокий арт-объект в России. Он представляет собой 75-метровую заводскую трубу, но достаточно непростую: художники украсили промышленную трубу иллюзорной графикой, навеянной творчеством известного нидерландского иллюстратора Маурица Эшера. Создавали необычную картину прямо на глазах у интересующейся публики.'));

--files
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://sousguru.ru/wp-content/uploads/2021/04/Pashalnye-kulichi.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://static.tildacdn.com/tild3734-6238-4732-a235-373238636364/42e9b4727cf579737f19.jpeg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
--hint files
INSERT INTO hint_files (f_id, hint_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://sousguru.ru/wp-content/uploads/2021/04/Pashalnye-kulichi.jpg'),
    (SELECT hint_id FROM hints WHERE hint_text= '' AND question_id= 
        (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать название храма по его внешнему виду.')));
INSERT INTO hint_files (f_id, hint_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://static.tildacdn.com/tild3734-6238-4732-a235-373238636364/42e9b4727cf579737f19.jpeg'),
    (SELECT hint_id FROM hints WHERE hint_text= '' AND question_id= 
        (SELECT question_id FROM questions WHERE question_text= 'Попробуйте угадать чьими руками создана эта красота.')));
--files
--branch "Temple architecture"
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://evroportal.ru/wp-content/uploads/2019/03/post_5c9a4dd0e5311.jpeg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://puzzleit.ru/files/puzzles/205/205062/_original.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://notypicspb.ru/wp-content/uploads/2021/09/p_cyx_4thmc_aleksandr_yaroslavcev.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://gvfsmimulqbb.usemoralis.com/0.mp4',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'video'));
--branch "Yards and layouts"
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://www.fiesta.ru/uploads/slider_image/image/40183/v880_12_MG_9257.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://gvfsmimulqbb.usemoralis.com/1.mp3',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'audio'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://www.fiesta.ru/uploads/slider_image/image/11478/v880_0_5c50d_e6fc0040_orig.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://gvfsmimulqbb.usemoralis.com/2.mp4',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'video'));
--branch "Art"
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://www.nashe.ru/storage/3427/conversions/expush2b-large.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://www.fiesta.ru/uploads/slider_image/image/11483/v880_1393947_468649363253889_121508955_n.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
INSERT INTO files (url_for_file, f_type_id) VALUES (
    'https://www.fiesta.ru/uploads/slider_image/image/40199/v880_v800_1uEfjChw0Ws.jpg',
    (SELECT f_type_id FROM file_types WHERE f_type_name= 'image'));
--question files
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://evroportal.ru/wp-content/uploads/2019/03/post_5c9a4dd0e5311.jpeg'),
    (SELECT question_id FROM questions WHERE question_text= 'Композиция ансамбля при ближайшем рассмотрении превращается в архитектурную шутку выдающегося архитектора и новатора Н. Львова. Храм построен в форме кулича, а колокольня — в форме пасхи. Кроме того, в этой церкви хранится уникальная чудотворная икона Всех скорбящих Радость с грошиками, прилипшими к красочному слою во время пожара.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://puzzleit.ru/files/puzzles/205/205062/_original.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Соборная мечеть на Горьковской долгое время считалась самой крупной мечетью в нашей стране. Петербургская мечеть — одна из самых больших в Европе, а также считается самой северной в мире. Высота здания достигает 39 метров, а высота минаретов — 48 метров.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://notypicspb.ru/wp-content/uploads/2021/09/p_cyx_4thmc_aleksandr_yaroslavcev.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Самый северный на планете буддийский храм был построен в Петербурге в 1909–1915 годы. Проектировкой и возведением здания занимался архитектор Барановский, который тщательно подошёл к работе над проектом. В своём великолепном здании он учёл все тибетские традиции и каноны, что позволило передать атмосферу настоящего буддийского храма.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://gvfsmimulqbb.usemoralis.com/0.mp4'),
    (SELECT question_id FROM questions WHERE question_text= 'Самый северный на планете буддийский храм был построен в Петербурге в 1909–1915 годы. Проектировкой и возведением здания занимался архитектор Барановский, который тщательно подошёл к работе над проектом. В своём великолепном здании он учёл все тибетские традиции и каноны, что позволило передать атмосферу настоящего буддийского храма.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://www.fiesta.ru/uploads/slider_image/image/40183/v880_12_MG_9257.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Копия Эйфелевой башни высотой в пятиэтажный дом, Триумфальная арка и даже стеклянная пирамида Лувра — двор жилого комплекса «Гранд Фамилия» в Московском районе летом 2014 стал настоящей резиденцией Парижа в Петербурге. Не хватает разве что шарманщика, запаха жареных каштанов и уютных кафе. Но со временем возможно всё.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://gvfsmimulqbb.usemoralis.com/1.mp3'),
    (SELECT question_id FROM questions WHERE question_text= 'Копия Эйфелевой башни высотой в пятиэтажный дом, Триумфальная арка и даже стеклянная пирамида Лувра — двор жилого комплекса «Гранд Фамилия» в Московском районе летом 2014 стал настоящей резиденцией Парижа в Петербурге. Не хватает разве что шарманщика, запаха жареных каштанов и уютных кафе. Но со временем возможно всё.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://www.fiesta.ru/uploads/slider_image/image/11478/v880_0_5c50d_e6fc0040_orig.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Этот удивительный дворик на улице Чайковского является одной из самых молодых достопримечательностей Петербурга. Кстати, двор знаменит не только благодаря ярким краскам мозаики, но также и потому, что сделан он руками детей. Красочное панно, словно чешуя пёстрой рыбы, окутало буквально каждый объект во дворе. Скамейки, дорожки, стены домов, скульптуры и солнечные часы украшены красочными рисунками мозаики из цветного стекла. Ничем не примечательный двор в какой-то момент начал буквально обрастать мозаикой прямо на глазах у местных жителей и со временем стал своеобразным музеем под открытым небом. Эту достопримечательность, которую лучше один раз увидеть, чем сто раз о ней услышать, создали ученики Малой Академии искусств.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://gvfsmimulqbb.usemoralis.com/2.mp4'),
    (SELECT question_id FROM questions WHERE question_text= 'Экспозиция музея – самый большой макет России в мире площадью 800 квадратных метров, который является художественным воплощением образа нашей страны: от ее Дальневосточных рубежей до «янтарного» побережья Балтийского моря. Над его созданием трудились круглосуточно в течение пяти лет десятки самых разнообразных специалистов. На макетном поле переданы собирательные образы различных городов и регионов, а в жанровых сценках отображены фактически все виды человеческой деятельности.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://www.nashe.ru/storage/3427/conversions/expush2b-large.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Этой улицы вы не найдёте на картах города, но она всё-таки есть, хоть и скрыта от глаз непосвящённых за двумя дверями, ведущими в арт-центр «Пушкинская,10». Для всех тех, кому близка пропитанная романтикой лирика легендарных The Beatles, это место станет настоящей Меккой ливерпульской четвёрки в Петербурге. Стены здания украшает жёлтая подводная лодка, барельефы участников группы, а также разнообразные элементы и детали, так или иначе связанные с творчеством коллектива, покорившего сердца миллионов слушателей по всему миру.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://www.fiesta.ru/uploads/slider_image/image/11483/v880_1393947_468649363253889_121508955_n.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Барон Александр Людвигович Штиглиц сыскал известность благодаря своей необычной меценатской деятельности, свои честно сколоченные капиталы финансист и промышленник тратил вовсе не на постройку храмов и не на работу журналов или газет, а на развитие российского искусства. Сегодня подобная деятельность может показаться абсурдной, но стоит заметить, что художников и дизайнеров только сейчас начали готовить практически во всех учебных заведениях, а во времена дореволюционной России развитием творчества занимались далеко не многие. Музей прикладного искусства является неотъемлемой частью Санкт-Петербургской государственной художественно-промышленной академии имени А. Л. Штиглица, которую основали по инициативе барона в 1878 году.'));
INSERT INTO question_files (f_id, question_id) VALUES (
    (SELECT f_id FROM files WHERE url_for_file= 'https://www.fiesta.ru/uploads/slider_image/image/40199/v880_v800_1uEfjChw0Ws.jpg'),
    (SELECT question_id FROM questions WHERE question_text= 'Петербург ежегодно принимает не один десяток самых разнообразных проектов, посвящённых современному искусству. Немудрено, что после того, как фестивали заканчиваются, в городе остаются весьма необычные арт-объекты. Так, например, в 2013 году проходил фестиваль grаFFFest, в рамках которого у нас появился самый высокий арт-объект в России. Он представляет собой 75-метровую заводскую трубу, но достаточно непростую: художники украсили промышленную трубу иллюзорной графикой, навеянной творчеством известного нидерландского иллюстратора Маурица Эшера. Создавали необычную картину прямо на глазах у интересующейся публики.'));