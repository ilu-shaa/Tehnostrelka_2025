import os
import csv
import django

# Настройка Django-окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_project.settings')
django.setup()

from movies_app.models import Movie

def create_table():
    """
    Создает таблицу в базе данных на основе модели Movie.
    """
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'makemigrations', 'movies_app'])
    execute_from_command_line(['manage.py', 'migrate'])

# Создание таблицы в базе данных
create_table()

# Путь к CSV файлу
csv_file_path = "movies.csv"

# Импорт данных из CSV в базу данных
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        year = row['year'].split('–')[0]
        try:
            year = int(year)
        except ValueError:
            print(f"⚠ Пропущен фильм {row['title']} с некорректным годом: {row['year']}")
            continue  
        Movie.objects.create(
            title=row['title'],
            year=year,
            user_tags=row['user_tags'],
            reviews=row['reviews'],
            author=row['author'],
            plot=row['plot'],
            poster=row['poster']
        )

print("✅ Данные успешно загружены в базу!")