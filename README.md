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

After pull request opening connect it with ZenHub issue. Use [ZenHub extension](https://www.zenhub.com/extension) for GitHub in browser.

### Branch naming rules
Branch name consist of lowercase letters words separated by `_`.

### Commit rules
Commit description structure:
```
<Verb infinitive> {grammatical modifiers for subject} <subject> #<ZenHub issue number>
```

### Pull request naming rules
In the end of pull request name must be `#<ZenHub isssue number>`.

## Development tools
+ <a href="https://www.python.org"><b>Python</b></a> 3.8 and later for bot and website backend
+ <a href="https://flask.palletsprojects.com/en/2.0.x"><b>Flask</b></a> framework for website backend
+ <a href="https://docs.aiogram.dev/en/latest"><b>aiogram</b></a> framework for telegram bot

## Code style
### Python backend
We use <a href="https://www.python.org/dev/peps/pep-0008/">
PEP 8</a> with small changes and additions:
+ Maximum line length is 120 characters (default for PyCharm)
+ Use spaces, no tabs
+ Always surround <b>all</b> binary operators with a single space on either side
+ Use documentation strings for all modules, functions, classes and methods
+ Use english for all docstrings and comments