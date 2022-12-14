import asyncio
import logging
from datetime import datetime

import aiocron
from aiogram import Bot

from client.khadi_client import KHADIClient
from config.config import Config
from provider.lesson_provider import LessonProvider
from utils import keyboard, mapper

logging.basicConfig(level=logging.INFO, format='[%(asctime)s: %(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(Config.BOT_TOKEN)

khadi_client = KHADIClient('https://vuz.khadi.kharkov.ua')
lesson_provider = LessonProvider(khadi_client)


async def send_lessons_today() -> None:
    await send_lessons_on_date(datetime.now())


async def send_lessons_on_date(date: datetime) -> None:
    logger.info(f'Searching lessons for date {date}')
    lessons = await lesson_provider.get_lessons(date)
    logger.info(f'Lessons for date: {lessons}')
    text = 'Пары на сегодня: ' if lessons else 'Вам повезло, сегодня нет пар 🥳'
    await bot.send_message(Config.CHAT_ID, '\n'.join(['Доброе утро, блядь!', text]))
    for lesson in lessons:
        await bot.send_message(Config.CHAT_ID, mapper.lesson_to_text(lesson),
                               reply_markup=keyboard.lesson_url(lesson.url))


async def send_lesson_today(lesson: dict):
    logger.info(f'Sending lesson: {lesson}')
    await send_lesson_on_date(lesson, datetime.now())


async def send_lesson_on_date(lesson: dict, date: datetime) -> None:
    clazz = await lesson_provider.get_lesson(lesson, date)
    if not clazz:
        logger.info(f'Lesson not found {lesson}')
        return
    text = '\n'.join(['Сейчас по расписанию:', mapper.lesson_to_text(clazz)])
    await bot.send_message(Config.CHAT_ID, text, reply_markup=keyboard.lesson_url(clazz.url))


async def main():
    aiocron.crontab(Config.START_CRON, send_lessons_today)
    for lesson in Config.LESSONS:
        cron = lesson['cron']
        aiocron.crontab(cron, send_lesson_today, (lesson,))
        logger.info(f'Registered job on {cron} for lesson {lesson}')
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Goodbye!')
        exit(0)
