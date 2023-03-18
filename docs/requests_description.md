# catalog
  - /quests/\<int:quest_id\> GET - get a quest from the catalog using id
  - /quests GET - get all quests from the catalog
  - /tags GET - get all tags
  - /quests/amount GET - get quests amount 

# constructor
  - /quest/\<int:quest_id\> GET - get quest in json format using id  
  - /quest POST - create new quest using json description
  - /question_block POST - create new question block using json description and get its id in current quest
  - /movement_block POST - create new movement block using json description and get its id in current quest
  - /information_block POST - create new information block (start, end, message) using json description and get its id in current quest
  - /answer_host/\<int:host_id\>/answer_id/\<int:answer_id\>/block/\<int:block_id\> PUT - connect question answer and block  
    &emsp; host_id - answer block host id  
    &emsp; answer_id - answer id in block host  
    &emsp; block_id - connection block id
  - /source_block/\<int:source_id\>/target_block/\<int:target_id\> PUT - connect two blocks  
    &emsp; source_id - source block id  
    &emsp; target_id - target block id  
  - /media/block/\<int:block_id\> POST - create new media using json description and add it to the block    
    &emsp; block_id - block to which is added media  
    &emsp; return - media id  
  - /media/block/\<int:block_id\>/hint/\<int:hint_id\> POST - create media using json description and add it to hint  
    &emsp; block_id - hint block host id  
    &emsp; hint_id - hint id in block host  
    &emsp; return - medit id in hint  
  - /answer_option/question/\<int:question_id\> POST - create new answer in question block  
    &emsp; question_id - question id to which the answer is added  
    &emsp; return - answer id  
  - /hint/block/\<int:block_id\> POST - create new hint and add it to block  
    &emsp; block_id - block id to which the hint is added  
    &emsp; return - hint id  
  - /place/movement_block/\<int:block_id\> POST - create new place and add it to movement block  
    &emsp; block_id - block id to which the place is added    
    &emsp; return - place id  
  - /block/\<int:block_id\> PUT - update block's attributes from json  
    &emsp; block_id - block id to which attributes updating  
    &emsp; return - status code  
  - /block/\<int:block_id\>/media/\<int:media_id\> PUT - update media attributes from json  
    &emsp; block_id - block containing media  
    &emsp; media_id - media id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/hint/\<int:hint_id\>/media/\<int:media_id\> PUT - Set block media attributes from JSON  
    &emsp; block_id - block containing hint  
    &emsp; hint_id - hint id  
    &emsp; media_id - media id  
    &emsp; return status code  
  - /block/\<int:block_id\>/answer/\<int:answer_id\> PUT - Set question block answer attributes from JSON  
    &emsp; block_id - block containing answer  
    &emsp; answer_id - answer id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/hint/\<int:hint_id\> PUT - Set hint media attributes from JSON  
    &emsp; block_id - block containing hint  
    &emsp; hint_id - answer id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/place/\<int:place_id\> PUT - Set movement block place attributes from JSON  
    &emsp; block_id - block containing answer  
    &emsp; place_id - place id  
    &emsp; return - status code  
  - /quest PUT - Set quest attributes from JSON  
    &emsp; return - status code  
  - /block/\<int:block_id\> DELETE - Remove block from quest  
    &emsp; block_id - block id
    &emsp; return - status code  
  - /block/\<int:block_id\>/media/\<int:media_id\> DELETE - Remove media from block  
    &emsp; block_id - block containing media  
    &emsp; media_id - media id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/hint/\<int:hint_id\>/media/\<int:media_id\> DELETE - Remove media from hint  
    &emsp; block_id - block containing hint  
    &emsp; hint_id - hint id  
    &emsp; media_id - media id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/answer/\<int:answer_id\> DELETE - Remove answer from question block  
    &emsp; block_id - block containing media  
    &emsp; answer_id - answer id  
    &emsp; return - status code  
  - /block/\<int:block_id\>/hint/\<int:hint_id\> DELETE - Remove hint from block  
    &emsp; block_id - block containing hint  
    &emsp; hint_id - hint id  
    &emsp; return - status code  
  - /answer_host/\<int:host_id\>/answer_id/\<int:answer_id\> PUT - Unlink answer and its next block  
    &emsp; host_id - block containing answer  
    &emsp; answer_id - answer id  
    &emsp; return - status code  
  - /source_block/\<int:source_id\> PUT - Unlink two blocks
    &emsp; source_id - block containing next block  
    &emsp; return - status code  
  - /save/\<int:quest_id\> POST - Save quest in database and remove from drafts  
    &emsp; quest_id - quest for deleting  
    &emsp; return - status code  

# personal_catalog
  - /quest/\<int:quest_id\> DELETE - delete quest from catalog  
    &emsp; quest_id - quest for deleting  
    &emsp; return - status code  

