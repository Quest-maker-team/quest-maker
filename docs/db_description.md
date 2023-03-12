# Database description
Description of the moments not displayed on the database schema.

You can get acquainted with the scheme of the database in the form of an [image](https://github.com/Quest-maker-team/quest-maker/blob/main/docs/image/db.svg).

## Contents of auxiliary tables with types
The following tables are necessary for fixing the names of the types of objects used in the project.

In the future, their content may be supplemented for the expansion of functionality, but <b>entries from these tables cannot be deleted or replaced</b> without a separate agreement on this matter (since some functionality relies on them).

### Status
0. `author` - an ordinary user of the site, the creator of quests. Has no special abilities and responsibilities.
1. `moderator` - has access to hidden quests, checks them and approves them for public access.

### Media_type
0. `image`
1. `video`
2. `audio`

### Block_type
0. `start_block` - a special type defining the beginning of the quest was introduced due to the fact that when editing a question may be added to the beginning, and then ordering by id is not valid.
1. `open_question` - an open question with a text answer.
2. `choice_question` - choosing one answer from the suggested ones.
3. `movement` - an indication of the player's movement to a new location.
4. `message` - a special type that is used to send a message with some information; does not require any action from the player
5. `end_block` - a special type indicating the end of the quest branch.

## Notes on other tables

### Quest
The `open_time` and `close_time` fields represent the opening date and time of the quest and the closing date and time, respectively.
The `periodicity` field indicates how often the quest will be available - used to update fields `open_time` and `close_time` after reaching `close_time`.
The `lead_time` field determines the time limit for completing the quest. It is impossible to resume the passage of the quest with such a restriction after interruption.
It is not possible to describe the full work schedule.

The `keyword` is the unique 8-length string identifier.

If the `password` field is NULL, then the quest is public.

The `published` is `TRUE` if quest was published and `FALSE` if quest was only created as draft.

### Tag
Implemented automatic deletion of tags that are not mentioned in any of the quest descriptions.

### Draft
Table with unpublished quests. 
The `container_path` is a pickled quest object path. The `quest_id` is id of related quest if draft isn't a new quest. 

### Block
General table containing all kinds of blocks. Some types use additional tables.
+ If the question is of the `end_block` type, then when it is reached, the quest ends.
+ If the question type is `movement`, then the `place` table is additionally used.
+ If the question type is `open_question` or `choice_question`, then the `answer_option` table is additionally used.
The `next_block_id` field can be NULL only for questions and the end. In other cases, when the quest is being completed, this is perceived as a violation of the integrity of the quest.

### Place
The `open_time` and `close_time` fields represent the opening time of the place and the closing time, respectively. These fields provide a cyclical opening every day. They should not have a date written in them.

### Answer_option
+ If the `next_question_id` field is NULL when the quest is being completed, then we consider that the integrity of the quest has been violated.
+ If among the possible answers to the question there is one in which the `option_text` field contains the string <b>`skip`</b>, then this question can be skipped.
+ If among the possible answers to an open question there is one in which the `option_text` field contains <b>an empty string</b>, then the actions assigned to it (changing the number of points, switching to another question) are triggered when entering any answer other than the suggested answers to this question.

### Block_media and hint_media
Before deleting a block or hint, you must consult these tables and extract the paths to the files that you also need to delete.

### Histories
If the `is_finished` field has the value false, but the `last_question_id` field is empty, then the quest has been changed and its continuation is not possible.
