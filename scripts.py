import random

from django.core.exceptions import MultipleObjectsReturned
from datacenter.models import Lesson, Schoolkid, Commendation, Mark, Chastisement


class NameError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_schoolkid(schoolkid_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        message = f'Имя  "{schoolkid_name}" не найдено в БД. Введите другое.'
        raise NameError(message)
    except MultipleObjectsReturned:
        message = f'Для имени "{schoolkid_name}" найдено несколько вариантов. Конкретизируйте запрос.'
        raise NameError(message)
    return child


def fix_marks(schoolkid, new_mark, bad_mark):
    Mark.objects.filter(schoolkid=schoolkid, points__in=bad_mark).update(points=new_mark)


def remove_chastisements(schoolkid):
    child_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisement.delete()


def lesson_without_commendation(schoolkid, lessons):
    parallel_lessons = lessons.filter(
        year_of_study__contains=schoolkid.year_of_study,
        group_letter__contains =schoolkid.group_letter
    )

    child_commendation = Commendation.objects.filter(schoolkid=schoolkid)

    for parallel_lesson in parallel_lessons.order_by('-date'):
        if not child_commendation.filter(created=parallel_lesson.date).exists():
            return parallel_lesson


def create_commendation(schoolkid, lesson_name):
    commendation_texts = ['Молодец!',
                          'Ты меня очень обрадовал!',
                          'Великолепно!',
                          ]

    commendation_text = random.choice(commendation_texts)

    lessons = Lesson.objects.filter(subject__title__contains=lesson_name)

    if not lessons.exists():
        message = f'Предмет "{lesson_name}" не найден. Введите другое название предмета.'
        raise NameError(message)

    commendation_lesson = lesson_without_commendation(schoolkid, lessons)
    Commendation.objects.create(
        created=commendation_lesson.date,
        schoolkid=schoolkid,
        subject=commendation_lesson.subject,
        teacher=commendation_lesson.teacher,
        text=commendation_text
    )


def improve_school_results(schoolkid_name, lesson_name, new_mark=5, bad_marks=[2, 3]):

    if not lesson_name:
        print('Название предмета не введено. Повторите ввод.')
        exit(2)

    try:
        child = get_schoolkid(schoolkid_name)
        fix_marks(child, new_mark, bad_marks)
        remove_chastisements(child)
        create_commendation(child, lesson_name)
    except NameError as err:
        print(err)
        exit(2)
    else:
        print('School results corrected.')
