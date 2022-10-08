import re
from datetime import datetime
from os import environ
from typing import Tuple, cast, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet


def get_timetable_from_server():
    cookies = {
        '_csrf-frontend': 'e16d6c209f84adf52830964505c618b84dfe86306507d39ef0fdb9e85af0e4a0a%3A2%3A%7Bi%3A0%3Bs%3A1'
                          '4%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228mQLvU7KmkT1uQ5r1LvhFvZsFs9LHMqk%22%3B%7D',
    }

    params = {
        'type': '0',
    }

    data = {
        '_csrf-frontend': 'l547P68_3nvb_4rM2P-KQQVi5-DkWUT4YfIiC_0XK-uv82pz2WrpMLaU3v2trr8zNC6RiKIvHosngRtHtVpagA==',
        'TimeTableForm[facultyId]': '3',
        'TimeTableForm[course]': '1',
        'TimeTableForm[groupId]': '1046',
    }

    return requests.post('https://vuz.khadi.kharkov.ua/time-table/group', params=params, cookies=cookies, data=data)


def convert_response_to_message(response: requests.Response, current_time: datetime) -> Tuple[str, Optional[str]]:
    soup = BeautifulSoup(response.content.decode(), 'html.parser')
    current_time_str = current_time.strftime('%d.%m.%Y')
    lessons_today = soup.find_all('div', {'title': re.compile(' '.join([current_time_str, r'\d', 'пара']))})
    date, nearest_lesson, nearest_lesson_time = find_nearest_lesson(lessons_today, current_time)
    lesson, start, end = (tag.text for tag in nearest_lesson_time.find_all())
    details_tag = cast(Tag, nearest_lesson.previous_sibling.previous_sibling)
    details = get_details(details_tag.attrs['data-r1'], details_tag.attrs['data-r2'])
    text = f'Сейчас по расписанию: {lesson} ({start} - {end})\n\n' + nearest_lesson.text.strip()
    url = BeautifulSoup(details.content.decode(), 'html.parser').find('a').text
    return 'Сегодня больше нет пар 🤷🏿' if date < current_time else text, url


def get_details(data_r1: str, data_r2: str) -> requests.Response:
    params = {
        'r1': data_r1,
        'r2': data_r2
    }

    headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.get('https://vuz.khadi.kharkov.ua/time-table/show-ads', params=params, headers=headers)


def find_nearest_lesson(lessons: ResultSet[Tag], current_time: datetime) -> Tuple[datetime, Tag, Tag]:
    lesson_starts = {(lesson, lesson.find_parent('td').find_previous_sibling('th')) for lesson in lessons}
    dates = {(datetime.strptime(time.find('span', class_='start').text, '%H:%M'), lesson, time) for lesson, time in
             lesson_starts}
    dates = {(current_time.replace(hour=date.hour, minute=date.minute), lesson, time) for date, lesson, time in dates}
    return min(dates, key=lambda date: abs(current_time - date[0]))


def send_message_to_tg_group(message: str, url: str):
    json = {
        'chat_id': environ['CHAT_ID'],
        'text': message,
    }
    if url:
        json['reply_markup'] = {'inline_keyboard': [[
            {
                'text': 'Ссылка на занятие',
                'url': url
            }
        ]]}

    requests.post(f'https://api.telegram.org/bot{environ["BOT_TOKEN"]}/sendMessage', json=json)


def main(current_time: datetime = None):
    if not current_time:
        current_time = datetime.now()
    response = get_timetable_from_server()
    message, url = convert_response_to_message(response, current_time)
    send_message_to_tg_group(message, url)


if __name__ == '__main__':
    main()
