# [Personal catalog](#personal-catalog)
  - `api/personal_catalog/quest/\<int:quest_id\> DELETE` - delete quest from catalog  
    &emsp; **:param quest_id:** quest for deleting  
    &emsp; **:return:** status message and code:  
    &emsp; &emsp; ("", 200) - success    
    &emsp; &emsp; ("This is not your quest", 403) - failed  