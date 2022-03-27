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
field `start_qustion_id` and array `tags`, array 
and also arrays `questions`, `answer_options`, `movements`
and `files` with info about related entities
(**but with values instead of values ids, e.g. `q_type` 
instead of `q_type_id`**).

If quest is public, JSON has `password` field with empty string.

`quest` `question`, `hint`, `answer` objects also contain array
`files` of file objects.

`question` objects contain arrays `hints`, 
`answer_option_ids`, `movements_ids`.

`hint` objects contain fields `hint_text`, `fine`
and array `file` of file objects

`movement` objects contain array `places` of place objects.

Returned JSON example:
```json
{
  "quest_id": 0,
  "title": "Example",
  "author": "some author",
  "description": "This is example quest",
  "tags": ["example", "test"],
  "password": "12345abc",
  "hidden": true,
  "files": [
    {
      "f_id": 1, 
      "url_for_file": "www.files.com/files/228.jpg",
      "f_type": "image"
    }
  ],
  "time_open": "2011-01-01 00:00:00",
  "time_close": "2022-01-01 00:00:00",
  "lead_time": "6 months",
  "start_question_id": 0,
  "questions": [
    {
      "question_id": 0,
      "question_text": "",
      "q_type": "start",
      "answer_options_ids": [0],
      "movements_ids": [],
      "files": [],
      "hints": []
    },
    {
      "question_id": 1,
      "question_text": "first question",
      "q_type": "choice",
      "answer_options_ids": [1],
      "movements_ids": [],
      "files": [],
      "hints": [
        {
          "hint_id": 1,
          "hint_text": "hint",
          "fine": 5,
          "files": []
        }
      ]
    },
    {
      "question_id": 2,
      "question_text": "",
      "q_type": "end",
      "answer_option_ids": [],
      "movement_ids": [],
      "files": [],
      "hints": []
    }
  ],
  "answer_options": [
    {
      "option_id": 0,
      "option_text": "",
      "points": 0,
      "next_question_id": 1
    },
    {
      "option_id": 1,
      "option_text": "right answer",
      "points": 10,
      "next_question_id": 2
    }
  ]
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