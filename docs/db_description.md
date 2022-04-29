# Database description
Description of the moments not displayed on the database schema.

You can get acquainted with the scheme of the database in the form of an [image](https://github.com/Quest-maker-team/quest-maker/blob/main/docs/image/db.png).

## Contents of auxiliary tables with types
The following tables are necessary for fixing the names of the types of objects used in the project.

In the future, their content may be supplemented for the expansion of functionality, but <b>entries from these tables cannot be deleted or replaced</b> without a separate agreement on this matter (since some functionality relies on them).

### Statuses
0. `author` - an ordinary user of the site, the creator of quests. Has no special abilities and responsibilities.
1. `moderator` - has access to hidden quests, checks them and approves them for public access.

### File_types
0. `image`
1. `video`
2. `audio`

### Question_types
0. `open` - an open question with a text answer.
1. `choice` - choosing one answer from the suggested ones.
2. `movement` - an indication of the player's movement to a new location.
3. `start` - a special type defining the beginning of the quest was introduced due to the fact that when editing a question may be added to the beginning, and then ordering by id is not valid. <b>It is a fictitious question with one answer option leading to the real first question.</b>
4. `end` - a special type indicating the end of the quest branch.

## Notes on other tables

### Quests
The `open_time` and `close_time` fields represent the opening date and time of the quest and the closing date and time, respectively. These fields do not ensure the cyclical opening of the quest, for example, it will not be possible to record 12:00 and 18:00 in the hope that the quest will open every day at 12 and close at 18.

`keyword` is the unique 8-length string identifier     

### Draft quests
Table with unpublished quests. 
`container` is a pickled quest object. `quest_id` is id of related quest if draft isn't a new quest. 

### Places
The `open_time` and `close_time` fields represent the opening time of the place and the closing time, respectively. These fields provide a cyclical opening every day. They should not have a date written in them.

### Questions
+ If the question is of the `end` type, then when it is reached, the quest ends.
+ If the question is of the type `movement`, then the reference to the table `movements`.
+ In other cases, the `answer_options` table is accessed.

### Answer_options
+ If the `next_question_id` field is empty, then when choosing this answer option, the question repeats, so it is important that the `correct` answers have this field not empty.
+ The question is also repeated if the user has entered an answer not provided by the author as an answer to an open question.
+ If among the possible answers to the question there is one in which the `option_text` field contains the string <b>`skip`</b>, then this question can be skipped.
+ If among the possible answers to an open question there is one in which the `option_text` field contains <b>an empty string</b>, then the actions assigned to it (changing the number of points, switching to another question) are triggered when entering any answer other than the suggested answers to this question.

### Histories
If the `is_finished` field has the value false, but the `last_question_id` field is empty, then the quest has been changed and its continuation is not possible.
