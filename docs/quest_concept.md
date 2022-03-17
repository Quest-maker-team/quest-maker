## Quest concept

### General description
The quest presents a sequence of questions and movement instructions (possibly not explicit). The process of passing consists in answering questions and, possibly, moving around the locations. The question or instruction is a text message, possibly with an attached audio or other file. The answer to the question can be a text message, or by clicking on one of the buttons provided, depending on the type of question. Each question must have at least one answer. But it is possible to indicate the transition to the next point. What can be considered as a question, the answer to which is the achievement of a location. Answers that do not lead to further questions, directions to travel, or completion of the quest are considered "unsatisfactory" and lead to the question being repeated. At least one such connection must come from the question. There can be no transition without instructions. The transition mechanism with instructions looks like this. After the next accepted response, the user is instructed to move. Moves to the specified location, after which he is asked the next question in the thread. Users earn points as they progress. At the discretion of the author, the quest may be limited in time.

### Quest start
With the help of the bot, the user selects the desired quest and begins its passage. The quest can be private. To access such quests, you need to know the keyword. Perhaps it will be possible to replace this with a link invitation, then there will be no need to display it in the general list. After that, a welcome message is sent to him, and then the first question.

### Along the quest
After receiving the answer, the bot either sends the next question (in this case, the points may change in any direction or not change at all), or in case of an unsatisfactory answer, it repeats the current one (possibly with deduction of points), or sends an indication of movement to a specific place (in this case the quest continues after reaching this point, at the discretion of the author, he can add the time the point is active, for example, night hours). The next question or indication (if the author has provided a branch of the quest) may depend on the answer to the current question.

At the discretion of the author, hints can be attached to the question (the presence and size of the fine, for which the author determines). Also, at the discretion of the author, some questions may be skipped (the presence and amount of the fine, for which the author determines).

The user can interrupt the passage of the quest and continue it in the future, if the passage is not limited in time.

### After passing
The quest ends after receiving a satisfactory answer to the last question in the branch. At the end of the quest, the user receives a result in points and a farewell message.