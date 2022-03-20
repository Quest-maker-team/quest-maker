# QuestMaker telegram bot
Telegram bot to play quests created by QuestMaker.
## User guide
Use telegram bot [@QuestMakerBot](https://t.me/QuestMakerBot) or another bot that used our project for responses.
Bot is used to play quests. To choose quest use our [web service](../website/README.md).
## "aiogram" installing
Installing "aiogram" library.

Run virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
Inside `venv` virtual environment:
```
pip install -r requirements.txt
deactivate
```

## Telegram bot token
For correct work telegram token must be written to `TG_BOT_TOKEN` environment variable.
