import json
from os import environ
from typing import List


class Config:
    BOT_TOKEN: str = environ['BOT_TOKEN']
    CHAT_ID: int = int(environ['CHAT_ID'])
    FACULTY_ID: int = int(environ['FACULTY_ID'])
    COURSE: int = int(environ['COURSE'])
    GROUP_ID: int = int(environ['GROUP_ID'])
    LESSONS: List[dict] = json.loads(environ['LESSONS'])
    START_CRON: str = environ['START_CRON']
