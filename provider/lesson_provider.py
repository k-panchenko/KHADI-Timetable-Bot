from datetime import datetime
from typing import List, Optional, cast

from bs4 import BeautifulSoup
from bs4.element import Tag

from client.khadi_client import KHADIClient
from config.config import Config
from domain.lesson import Lesson


class LessonProvider:
    def __init__(self, khadi_client: KHADIClient):
        self._khadi_client = khadi_client

    async def get_lessons(self, date: datetime) -> List[Lesson]:
        pattern = date.strftime('%d.%m.%Y')
        soup = await self._get_timetable_soup()
        lessons = []
        for lesson in Config.LESSONS:
            result = await self._find_lesson(lesson, pattern, soup)
            if result:
                lessons.append(result)
        return lessons

    async def get_lesson(self, lesson: dict, date: datetime):
        pattern = date.strftime('%d.%m.%Y')
        return await self._find_lesson(lesson, pattern, await self._get_timetable_soup())

    async def _get_timetable_soup(self) -> BeautifulSoup:
        response = await self._khadi_client.get_timetable_from_server(Config.FACULTY_ID, Config.COURSE, Config.GROUP_ID)
        return BeautifulSoup(response, 'html.parser')

    async def _find_lesson(self, lesson: dict, pattern: str, soup: BeautifulSoup) -> Optional[Lesson]:
        title = ' '.join([pattern, lesson['name']])
        lesson_tag = soup.find('div', attrs={'title': title})
        if not lesson_tag:
            return
        sibling = cast(Tag, lesson_tag.previous_sibling.previous_sibling)
        datas = [v for k, v in sibling.attrs.items() if 'data' in k]
        details = await self._khadi_client.get_details(*datas)
        details_soup = BeautifulSoup(details, 'html.parser')
        link_tag = details_soup.find('a')
        return Lesson(lesson['name'], lesson['start'], lesson['end'], lesson_tag.text.strip(), link_tag.text, None)
