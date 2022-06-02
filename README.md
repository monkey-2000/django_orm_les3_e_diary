# Корректируем данные в электронном дневнике
Скрипт изменения данных в электронном дневнике:
 - исправляет плохие оценки;
 - удаляет замечания;
 - добавляет похвалу от учителя.


### Как установить
Скачать сайт электронного дневника здесь https://github.com/devmanorg/e-diary. 
Там же можно найти инструкции по его запуску. Также вам потребуется файл с базой данных.

Положить scripts.py в папку электронного дневника, которая содержит файл manage.py.

### Пример запуска скрипта
 - запустить интерактивную панель Django, импортировать функцию improve_school_result_script из scripts:
 ```
    venv> python manage.py shell
	Python .....
	Type "help", "copyright", "credits" or "license" for more information.
	(InteractiveConsole)
    >>> from scripts import improve_school_result_script
    >>> improve_school_result_script('INPUT NAME', 'INPUTLESSON NAME')
    School result corrected.
 ```

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
