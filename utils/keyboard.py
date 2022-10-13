from typing import Optional

from aiogram import types


def lesson_url(url: Optional[str], title: str = 'Ссылка на занятие') -> Optional[types.InlineKeyboardMarkup]:
    return types.InlineKeyboardMarkup(1).add(*[
        types.InlineKeyboardButton(title, url)
    ]) if url else None
