import random

from django.core.exceptions import MultipleObjectsReturned
from datacenter.models import Lesson, Schoolkid, Commendation, Mark, Chastisement


class NameError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DiaryEditor:

    def __init__(self, schoolkid_name='Фролов Иван'):
        self.schoolkid_name = schoolkid_name
        try:
            self.schoolkid = self.get_schoolkid()
        except NameError as e:
            print(e)

    def improve_school_result(self, lesson_name, new_mark=5, bad_mark=[2, 3]):
        self.fix_marks(new_mark, bad_mark)
        self.remove_chastisements()
        try:
            self.create_commendation(lesson_name)
        except NameError as err:
            print(err)
        else:
            print('School result corrected.')


    def get_schoolkid(self):
        if not self.schoolkid_name:
            return False
        try:
            child = Schoolkid.objects.get(full_name__contains=self.schoolkid_name)
        except Schoolkid.DoesNotExist:
            message = f'Имя  "{self.schoolkid_name}" не найдено в БД. Введите другое.'
            raise NameError(message)
        except MultipleObjectsReturned:
            message = f'Для имени "{self.schoolkid_name}" найдено несколько вариантов. Конкретизируйте запрос.'
            raise NameError(message)
        return child

    def fix_marks(self, new_mark, bad_mark):
        Mark.objects.filter(schoolkid=self.schoolkid, points__in=bad_mark).update(points=new_mark)

    def remove_chastisements(self):
        child_chastisement = Chastisement.objects.filter(schoolkid=self.schoolkid)
        child_chastisement.delete()

    def create_commendation(self, lesson_name):
        if not lesson_name:
            raise NameError('Название предмета не введено. Посторите ввод.')

        commendation_texts = ['Молодец!',
                              'Ты меня очень обрадовал!',
                              'Великолепно!',
                              ]

        commendation_text = random.choice(commendation_texts)

        lessons = Lesson.objects.filter(subject__title__contains=lesson_name)

        if not lessons.exists():
            message = f'Предмет "{lesson_name}" не найден. Введите другое название предмета.'
            raise NameError(message)

        commendation_lesson = self.lesson_without_commendation(lessons)
        Commendation.objects.create(
            created=commendation_lesson.date,
            schoolkid=self.schoolkid,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher,
            text=commendation_text
        )

    def lesson_without_commendation(self, lessons):
        parallel_lessons = lessons.filter(
            year_of_study__contains=self.schoolkid.year_of_study,
            group_letter__contains =self.schoolkid.group_letter
        )

        child_commendation = Commendation.objects.filter(schoolkid=self.schoolkid)

        for parallel_lesson in parallel_lessons.order_by('-date'):
            if not child_commendation.filter(created=parallel_lesson.date).exists():
                return parallel_lesson


def improve_school_result_script(schoolkid_name,lesson_name, new_mark=5, bad_mark=[2, 3]):

    a = DiaryEditor(schoolkid_name)
    try:
        a.improve_school_result(lesson_name, new_mark, bad_mark)
    except AttributeError:
        pass
