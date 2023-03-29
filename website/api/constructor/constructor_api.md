# [Constructor](#constructor)
## [GET requests](#get-requests)
  - `api/constructor/quest/\<int:quest_id\> GET` - get quest in json format using id  
    &emsp; **:param quest_id:** quest id  
    &emsp; **:return:** quest in json format: [see example](json_example.md)  

## [POST requests](#post-requests)
  - `api/constructor/quest POST` - create new quest using json description  
    &emsp; **:request_arg quest_dict:** quest description in json format:  
    ```json
    {  
      "title": "title", //required parameter  
      "description": "description", //optional parameter  
      "keyword": "12345678", //required parameter  
      "password": "e2413rw", //optional parameter  
      "cover_path": "path", //optional parameter  
      "hidden": false, //required parameter  
      "published": false //required parameter    
    }   
    ```
    &emsp; **:return:** quest in json format: [see example](json_example.md)  

  - `api/constructor/save/\<int:quest_id\> POST` - Save quest in database and remove from drafts  
    &emsp; **:param quest_id:** quest id for saving  
    &emsp; **:return:** status message and code:  
    &emsp; &emsp; ("", 200) - success    
    &emsp; &emsp; ("No quest with this id"), 400 - failed   
    &emsp; &emsp; ("This is not your quest"), 403 - failed   

### [Blocks creation](#blocks-creation)
  - `api/constructor/block POST` - create new block using json description and get its id in current quest  
    &emsp; **:request_arg block_dict:** block description in json format:  
    ```json
    {  
      "block_text": "text", //required parameter
      "block_type_name": "open_question", //required parameter
      "pos_x": 100, //optional paramter
      "pos_y": 100, //optional paramter
    }  
    ```
    &emsp; **:return:** created block id in json format:
    ```json
    {"block_id": 1}
    ```
    &emsp; **posible block type name:** "open_question", "choice_question", "movement", "message", "start_block", "end_block"
    
### [Media, answer, hint, place creation](#media-answer-hint-place-creation)
  - `api/constructor/media/block/\<int:block_id\> POST` - create new media using json description and add it to the block    
    &emsp; **:param block_id:** - block to which is added media  
    &emsp; **:request_arg media_dict:** - media description in json format:
    ```json
      {
        "media_path": "path", //required parameter
        "media_type_name": "audio" //required parameter
      }
    ```
    &emsp; **:return:** - media id if media created:
    ```json
    {"media_id": 0}
    ```  
    else return status message and code:  
    &emsp; 'Wrong block id', 400  
    &emsp; 'Wrong JSON attributes', 400

  - `api/constructor/media/block/\<int:block_id\>/hint/\<int:hint_id\> POST` - create media using json description and add it to hint  
    &emsp; **:param block_id:** - hint block host id  
    &emsp; **:param hint_id:** - hint id in block host  
    &emsp; **:request_arg media_dict:** - media description in json format:
    ```json
    {
      "media_path": "path", //required parameter
      "media_type_name": "audio" //required parameter
    }
    ```
    &emsp; **:return:** - media id in hint if media created:  
    ```json
    {"media_id": 1}
    ```  
    else return status message and code:  
    &emsp; 'Wrong hint id', 400  
    &emsp; 'Wrong block id', 400  
    &emsp; 'Wrong JSON attributes', 400

  - `api/constructor/answer_option/block/\<int:block_id\> POST` - create new answer in question block  
    &emsp; **:param block_id:** - question id to which the answer is added  
    &emsp; **:request_arg answer_dict:** - answer description in json format:
    ```json
      {
        "text": "text", //required parameter
        "points": 10 //optional parameter
      }
    ```
    &emsp; **:return:** - answer id if answer created:
    ```json
    {"answer_option_id": 2}
    ```  
    else return status message and code:  
    &emsp; 'Wrong block id', 400  
    &emsp; 'Wrong JSON attributes', 400  
    
  - `api/constructor/hint/block/\<int:block_id\> POST` - create new hint and add it to block  
    &emsp; **:param block_id:** - block id to which the hint is added  
    &emsp; **:request_arg hint_dict:** - hint description in json format:  
    ```json
      {
        "hint_text": "text", //required parameter
        "fine": 10 //optional parameter
      }
    ```
    &emsp; **:return:** - hint id if hint created:
    ```json
      {"hint_id": 1}
    ```
    else return status message and code:  
    &emsp; 'Wrong block id', 400  
    &emsp; 'Wrong JSON attributes', 400  
  
  - `api/constructor/place/movement_block/\<int:block_id\> POST` - create new place and add it to movement block  
    &emsp; **:param block_id:** - block id to which the place is added    
    &emsp; **:request_arg place_dict:** - place description in json format:  
    ```json
      {
        "latitude": 100, //required parameter
        "longitude": 100, //required parameter
        "radius": 100, //required parameter
      }
    ```
    &emsp; **:return:** - place id if place created:
    ```json
      {"place_id": 0}
    ```
    else return status message and code:  
    &emsp; 'Wrong block id', 400  
    &emsp; 'Wrong JSON attributes', 400  

