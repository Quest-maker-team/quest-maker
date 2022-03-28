# QuestMaker telegram bot
Telegram bot to play quests created by QuestMaker.
## User guide
Use telegram bot [@QuestMakerBot](https://t.me/QuestMakerBot) or another bot that used our project for responses.
Bot is used to play quests. To choose quest use our [web service](../website/README.md).
## Installation
Use `git clone https://github.com/Quest-maker-team/quest-maker` to load repo in your computer.
## Run application
### Telegram bot token
For correct work telegram token must be written to `TG_BOT_TOKEN` environment variable.
### Virtual environment
We use virtual environment to run application:
```
python3 -m venv venv                   # creating environment
source venv/bin/activate               # activating environment
```
Inside `venv` virtual environment:
```
pip install -r requirements.txt        # installing environments
export TG_BOT_TOKEN=<bot token value>  # exporting bot token
python3 bot.py                         # running bot
deactivate                             # deactivating enveronment
```
## Data base
We use PostgreSQL. See docs for more information:
+ [description](../docs/db_description.md);
+ [guide](../docs/db_guide.md).
### Create config file
* In `QuestMaker/bot` create file `db_config.ini`.
* File must contain following:
  ```
  [DB]
  NAME = 'questmaker'
  USER = 'postgres'
  PASSWORD = 'postgres'
  HOST = 'localhost'
  PORT = '5432'
  ```
  if the database is configured according to the [guide](../docs/db_guide.md).