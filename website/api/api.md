# API description
For simplicity, answers can contain only this status codes:
* `200 OK` if success;
* `400 Bad Request` if there is request syntax error;
* `500 Internal Server Error` if server error.

## GET
`GET api/quest/{quest_id}`

Return JSON with information about quest.

JSON contains fields as same as table [quests](../../docs/image/db.png),
but with 
field `start_qustion_id` and arrays `tags`, `questions`,
and `files` with info about related entities
(**but with values instead of values ids, e.g. `type` 
instead of `q_type_id`**).

`quest` `question`, `hint`, `answer` objects also contain array
`files` of file objects.

`question` objects contain arrays `hints`, 
`answer_options` and `movements` with related entities.

`hint` objects contain fields `hint_text`, `fine`
and array `file` of file objects

Other entities' fields as same as in [database](../../docs/image/db.png).

Returned JSON example:
```json
{
    "author": "Главный Музей Страны",
    "cover_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Winter_Palace_Panorama_4.jpg/548px-Winter_Palace_Panorama_4.jpg",
    "description": "Главный музейный комплекс включает в себя шесть связанных между собой зданий — Зимний дворец, Запасной дом Зимнего дворца, Малый Эрмитаж, Большой (Старый) Эрмитаж, Новый Эрмитаж и Эрмитажный театр. В них открыты для посещения 365 залов. Также в распоряжении музея находятся Главный штаб, Музей Императорского фарфорового завода, реставрационно-хранительский центр «Старая Деревня» и Меншиковский дворец.\r\nОбщая площадь помещений (зданий) Государственного Эрмитажа составляет 233 345 м², экспозиционно-выставочная площадь — 100 000 м².\r\nСвою историю музей начинал с коллекции произведений искусства, приобретённых в частном порядке российской императрицей Екатериной II в 1764 году. Первоначально это собрание размещалось в специальном дворцовом флигеле — Эрмитаже (от фр. ermitage — место уединения, келья, приют отшельника, затворничество; ныне Малый Эрмитаж) — откуда и закрепилось общее название будущего музея. В 1852 году из сильно разросшейся коллекции был сформирован и открыт для посещения публичный музей, расположившийся в специально для этого построенном здании Нового Эрмитажа.\r\nСовременный Государственный Эрмитаж представляет собой сложный музейный комплекс. Основная экспозиционная часть музея занимает пять зданий, расположенных вдоль набережной реки Невы, главным из которых принято считать Зимний дворец, также музею принадлежат Восточное крыло Главного штаба на Дворцовой площади, Меншиковский дворец на другой стороне Невы, фондохранилище в «Старой Деревне» и другие здания.\r\nКоллекция музея насчитывает около трёх миллионов произведений искусства и памятников мировой культуры, собранных начиная с каменного века и до нашего столетия. В составе коллекции — живопись, графика, скульптура и предметы прикладного искусства, археологические находки и нумизматический материал.\r\nВ 2013 году Государственный Эрмитаж вошёл в число двадцати самых посещаемых художественных музеев мира. По результатам 2018 года он занял 9-е место по посещаемости среди музеев мира (в 2018 году там побывали 4,2 миллиона человек)[7]. В 2019 году Эрмитаж принял 4 956 524 посетителя, заняв восьмое место среди самых посещаемых художественных музеев мира.",
    "files": [],
    "hidden": false,
    "lead_time": 15552000.0,
    "password": "password",
    "quest_id": "1",
    "questions": [
        {
            "answer_options": [],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 14,
            "text": "Квест закончен",
            "type": "end"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 14,
                    "points": 100.0,
                    "text": "да"
                },
                {
                    "next_question_id": 14,
                    "points": -100.0,
                    "text": "нет"
                }
            ],
            "files": [],
            "hints": [
                {
                    "files": [
                        {
                            "type": "image",
                            "url": "https://habrastorage.org/getpro/habr/post_images/a42/97b/c0b/a4297bc0b36fbf9878dd6173c0f0fbb4.jpg"
                        }
                    ],
                    "fine": 50.0,
                    "hint_text": "Правильный ответ - да"
                }
            ],
            "movements": [],
            "question_id": 13,
            "text": "Понравился ли квест?",
            "type": "choice"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 13,
                    "points": 0.0,
                    "text": "skip"
                },
                {
                    "next_question_id": 13,
                    "points": 3.0,
                    "text": "1782"
                }
            ],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 12,
            "text": "В каком году был основан Эрмитажный театр?",
            "type": "open"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 12,
                    "points": 3.0,
                    "text": ""
                }
            ],
            "files": [],
            "hints": [],
            "movements": [
                {
                    "next_question_id": 12,
                    "place": {
                        "coords": "(59.942345,30.316612)",
                        "radius": 15.6,
                        "time_close": "Sun, 12 Aug 2001 19:00:00 GMT",
                        "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
                    }
                }
            ],
            "question_id": 11,
            "text": "Двиньтесь к Эрмитажному театру",
            "type": "movement"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 11,
                    "points": 10.0,
                    "text": "1764—1775"
                }
            ],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 8,
            "text": "В какие годы строился Малый Эрмитаж? Укажите годы через дефис.",
            "type": "open"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 8,
                    "points": 3.0,
                    "text": ""
                }
            ],
            "files": [],
            "hints": [],
            "movements": [
                {
                    "next_question_id": 8,
                    "place": {
                        "coords": "(59.940742,30.316448)",
                        "radius": 15.7,
                        "time_close": "Sun, 12 Aug 2001 19:00:00 GMT",
                        "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
                    }
                }
            ],
            "question_id": 5,
            "text": "Двиньтесь к Малому Эрмитажу",
            "type": "movement"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 11,
                    "points": 10.0,
                    "text": "1771—1787"
                }
            ],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 9,
            "text": "В какие годы строился Большой Эрмитаж? Укажите годы через дефис.",
            "type": "open"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 9,
                    "points": 3.0,
                    "text": ""
                }
            ],
            "files": [],
            "hints": [],
            "movements": [
                {
                    "next_question_id": 9,
                    "place": {
                        "coords": "(59.942178,30.316193)",
                        "radius": 50.3,
                        "time_close": "Sun, 12 Aug 2001 20:00:00 GMT",
                        "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
                    }
                }
            ],
            "question_id": 6,
            "text": "Двиньтесь к Большому Эрмитажу",
            "type": "movement"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 11,
                    "points": 10.0,
                    "text": "1842—1851"
                }
            ],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 10,
            "text": "В какие годы строился Новый Эрмитаж? Укажите годы через дефис.",
            "type": "open"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 10,
                    "points": 3.0,
                    "text": ""
                }
            ],
            "files": [],
            "hints": [],
            "movements": [
                {
                    "next_question_id": 10,
                    "place": {
                        "coords": "(59.941711,30.316884)",
                        "radius": 48.0,
                        "time_close": "Sun, 12 Aug 2001 19:00:00 GMT",
                        "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
                    }
                }
            ],
            "question_id": 7,
            "text": "Двиньтесь к Новому Эрмитажу",
            "type": "movement"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 5,
                    "points": -1.0,
                    "text": "1"
                },
                {
                    "next_question_id": 6,
                    "points": -1.0,
                    "text": "2"
                },
                {
                    "next_question_id": 7,
                    "points": 3.0,
                    "text": "3"
                }
            ],
            "files": [
                {
                    "type": "image",
                    "url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Elizabeth_of_Russia_by_V.Eriksen.jpg"
                },
                {
                    "type": "image",
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Mikola_II_%28cropped%29-2.jpg/548px-Mikola_II_%28cropped%29-2.jpg"
                },
                {
                    "type": "image",
                    "url": "https://azbyka.ru/days/storage/images/icons-of-saints/2280/p1ann1j7utlc61pgcs2p1gle1olc4.jpg"
                }
            ],
            "hints": [],
            "movements": [],
            "question_id": 4,
            "text": "На каком из представленых изображений находится правитель России по указу которого был построен Русский музей?",
            "type": "choice"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 4,
                    "points": -5.0,
                    "text": "Андрей Воронихин"
                },
                {
                    "next_question_id": 4,
                    "points": -5.0,
                    "text": "Огюст Монферран"
                },
                {
                    "next_question_id": 4,
                    "points": 5.0,
                    "text": "Франческо Растрелли"
                },
                {
                    "next_question_id": 4,
                    "points": -5.0,
                    "text": "Карл Росси"
                }
            ],
            "files": [],
            "hints": [],
            "movements": [],
            "question_id": 3,
            "text": "Кто архитектор?",
            "type": "choice"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 3,
                    "points": 10.0,
                    "text": "1754"
                }
            ],
            "files": [],
            "hints": [
                {
                    "files": [],
                    "fine": 1.0,
                    "hint_text": "Здание основано в шестидесятые годы 18 века."
                }
            ],
            "movements": [],
            "question_id": 2,
            "text": "В каком году был основан Зимний дворец?",
            "type": "open"
        },
        {
            "answer_options": [
                {
                    "next_question_id": 2,
                    "points": 0.0,
                    "text": ""
                }
            ],
            "files": [],
            "hints": [],
            "movements": [
                {
                    "next_question_id": 2,
                    "place": {
                        "coords": "(59.940925,30.312946)",
                        "radius": 26.5,
                        "time_close": "Sun, 12 Aug 2001 19:00:00 GMT",
                        "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
                    }
                }
            ],
            "question_id": 1,
            "text": "Идите к Зимнему Дворцу",
            "type": "start"
        }
    ],
    "rating": {
        "five": 0,
        "four": 0,
        "one": 0,
        "three": 0,
        "two": 0
    },
    "start_question_id": 1,
    "tags": [
        "educational",
        "historical"
    ],
    "time_close": "Sat, 01 Jan 2022 00:00:00 GMT",
    "time_open": "Sat, 01 Jan 2011 00:00:00 GMT",
    "title": "По залам Эрмитажа"
}
```
   
