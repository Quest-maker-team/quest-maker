# Database description
Description of the database structure for the Quest maker project, SPbPU 2022.

You can also get acquainted with the scheme of the database in the form of an [image](https://github.com/Quest-maker-team/quest-maker/blob/main/docs/image/db.png).

## Tables in the database
+ <a href = "#author">Author</a> - data required for authorization of users of the web component of the project.
+ <a href = "#status">Author's Status</a> - types of authorized users.
+ <a href = "#quest">Quest</a> - general information about the quest.
+ <a href = "#place">Place</a> - a certain geographical point that is part of the quest.
+ <a href = "#directions">Directions</a> - possible ways to continue the quest with a tree structure.
+ <a href = "#question">Question</a> - a task tied to a specific location.
+ <a href = "#qtype">Question Type</a> - types of tasks.
+ <a href = "#answer">Answer</a> - correct answers provided by the task author.
+ <a href = "#possibleAns">Possible Answers</a> - answer options provided by the author of the task.
+ <a href = "#hints">Hints</a> - hints linked to a specific task.
+ <a href = "#files">Files</a> - additional files for elements such as quest, location, question, hint, answer or possible answer.
+ <a href = "#otype">Object Type</a> - types of objects to which an additional file can be mapped.
+ <a href = "#user">User</a> - data of telegram bot users.
+ <a href = "#history">History</a> - the history of completing quests by telegram bot users.

## Detailed description of each table
<b>Note</b>: required fields are highlighted in <b>bold</b>.

<b>Note</b>: fields with unique values <i>are italicized</i>.

### <a name = "author"></a>Author
Fields:
+ <b><i>id</i></b> - the unique identifier assigned to the site user. Assumed data type: serial.
+ <b><i>login</i></b> - the unique user name of the site. Assumed data type: varchar.
+ <b>hash_password</b> - hash of the site user's password. Assumed data type: bytea.
+ <b>email</b> - the site user's email address. Assumed data type: varchar.
+ <b>status_id</b> - ID of the site user status. Assumed data type: integer.

Links to other tables:
1. id (from <a href = "#status">Author's Status</a>) -> status_id. Type: one-to-many.
2. id -> author_id (form <a href = "#quest">Quest</a>). Type: one-to-many.

### <a name = "status"></a>Author's Status
Fields:
+ <b><i>id</i></b> - the unique identifier for the site user status. Assumed data type: serial.
+ <b><i>status</i></b> - string status designation for convenient configuration. Assumed data type: varchar.

Links to other tables:
1. id -> status_id (from <a href = "#author">Author</a>). Type: one-to-many.

### <a name = "quest"></a>Quest
Fields:
+ <b><i>id</i></b> - the unique identifier for the quest. Assumed data type: serial.
+ <b>title</b> - name of the quest. Assumed data type: varchar.
+ <b>author_id</b> - ID of the author of this quest. Assumed data type: integer.
+ description - description of the quest provided by the author. Assumed data type: text.
+ key_word - keyword for access to private quests. Assumed data type: varchar.
+ tags - tags for quest search. Assumed data type: text.
+ time_open - date and time of the quest opening. Assumed data type: timestamp.
+ time_close - date and time of closing the quest. Assumed data type: timestamp.
+ lead_time - time limit for passing. Assumed data type: interval.

<b>Note</b>: the ability to interrupt quests with a time limit (if the lead_time field is not empty) is <b>not provided</b>.

Links to other tables:
1. id -> quest_id (from <a href = "#place">Place</a>). Type: one-to-many.
2. id -> quest_id (from <a href = "#history">History</a>). Type: one-to-many.
3. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
4. id (from <a href = "#author">Author</a>) -> author_id. Type: one-to-many.

### <a name = "place"></a>Place
Fields:
+ <b><i>id</i></b> - the unique identifier of the entry. Assumed data type: serial.
+ place_name - the name of the place provided by the author. Assumed data type: varchar.
+ coord - geographical coordinates of the place. Assumed data type: point.
+ <b>quest_id</b> - ID of the quest that the place belongs to. Assumed data type: integer.
+ description - description of the place provided by the author. Assumed data type: text.
+ time_open - opening time of the place. Assumed data type: timestamp.
+ time_close - closing time of the place. Assumed data type: timestamp.
+ points - the number of points received by the user for visiting the place. Assumed data type: float.
+ fine - the number of points deducted for skipping the place. Assumed data type: float.
+ radius - the distance (m) within which the task is activated when using geolocation. Assumed data type: float.

Links to other tables:
1. id -> place_id (from <a href = "#question">Question</a>). Type: one-to-many.
2. id -> last_place_id (from <a href = "#history">History</a>). Type: one-to-many.
3. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
4. id -> cur_place_id (from <a href = "#directions">Directions</a>). Type: one-to-many.
5. id -> next_place_id (from <a href = "#directions">Directions</a>). Type: one-to-many.
6. id (from <a href = "#quest">Quest</a>) -> quest_id. Type: one-to-many.

### <a name = "directions"></a>Directions
Fields:
+ <b><i>id</i></b> - the unique identifier of the entry. Assumed data type: serial.
+ <b>cur_place_id</b> - ID of the location from which the movement originates. Assumed data type: integer.
+ <b>next_place_id</b> - ID of the destination. Assumed data type: integer.
+ description - description provided by the author of the quest for this direction. Assumed data type: text.

Links to other tables:
1. id (from <a href = "#place">Place</a>) -> cur_place_id. Type: one-to-many.
2. id (from <a href = "#place">Place</a>) -> next_place_id. Type: one-to-many.

### <a name = "question"></a>Question
Fields:
+ <b><i>id</i></b> - the unique identifier of the task. Assumed data type: serial.
+ <b>place_id</b> - ID of the place the task is linked to. Assumed data type: integer.
+ question_text - task text. Assumed data type: text.
+ points - the number of points received by the user for completing the task. Assumed data type: float.
+ fine - the number of points deducted for skipping a task. Assumed data type: float.
+ <b>type</b> - ID of the task type. Assumed data type: integer.

Links to other tables:
1. id -> question_id (from <a href = "#answer">Answer</a>). Type: one-to-many.
2. id -> question_id (from <a href = "#possibleAns">Possible Answers</a>). Type: one-to-many.
3. id -> question_id (from <a href = "#hints">Hints</a>). Type: one-to-many.
4. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
5. id (from <a href = "#place">Place</a>) -> place_id. Type: one-to-many.
6. id (from <a href = "#qtype">Question Type</a>) -> type. Type: one-to-many.

### <a name = "qtype"></a>Question Type
Fields:
+ <b><i>id</i></b> - the unique identifier for the question type. Assumed data type: serial.
+ <b><i>question_type</i></b> - string question type designation for convenient configuration. Assumed data type: varchar.

Links to other tables:
1. id -> type (from <a href = "#question">Question</a>). Type: one-to-many.

### <a name = "answer"></a>Answer
Fields:
+ <b><i>id</i></b> - the unique identifier of the answer. Assumed data type: serial.
+ <b>question_id</b> - ID of the question that the answer corresponds to. Assumed data type: integer.
+ answer_text - text of the answer. Assumed data type: text.

Links to other tables:
1. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
2. id (from <a href = "#question">Question</a>) -> question_id. Type: one-to-many.

### <a name = "possibleAns"></a>Possible Answers
Fields:
+ <b><i>id</i></b> - the unique identifier of the answer option. Assumed data type: serial.
+ <b>question_id</b> - ID of the question that the answer option corresponds to. Assumed data type: integer.
+ possible_ans_text - text of the answer option. Assumed data type: text.

Links to other tables:
1. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
2. id (from <a href = "#question">Question</a>) -> question_id. Type: one-to-many.

### <a name = "hints"></a>Hints
Fields:
+ <b><i>id</i></b> - the unique identifier of the hint. Assumed data type: serial.
+ <b>question_id</b> - ID of the question that the hint corresponds to. Assumed data type: integer.
+ hint_text - hint text. Assumed data type: text.
+ fine - the number of points deducted for using the hint. Assumed data type: float.

Links to other tables:
1. id -> object_id (from <a href = "#files">Files</a>). Type: one-to-many.
2. id (from <a href = "#question">Question</a>) -> question_id. Type: one-to-many.

### <a name = "files"></a>Files
Fields:
+ <b><i>id</i></b> - the unique identifier of the entry. Assumed data type: serial.
+ <b>type_of_object_id</b> - ID of the type of object the file is linked to. Assumed data type: integer.
+ <b>object_id</b> - ID of the object the file is linked to. Assumed data type: integer.
+ <b>url_for_file</b> - link to the file. Assumed data type: text.
+ <b>type_of_file</b> - file format. Assumed data type: varchar.

Links to other tables:
1. id (from <a href = "#otype">Object Type</a>) -> type_of_object_id. Type: one-to-many.
2. id (from <a href = "#quest">Quest</a>) -> object_id. Type: one-to-many.
3. id (from <a href = "#place">Place</a>) -> object_id. Type: one-to-many.
4. id (from <a href = "#question">Question</a>) -> object_id. Type: one-to-many.
5. id (from <a href = "#answer">Answer</a>) -> object_id. Type: one-to-many.
6. id (from <a href = "#possibleAns">Possible Answers</a>) -> object_id. Type: one-to-many.
7. id (from <a href = "#hints">Hints</a>) -> object_id. Type: one-to-many.

### <a name = "otype"></a>Object Type
Fields:
+ <b><i>id</i></b> - the unique identifier for the object type. Assumed data type: serial.
+ <b><i>object_type</i></b> - string object type designation for convenient use. Assumed data type: varchar.

Links to other tables:
1. id -> type_of_object_id (from <a href = "#files">Files</a>). Type: one-to-many.

### <a name = "user"></a>User
Fields:
+ <b><i>id</i></b> - the unique identifier assigned to the telegram bot user. Assumed data type: serial.
+ <b><i>telegram_id</i></b> - telegram user ID. Assumed data type: text.

Links to other tables:
1. id -> user_id (from <a href = "#history">History</a>). Type: one-to-many.

### <a name = "history"></a>History
Fields:
+ <b><i>id</i></b> - the unique identifier of the entry. Assumed data type: serial.
+ <b>user_id</b> - user ID. Assumed data type: integer.
+ <b>quest_id</b> - quest ID. Assumed data type: integer.
+ <b>is_finished</b> - quest status: completed (true) or interrupted (false). Assumed data type: boolean.
+ <b>last_place_id</b> - ID of the place where the quest ends. Assumed data type: integer.
+ final_score - the number of points scored by the player at the time of ending of the quest. Assumed data type: float.

Links to other tables:
1. id (form <a href = "#user">User</a>) -> user_id. Type: one-to-many.
2. id (form <a href = "#quest">Quest</a>) -> quest_id. Type: one-to-many.
3. id (form <a href = "#place">Place</a>) -> last_place_id. Type: one-to-many.