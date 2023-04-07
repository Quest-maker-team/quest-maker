# [Catalog](#catalog)
  - `api/catalog/quests/<int:quest_id> GET` - get a quest from the catalog using id  
    &emsp; **:param quest_id:** quest id  
    &emsp; **:return:**  
    &emsp; &emsp; if success return quest in json format :   
    ```json
    {  
      "quest_id": 0,  
      "title": "title",  
      "author": "author_name",  
      "description": "description",  
      "keyword": "12345678",  
      "rating": {
        "one": 0,
        "two": 0,
        "three_": 0,
        "four": 0,
        "five": 10
      },  
      "cover_path": "path"  
    }
    ```  
    &emsp; &emsp; else return status message and code:  
    &emsp; &emsp; &emsp; ("Not Found", 400) - failed

  - `api/catalog/quests GET` - get all quests from the catalog  
      &emsp; **:request_arg title:** quests title pattern  
      &emsp; **:request_arg description:** quests description pattern  
      &emsp; **:request_arg limit:** maximum number of selected quests  
      &emsp; **:request_arg offset:** start receiving quests from the array  
      &emsp; **:request_arg sort_by:** by which column to sort the array ("id", "rating", "title")  
      &emsp; **:request_arg order_by:** sort ascending or descending ("DESC", "ASC")  
      &emsp; **:request_arg author:** author name  
      &emsp; **:request_arg tags:** list with tags   
      &emsp; **:return:** total number of quests and array of quests in json format the same as returned from `api/catalog/quests/<int:quest_id> GET`:
      ```json
      {
        "quests": [
          {
            ...
          },
          {
            ...
          }
        ],
        "total": 4
      }
      ```

  - `api/catalog/tags GET` - get all tags  
      &emsp; **:return:** array of tags in json format:  
      ```json
      {  
        "tags": ["tag1", "tag2"]  
      }  
      ```

  - `api/catalog/quests/amount GET` - get quests amount  
      &emsp; **:return:** number of quests:  
      ```json
      {  
        "quests_amount": 10  
      }  
      ```