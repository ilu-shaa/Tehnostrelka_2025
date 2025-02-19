import csv
from movies_app.models import Movie

csv_file_path = "movies.csv"

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

print("✅ Данные успешно загружены в базу!")  # Вне блока with
