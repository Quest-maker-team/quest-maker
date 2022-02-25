# QuestMaker 
Quest maker project, SPbPU 2022.

Consist of 2 parts:
+ Telegram bot to play quests.
+ Service for quest creating including back-end and front-end.

## Staff
+ Baev Daniil
+ Vorotnikov Andrey
+ Pavlov Ilya
+ Chevykalov Grigory
+ Schvartz Aleksandr

## Rules for git workflow
'main' branch is a main project branch. Contains current project version.
To send updates make own branch and make commits to it.

One branch is one issue (there can be agreed exceptions). One commit is one logical action.

After all necessary commits push changes and open pull request.
Pull request name contains issue number in the end.

### Commit rules
Commit description structure:

`<Verb infinitive> {grammatical modifiers for subject} <subject> #<ZenHub issue number>`

## Development tools
+ <b>Python</b> 3.8 and later for bot and website backend
+ <b>Flask</b> framework for website backend
+ <b>aiogram</b> framework for telegram bot

## Code style
### Python backend
We use <a href="https://www.python.org/dev/peps/pep-0008/">
PEP 8</a> with small changes and additions:
+ Maximum line length is 120 characters (default for PyCharm)
+ Use spaces, no tabs
+ Always surround <b>all</b> binary operators with a single space on either side
+ Use documentation strings for all modules, functions, classes and methods
+ Use english for all docstrings and comments