# QuestMaker website
Web application for creating and managing quests. 
## Installation
Use `git clone  https://github.com/Quest-maker-team/quest-maker` to load repo in your computer.
## Dependencies
### Virtual environment
You may install dependencies to isolated environment (only for this project).
Enter `python venv venv` in `website` directory to create virtual environment with name `venv`. 
Then activate it with command `venv/Scripts/activate`.
### Packages
You may use pip - standard python package manager.
Enter `pip install -r requirements.txt` to install packages.

## Local database
We use PostgreSQL as DBMS. You may read about installation [here](https://www.postgresql.org/docs/).
Also read instruction [how to create and initialize database](https://github.com/Quest-maker-team/quest-maker/blob/main/docs/db_guide.md). 

## Run the application
To run application in development mode, enter `website`(top-level
directory for this project). Then set `FLASK_APP` and `FLASK_ENV`
environmental variables and use command `flask run`.
+ Bash
```
$ export FLASK_APP=questmaker
$ export FLASK_ENV=development
$ flask run
```
+ CMD
```
> set FLASK_APP=questmaker
> set FLASK_ENV=development
> flask run
```