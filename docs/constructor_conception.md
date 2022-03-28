# Description of the quest constructor interface
## Basic concept
The constructor is a graphic editor of the quest graph. Using it, the user can both create new quests and edit old ones.

## Graphical representation
Each question or instruction (as well as the first greeting and last farewell messages) is represented by a block with brief information: the wording of the question or instruction (with a limit on the length of the text output), the type of question, and additional brief information (see block descriptions). The blocks are arranged in levels. The block is located at the next level from the level of the previous question (indication) and is connected to the ancestor by a line. Thus, the starting block is located on the top of page and the entire quest graph "descends" from it to the final block.

## Appearance of blocks
### Open question
A block with one or more input and output lines. Contains a brief statement of the question and answer.

### Multiple choice question
Block with one or more input and output lines. The output lines start from the letters of the answer (the answers themselves are not displayed in the block). The block contains only the question and the letters of the answer options (determined automatically).

### Direction to jump
The block contains the instruction text. Can only have one output line.

### Start block
A block with a welcome message is always present in the quest. Has one outgoing line. Contains the message itself (with a limit on the length of the output).

### End block
A block with a farewell message (with a limit on the length of the output). It does not have an output and any number of input lines.

## Expanded view
When clicking on the block with the left mouse button, the user goes to a modal window with detailed settings. The view of the window depends on the type of question and contains all the necessary fields for customizing this question (text, answer options, files, hints...). 

## Create a new block
When right-clicking on a block, the user sees a drop-down menu where one of the options is "create next block". Clicking on it takes the user to a modal window with the choice of the type of the next block (and the choice of the answer leading to this block for a multiple choice question). After that, a block is created, and the user goes to the modal window for its settings. A block with no outgoing connections is automatically connected to a target block until the outgoing block is created. If the end block is selected as the next block, it is simply connected to it

## Removing blocks
When right-clicking on a block, the user sees a drop-down menu, one of which is "delete block". When clicked, confirmation is requested and the block is removed with all its information (files, hints, etc.), after which the graph may become disconnected.