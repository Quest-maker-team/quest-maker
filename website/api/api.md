# API description
For simplicity, answers can contain only this status codes:
* `200 OK` if success;
* `400 Bad Request` if there is request syntax error;
* `500 Internal Server Error` if server error.

## GET
Return JSON with entity data 
### Quest
* `GET api/quest/{quest_id}`
### Question
* `GET api/question/{question_id}`

... and other database entities.
   
## POST
Create new entity with params encountered in JSON.
Return JSON with id of created entity.

###Quest is created especially:
### Quest
* `POST api/quest`
Returned JSON also contains first answer id

### Other according to general schema: 
`api/to/what/{to_id}/[?id=what_id]`

(what_id if it has already been created, so without JSON body)
### Tag
* `POST api/quest/tag/{question_id}/[?id={tag_id}]`
### Question
* `POST api/answer/question/{answer_id}/[?id={question_id}]`
### Hint
* `POST api/question/hint/{question_id}/[?id={hint_id}]`
### File
* `POST api/quest|question|answer|hint/{id}/[?id={file_id}]`
### Answer
* `POST api/question/answer/{question_id}/[?id={answer_id}]`
### Movement
* `POST api/answer/movement/{answer_id}/[?id={movement_id}]`
### Place
* `POST api/movement/place/{movement_id}/[?id={place_id}]`
## PUT
### Question 
* `PUT api/quest/{quest_id}`

... and other database entities

## DELETE
* `DELETE api/quest/{quest_id}`

... and other database entities