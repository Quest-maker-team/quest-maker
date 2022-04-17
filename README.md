# QuestMaker
Quest maker project, SPbPU 2022.

Consist of 2 parts:
+ [Telegram bot to play quests.](bot/README.md)
+ [Service for quest creating including back-end and front-end.](website/README.md)

There is telegram bot [@QuestMakerBot](https://t.me/QuestMakerBot) to play quests.
In bot player is able to choose quest and then quest session starts.

Quests are created with web service. Creators make quests with sequence of stations.
After creation quest becomes unpublic and only selected users can play it.
To make quest public and visible in global list admin review is required.
After moderation all users can choose quest to play.

To see project advanteges and comparison see [doc](docs/analogues.md).

## Staff
+ [Baev Daniil](https://github.com/BaevDaniil)
+ [Vorotnikov Andrey](https://github.com/aVorotnikov)
+ [Pavlov Ilya](https://github.com/IlyaP01)
+ [Chevykalov Grigory](https://github.com/gchevykalov)
+ [Shvarts Aleksandr](https://github.com/AleksandrShvartz)

## Rules for git workflow
`main` branch is a main project branch. Contains current project version.
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

### Pull request rules
Web service part must be reviewed by Pavlov Ilya, bot part by Vorotnikov Andrey.
Pavlov Ilya and Vorotnikov Andrey add their part teammates for review.
Pavlov Ilya and Vorotnikov Andrey add each other as reviewers on document tasks.
Other reviewers are optional.

All reviewers must approve changes. After that last reviewer or pull request author can merge it.

#### Naming
In the end of pull request name must be `#<ZenHub isssue number>`.

## Development tools
+ <a href="https://www.python.org"><b>Python</b></a> 3.8 and later for bot and website backend
+ <a href="https://flask.palletsprojects.com/en/2.0.x"><b>Flask</b></a> framework for website backend
+ <a href="https://docs.aiogram.dev/en/latest"><b>aiogram</b></a> framework for telegram bot
+ <a href="https://devdocs.io/html/"><b>HTML</b></a> for website markup
+ <a href="https://devdocs.io/css/"><b>CSS</b></a> for styling website
+ <a href="https://devdocs.io/javascript/"><b>JavaScript</b></a> for webside frontend scripts

## Code style
### Python backend
We use <a href="https://www.python.org/dev/peps/pep-0008/">
PEP 8</a> with small changes and additions:
+ Maximum line length is 120 characters (default for PyCharm)
+ Use spaces, no tabs
+ Always surround <b>all</b> binary operators with a single space on either side
+ Use documentation strings for all modules, functions, classes and methods
+ Use english for all docstrings and comments

### HTML, CSS
We use <a href="https://google.github.io/styleguide/htmlcssguide.html#HTML">
Google HTML/CSS Style Guide</a> with small changes and addition:
+ Use <b>4</b> spaces for <b>every</b> child element, which starts on a new line (addit to <a href="https://google.github.io/styleguide/htmlcssguide.html#:~:text=HTML%20Formatting%20Rules-,General%20Formatting,-Use%20a%20new">3.2.1</a>)
+ When line-wrapping, each continuation line should be indented at least <b>8</b> additional spaces from the original line to distinguish wrapped attributes from child elements. (change in <a href="https://google.github.io/styleguide/htmlcssguide.html#:~:text=td%3E%24%204.50%0A%3C/table%3E-,HTML%20Line%2DWrapping,-Break%20long%20lines">3.2.2</a>)

### JavaScript
We use <a href="https://google.github.io/styleguide/jsguide.html">
Google JavaScript Style Guide</a> with small changes:
+ Block indentation: <b>+4<b> spaces (<a href="https://google.github.io/styleguide/jsguide.html#:~:text=4.2.1-,Array%20literals%3A%20optionally%20block%2Dlike,-Any%20array%20literal">4.2.1</a>)
+ Indent continuation lines at least <b>+8<b> spaces (<a href="https://google.github.io/styleguide/jsguide.html#:~:text=Indent%20continuation%20lines%20at%20least%20%2B4%20spaces">4.5.2</a>)
+ Maximum line length is 120 characters (<a href="https://google.github.io/styleguide/jsguide.html#:~:text=insertion%20is%20forbidden.-,4.4%20Column%20limit%3A%2080,-JavaScript%20code%20has">4.4</a>)
