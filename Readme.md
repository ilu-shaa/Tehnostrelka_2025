# Фильмотека — платформа для поиска и рекомендации фильмов

[![Статус сборки](https://img.shields.io/badge/статус-%20готов-green)](https://github.com/ilu-shaa/Tehnostrelka_2025.git)

## 🎬 Что делает проект?
Платформа предоставляет:
- Поиск фильмов по названию, жанру, году и режиссеру
- **Семантический поиск** по описанию с использованием AI
- Систему рекомендаций на основе лайков
- Возможность оставлять комментарии и оценки
- Персональные профили пользователей

## 🌟 Почему этот проект полезен?
- Объединяет классические методы поиска с нейросетевыми технологиями
- Позволяет находить фильмы по смыслу, а не точным совпадениям
- Открытый исходный код для модификаций
- Легковесная архитектура на SQLite

## 🚀 Как начать работу?

### Предварительные требования
- Python 3.12.4
- pip
- Виртуальное окружение 


### Установка
- git clone https://github.com/ilu-shaa/Tehnostrelka_2025.git
- python -m venv venv
- .venv\Scripts\activate 
- pip install -r requirements.txt
- pip install git+https://github.com/UKPLab/sentence-transformers.git
- cd TechStrel\Tehnostrelka_2025\TECHOBETA\movies_projec\
- pip install git+https://github.com/UKPLab/sentence-transformers.git
- python manage.py runserver
