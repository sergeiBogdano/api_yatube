import csv

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class Command(BaseCommand):
    help = (
        'Импорт данных из CSV файлов: категории, комментарии, жанры, '
        'отношения жанров и произведений, произведения и пользователи'
    )

    def handle(self, *args, **kwargs):
        self.import_categories()
        self.import_comments()
        self.import_genres()
        self.import_genre_title()
        self.import_titles()
        self.import_users()
        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))

    def import_categories(self):
        """Импорт категорий из файла category.csv."""
        with open(
                'static/data/category.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS(
            'Категории успешно импортированы!'
        ))

    def import_comments(self):
        """Импорт комментариев из файла comments.csv."""
        with open(
                'static/data/comments.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                pub_date = parse_datetime(row['pub_date'])
                review_id = int(row['review_id'])
                author_id = int(row['author'])

                try:
                    review = Review.objects.get(id=review_id)
                except Review.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Отзыв с id {review_id} не существует. "
                        f"Пропускаем строку {row['id']}."
                    ))
                    continue

                try:
                    author = User.objects.get(id=author_id)
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Пользователь с id {author_id} не существует. "
                        f"Пропускаем строку {row['id']}."
                    ))
                    continue

                Comment.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'review': review,
                        'text': row['text'],
                        'author': author,
                        'pub_date': pub_date,
                    }
                )
        self.stdout.write(self.style.SUCCESS(
            'Комментарии успешно импортированы!'
        ))

    def import_genres(self):
        """Импорт жанров из файла genre.csv."""
        with open(
                'static/data/genre.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genre.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'slug': row['slug']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Жанры успешно импортированы!'))

    def import_genre_title(self):
        """Импорт отношений жанров и произведений из файла genre_title.csv."""
        with open(
                'static/data/genre_title.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                title_id = int(row['title_id'])
                genre_id = int(row['genre_id'])

                try:
                    title = Title.objects.get(id=title_id)
                except Title.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Произведение с id {title_id} не существует. "
                        f"Пропускаем строку {row['id']}."
                    ))
                    continue

                try:
                    genre = Genre.objects.get(id=genre_id)
                except Genre.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Жанр с id {genre_id} не существует. "
                        f"Пропускаем строку {row['id']}."
                    ))
                    continue

                title.genre.add(genre)

        self.stdout.write(self.style.SUCCESS(
            'Отношения жанров и произведений успешно импортированы!'
        ))

    def import_titles(self):
        """Импорт произведений из файла titles.csv."""
        with open(
                'static/data/titles.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                category_id = int(row['category'])

                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Категория с id {category_id} не существует. "
                        f"Пропускаем строку {row['id']}."
                    ))
                    continue

                Title.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'year': int(row['year']),
                        'category': category,
                    }
                )
        self.stdout.write(self.style.SUCCESS(
            'Произведения успешно импортированы!'
        ))

    def import_users(self):
        """Импорт пользователей из файла users.csv."""
        with open(
                'static/data/users.csv',
                newline='',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = int(row['id'])
                username = row['username']
                email = row['email']
                role = row['role'] if row['role'] else 'user'
                bio = row.get('bio', '')
                first_name = row.get('first_name', '')
                last_name = row.get('last_name', '')

                User.objects.update_or_create(
                    id=user_id,
                    defaults={
                        'username': username,
                        'email': email,
                        'role': role,
                        'bio': bio,
                        'first_name': first_name,
                        'last_name': last_name
                    }
                )
        self.stdout.write(self.style.SUCCESS(
            'Пользователи успешно импортированы!'
        ))
