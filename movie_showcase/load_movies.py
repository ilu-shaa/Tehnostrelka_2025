import csv
import os
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Load movies from a CSV file'

    def handle(self, *args, **options):
        with open('movies.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert reviews from string to list of dicts
                reviews = eval(row['reviews']) if row['reviews'] else []
                
                # Create and save Movie object
                Movie.objects.create(
                    title=row['title'],
                    year=int(row['year']),
                    user_tags=row['user_tags'],
                    reviews=reviews,
                    author=row['author'],
                    plot=row['plot'],
                    poster=row['poster']  # Assuming the poster is a path to the image file
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded movies'))