# Catalog API
All requests return `200 OK` if success else `400 Bad Request` with info about error in body.
* `GET api/catalog/quests/{id}` - get quest by id.
    
    Return JSON with quest info. Example:
    ```json
    {
      "quest_id": 0,
      "title": "Не самые популярные достопримечательности Петербурга",
      "author": "Экскурсии",
      "description": "Это небольшой квест-экскурсия по малоизвестным местам Петербурга. Он содержит простые вопросы и несколько удаленных друг от друга мест, которые нужно посетить. Часть мест являются музеями и имеют свой режим работы.",
      "cover_url": "cover-url.cock",
      "files": [
        {
          "f_type": "image",
          "url_for_file": "file-url.cock"
        }
      ],
      "keyword": "12345678",
      "rating": {
        "one": 0,
        "two": 0,
        "three_": 0,
        "four": 0,
        "five": 1000
      },
      "tags": ["excursion"],
      "time_open": "",
      "time_close": ""
    }
    ```

* `GET api/catalog/quests`
    
    Return JSON with total of quests (excluding `limit` and `offset`) 
and list `quests` where each quest is object the same as returned from `GET api/catalog/quests/{id}`. Example:
    ```json
    {
      "quests": [
        {
          "quest_id": 0,
          "title": "Не самые популярные достопримечательности Петербурга",
          ...
        },
        {
          "quest_id": 1,
          "title": "Ещё один квест",
          ...
        }
      ]
      "total": 4
    }
    ```
   
    Parameters:
  * `limit` and `offset` - limit of number of quests and offset from start. Default values `100` and `0`. Max limit is `500`.
  * `sort_by` - sort key. Possible keys: `title`, `rating`. Default key is `id`.
  * `orber_by` - sort order. Possible values: `asc`, `desc` - ascending and descending.
  * `author` - name of author
  * `tags` - tags for search. To search using multiple tags just repeat this param.
  
* `GET api/catalog/tags` - return list of tags.
  ```json
  {
    "tags": []
  }
  ```

* `GET api/catalog/quests/amount` - return number of quests
  ```json
    {
      "quests_amount": 100
    }
  ```