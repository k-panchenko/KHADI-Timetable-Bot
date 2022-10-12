import asyncio
import re
from datetime import datetime
from typing import Tuple, cast, Optional

from aiogram import Bot, types
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

from client.khadi_client import KHADIClient
from config.config import Config

bot = Bot(Config.BOT_TOKEN)

khadi_client = KHADIClient('https://vuz.khadi.kharkov.ua')


async def convert_response_to_message(response: bytes, current_time: datetime) -> Tuple[str, Optional[str]]:
    soup = BeautifulSoup(response, 'html.parser')
    current_time_str = current_time.strftime('%d.%m.%Y')
    lessons_today = soup.find_all('div', {'title': re.compile(' '.join([current_time_str, r'\d', 'пара']))})
    date, nearest_lesson, nearest_lesson_time = find_nearest_lesson(lessons_today, current_time)
    lesson, start, end = (tag.text for tag in nearest_lesson_time.find_all())
    details_tag = cast(Tag, nearest_lesson.previous_sibling.previous_sibling)
    details = await khadi_client.get_details(details_tag.attrs['data-r1'], details_tag.attrs['data-r2'])
    text = f'Сейчас по расписанию: {lesson} ({start} - {end})\n\n' + nearest_lesson.text.strip()
    url = BeautifulSoup(details, 'html.parser').find('a').text
    return 'Сегодня больше нет пар 🤷🏿', None if date < current_time else (text, url)


def find_nearest_lesson(lessons: ResultSet[Tag], current_time: datetime) -> Tuple[datetime, Tag, Tag]:
    lesson_starts = {(lesson, lesson.find_parent('td').find_previous_sibling('th')) for lesson in lessons}
    dates = {(datetime.strptime(time.find('span', class_='start').text, '%H:%M'), lesson, time) for lesson, time in
             lesson_starts}
    dates = {(current_time.replace(hour=date.hour, minute=date.minute), lesson, time) for date, lesson, time in dates}
    return min(dates, key=lambda date: abs(current_time - date[0]))


async def send_message_to_tg_group(message: str, url: str = None):
    markup = types.InlineKeyboardMarkup(1).add(*[types.InlineKeyboardButton('Ссылка на занятие', url)]) if url else None
    await bot.send_message(Config.CHAT_ID, message, reply_markup=markup)


async def main(current_time: datetime = None):
    if not current_time:
        current_time = datetime.now()
    try:
        response = await khadi_client.get_timetable_from_server(Config.FACULTY_ID, Config.COURSE, Config.GROUP_ID)
        message, url = await convert_response_to_message(response, current_time)
        await send_message_to_tg_group(message, url)
    except Exception as ex:
        await send_message_to_tg_group('Не удалось получить расписание, возможно, сервер ХНАДУ упал 🤷🏿')
        raise ex
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
