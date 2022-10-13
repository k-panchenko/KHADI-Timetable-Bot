from domain.lesson import Lesson


def lesson_to_text(lesson: Lesson):
    return f'''{lesson.name} ({lesson.start} - {lesson.end})

{lesson.info}
{lesson.additional_info or ''}'''
