# API description
For simplicity, answers can contain only this status codes:
* `200 OK` if success;
* `400 Bad Request` if there is request syntax or logic error (body contains error message);
* `500 Internal Server Error` if server error.

## GET
* `GET api/quest/{quest_id}`

    Load or create draft of quest.
Return JSON with information about quest ([example](example.md)).

## POST
* Create new entity with params encountered in JSON 
  (**body must contain at least empty JSON, some 
  entities have required attributes**). 
  [List of available JSON attributes](available_attrs.md).

  General schema:
  `POST api/{entity}`, where `entity` is:
  * `quest`
  * `question`
  * `hint`
  * `answer_option`
  * `movement`
  * `place`
  * `file`

  `POST api/quest` return the same JSON as `GET api/db/quest/<id>`.
  Other return JSON with id of created entity, e.g.:
  ```json
  {
    "answer_option_id": 23
  }
  ```
  
* Save quest to database and delete from drafts:

    `api/save/{quest_id}`

### PUT
* Update entity attributes:

    `PUT api/entity/{entity_id}`
    
    Request body must contain JSON with updating 
attributes ([list of available JSON attributes](available_attrs.md)).
Returns `200 OK` if success or status code with error message.
    
  **!!!To update quest, you may use any id, it doesn't matter.
        Reason? There is no reason - it's hack. It will be fixed later!!!**
* Add connection between entities
  (add `entity_what` to `entity_to`):
    `api/entity_to/{to_id}/entity_what/{what_id}`

    (what_id is id of entity created before with `POST` request).
    
    It's possible to add:
    * `question` to `answer_option`
    * `question` to `movement`
    * `file` to `quest`, `question`, `hint`, **here you may also use any quest id**
    * `answer_option` to `question`
    * `movement` to `question`
    * `hint` to `question`
    * `place` to `movement`
  
## DELETE
* Delete entity.

  General schema: `DELETE api/entity/{entity_id}`.

  * **You can't delete quest this way**.
  * If the entity is question then related hint and files will be deleted.
  * If the entity is  movement then related place 
  will be deleted.
  * If the entity is question, answer or movement, quest graph
  can become disconnected.
  * With deletion of quest, question or hint related files 
  will be deleted too.

* Delete connection
  * `DELETE api/answer_option/{answer_id}/question` - 
  delete next question for answer
  * `DELETE api/mvoement/{movement_id}/question` - 
  delete next question for movement
  * `DELETE api/question/{question_id}/movement/{movement_id}`-
  delete movement with `movement_id` from question's movements
  * `DELETE api/question/{question_id}/answer_option/{answer_id}`-
  delete answer with `answer_id` from question's answers