from django import forms
from django.contrib.auth.forms import UserCreationForm
from movies_app.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # Переопределяем поле rating, чтобы пользователь выбирал его из вариантов 1..5
    rating = forms.ChoiceField(
        choices=[(i, f"{i}★") for i in range(1, 6)],
        label="Оценка",
        widget=forms.RadioSelect,   # Можно выбрать другой вид, например Select
        initial=5
    )

    class Meta:
        model = Comment
        fields = ['text', 'rating']  # Добавили rating в список выводимых полей
        labels = {
            'text': 'Комментарий',
        }