## POST
Create new entity with params encountered in JSON.
Return JSON with id of created entity.

###Quest is created especially:

`POST api/quest`

Returned JSON also contains first answer id

### Other according to general schema: 
`api/to/{to_id}/what/[?id=what_id]`

(what_id if it has already been created, so without JSON body)

#### Question
* `POST api/answer_option/{answer_option_id}/question/[?id={question_id}]`

or

* `POST api/movement/{movement_id}/question/[?id={question_id}]`
#### Hint
* `POST api/question/{question_id}/hint/[?id={hint_id}]`
#### File
* `POST api/quest|question|answer|hint/{id}/file/[?id={file_id}]`
#### Answer option
* `POST api/question/{question_id}/answer_option/[?id={answer_option_id}]`
#### Movement
* `POST api/answer/{answer_id}/movement/[?id={movement_id}]`
#### Place
* `POST api/movement/{movement_id}/place/[?id={place_id}]`

Example:
request `POST api/question/1/answer_option` with body
```json
{
  "option_text": "answer",
  "points": 10
}
```
adds answer to the question with `id` = 1. If success,
the server answer will have status code `200 OK` and body
```json
{
  "answer_option_id": 7
}
```
`7` is created answer option id.

## PUT
Update entity (add or change fields).

General schema:
`PUT api/entity/{entity_id}`

with body that contains JSON with fields, that will be changed.

Example:
`PUT api/answer_option/7`
with body
```json
{
  "option_text": "new text"
}
```
will change option text in answer option with `id` = 7.

## DELETE
Delete entity.

General schema: `DELETE api/entity/{entity_id}`.

* If the entity is quest, all information will be deleted.
* If the entity is question then related answers, hints and
movements will be deleted.
* If the entity is  movement then related place 
will be deleted.
* If the entity is answer or movement, quest graph
can become disconnected.
* With deletion of quest, questions or hints related files 
will be deleted too.