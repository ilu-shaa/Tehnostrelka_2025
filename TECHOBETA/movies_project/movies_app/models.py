from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin
from django.db import models
from django.db import models
from django.contrib.auth.models import User  # или ваша кастомная модель пользователя

class Movie(models.Model):
    title = models.CharField(max_length=255)
    user_tags = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    # ... и другие поля

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
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')



from django.db import models

from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'