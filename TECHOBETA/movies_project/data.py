import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_project.settings')
django.setup()

from django.core.management import call_command
from movies_app.models import Movie

def create_table():
    call_command('makemigrations', 'movies_app', interactive=False)
    call_command('migrate', interactive=False)

create_table()

csv_file_path = "C:\\Users\\Nikitosik\\VSCODE\\Tehnostrelka_2025\\TECHOBETA\\movies_project\\movies.csv"

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row.pop('Unnamed: 0', None)
        row.pop('', None)

        year_str = row.get('year', '').split('–')[0].strip() 
        try:
            year = int(year_str)
        except ValueError:
            print(f"⚠ Пропущен фильм {row.get('title')} с некорректным годом: {year_str}")
            year = None

        Movie.objects.create(
            title=row.get('title') or "",         # На случай, если ячейка пустая
            year=year,
            user_tags=row.get('user_tags') or "",
            reviews=row.get('reviews') or "",
            author=row.get('author') or "",
            plot=row.get('plot') or "",
            poster=row.get('poster') or ""
        )

print("✅ Данные успешно загружены в базу!")