## [PUT requests](#put-requests)
  - `api/constructor/answer_host/\<int:host_id\>/answer_id/\<int:answer_id\>/block/\<int:block_id\> PUT` - connect question answer and block  
    &emsp; **:param host_id:** - answer block host id  
    &emsp; **:param answer_id:** - answer id in block host  
    &emsp; **:param block_id:** - connection block id  
    &emsp; **:return:** - status message and code  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong answer id', 400) - failed  
    &emsp; ('Wrong host_block id', 400) - failed  

  - `api/constructor/source_block/\<int:source_id\>/target_block/\<int:target_id\> PUT` - connect two blocks  
    &emsp; **:param source_id:** - source block id  
    &emsp; **:param target_id:** - target block id  
    &emsp; **:return:** - status message and code  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong source id', 400) - failed  
    &emsp; ('Wrong target id', 400) - failed  

  - `api/constructor/block/\<int:block_id\> PUT` - update block's attributes from json  
    &emsp; **:param block_id:** - block id to which attributes updating  
    &emsp; **:request_arg block_dict:** - block description in json format:  
    ```json
    {  
      "block_text": "text", //optional parameter
      "block_type_name": "movement", //optional parameter
      "pos_x": 100, //optional paramter
      "pos_y": 100, //optional paramter
    }  
    ```
    &emsp; **:return:** - status message and code  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed   

  - `api/constructor/block/\<int:block_id\>/media/\<int:media_id\> PUT` - update block's media attributes from json  
    &emsp; **:param block_id:** - block containing media  
    &emsp; **:param media_id:** - media id  
    &emsp; **:request_arg media_dict:** - media description in json format:
    ```json
      {
        "media_path": "path", //optional parameter
        "media_type_name": "audio" //optional parameter
      }
    ```
    &emsp; **:return:** - status message and code:    
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong media id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed  

  - `api/constructor/block/\<int:block_id\>/hint/\<int:hint_id\>/media/\<int:media_id\> PUT` - Set block media attributes from JSON  
    &emsp; **:param block_id:** - block containing hint  
    &emsp; **:param hint_id:** - hint id  
    &emsp; **:param media_id:** - media id  
    &emsp; **:request_arg media_dict:** - media description in json format:  
    ```json
      {
        "media_path": "path", //optional parameter
        "media_type_name": "audio" //optional parameter
      }
    ```
    &emsp; **:return:** status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong hint id', 400) - failed  
    &emsp; ('Wrong media id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed  

  - `api/constructor/block/\<int:block_id\>/answer_option/\<int:answer_id\> PUT` - Set question block answer attributes from JSON  
    &emsp; **:param block_id:** - block containing answer  
    &emsp; **:param answer_id:** - answer id  
    &emsp; **:request_arg answer_dict:** - answer description in json format:  
    ```json
      {
        "text": "text", //optional parameter
        "points": 10 //optional parameter
      }
    ```
    &emsp; **:return:** - status message and code   
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong answer id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed  

  - `api/constructor/block/\<int:block_id\>/hint/\<int:hint_id\> PUT` - Set hint attributes from JSON  
    &emsp; **:param block_id:** - block containing hint  
    &emsp; **:param hint_id:** - answer id
    &emsp; **:request_arg hint_dict:** - hint description in json format:  
    ```json
      {
        "hint_text": "text", //optional parameter
        "fine": 10 //optional parameter
      }
    ```
    &emsp; **:return:** - status message and code:    
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong hint id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed  

  - `api/constructor/block/\<int:block_id\>/place/\<int:place_id\> PUT` - Set movement block place attributes from JSON  
    &emsp; **:param block_id:** - block containing answer  
    &emsp; **:param place_id:** - place id
    &emsp; **:request_arg place_dict:** - place description in json format  
    ```json
      {
        "latitude": 100, //optional parameter
        "longitude": 100, //optional parameter
        "radius": 100, //optional parameter
      }
    ```
    &emsp; **:return:** - status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed  
    &emsp; ('Wrong place id', 400) - failed  
    &emsp; ('Wrong JSON attributes', 400) - failed   

  - `api/constructor/quest PUT` - Set quest attributes from JSON  
    &emsp; **:request_arg quest_dict:** - quest description in json format:  
    ```json
      {
        "title": "title", //optional parameter  
        "description": "description", //optional parameter  
        "keyword": "12345678", //optional parameter  
        "password": "e2413rw", //optional parameter  
        "cover_path": "path", //optional parameter  
        "hidden": false, //optional parameter  
        "published": false //optional parameter 
      }
    ```
    &emsp; **:return:** - status message and code:   
    &emsp; ('', 200) - success  
    &emsp; ('Wrong JSON attributes', 400) - failed   

  - `api/constructor/answer_host/\<int:host_id\>/answer_id/\<int:answer_id\> PUT` - Unlink answer and its next block  
    &emsp; **:param host_id:** - block containing answer  
    &emsp; **:param answer_id:** - answer id  
    &emsp; **:return:** - status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong host_block id', 400) - failed   
    &emsp; ('Wrong answer id', 400) - failed   

  - `api/constructor/source_block/\<int:source_id\> PUT` - Unlink two blocks
    &emsp; **:param source_id:** - block containing next block  
    &emsp; **:return:** - status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong source id', 400) - failed   

## [DELETE requests](#delete-requests)
  - `api/constructor/block/\<int:block_id\> DELETE` - Remove block from quest  
    &emsp; **:param block_id:** - block id
    &emsp; **:return:** - status message and code:   
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed   

  - `api/constructor/block/\<int:block_id\>/media/\<int:media_id\> DELETE` - Remove media from block  
    &emsp; **:param block_id:** - block containing media  
    &emsp; **:param media_id:** - media id  
    &emsp; **:return:** - status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed   
    &emsp; ('Wrong media id', 400) - failed   

  - `api/constructor/block/\<int:block_id\>/hint/\<int:hint_id\>/media/\<int:media_id\> DELETE` - Remove media from hint  
    &emsp; **:param block_id:** - block containing hint  
    &emsp; **:param hint_id:** - hint id  
    &emsp; **:param media_id:** - media id  
    &emsp; **:return:** - status message and code:  
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed   
    &emsp; ('Wrong hint id', 400) - failed   
    &emsp; ('Wrong media id', 400) - failed   

  - `api/constructor/block/\<int:block_id\>/answer_option/\<int:answer_id\> DELETE` - Remove answer from question block  
    &emsp; **:param block_id:** - block containing media  
    &emsp; **:param answer_id:** - answer id  
    &emsp; **:return:** - status message and code:    
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed   
    &emsp; ('Wrong answer id', 400) - failed   

  - `api/constructor/block/\<int:block_id\>/hint/\<int:hint_id\> DELETE` - Remove hint from block  
    &emsp; **:param block_id:** - block containing hint  
    &emsp; **:param hint_id:** - hint id  
    &emsp; **:return:** - status message and code:    
    &emsp; ('', 200) - success  
    &emsp; ('Wrong block id', 400) - failed   
    &emsp; ('Wrong hint id', 400) - failed  


