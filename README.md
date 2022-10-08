# KHADI-Timetable-Bot

## Requirements

* Python 3+

## Run

1. `python pip install -r requirements.txt`
2. Set environment variables: `CHAT_ID` and `BOT_TOKEN`
3. Schedule bot run in cron:
    1. `45 7 * * 1-6 python main.py` - before first lesson
    2. `30 9 * * 1-6 python main.py` - before second lesson
    3. `25 11 * * 1-6 python main.py` - before third lesson
    4. `10 13 * * 1-6 python main.py` - before fourth lesson
