from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    user_tags = models.CharField(max_length=255)   # Можно хранить как текст
    reviews = models.TextField()                   # Будем хранить JSON-строку
    author = models.CharField(max_length=255)      # Режиссёр / автор
    plot = models.TextField()                      # Описание
    poster = models.CharField(max_length=255)      # Имя файла постера

    def __str__(self):
        return self.title
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username)
        user.set_password(password)
        user.is_active = True  # Убедитесь, что пользователь активен
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)  # Поле для активации пользователя
    is_staff = models.BooleanField(default=False)   # Поле для определения, является ли пользователь администратором

    USERNAME_FIELD = 'username'  # Поле для входа в систему
# Дополнительные поля для создания суперпользователя

    objects = UserManager()

    def __str__(self):
        return self.username