from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.core.validators import (MinValueValidator,  MaxValueValidator)
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.shortcuts import reverse


class Director(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name="Имя", blank=True, null=True)

    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name="Имя", blank=True, null=True)
    img = models.CharField(verbose_name="Изображение", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'

    def __str__(self):
        return self.name

 
class User(AbstractUser):
    nick = models.CharField(max_length=50, verbose_name="Никнейм")
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    img = models.CharField(verbose_name="Изображение", max_length=100, blank=True, null=True)
    description = models.TextField(verbose_name="Обо мне", null=True, blank=True)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Жанр")

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name

# Create your models here.
class Film(models.Model):
    RatingValidator = [MinValueValidator(0), MaxValueValidator(10)]

    title = models.CharField(verbose_name="Название", max_length=100, null=True, blank=True)
    img = models.CharField(verbose_name="Изображение", max_length=100, null=True, blank=True)
    box_office = models.CharField(verbose_name="Кассовые сборы", max_length=100, null=True, blank=True)
    budget = models.CharField(verbose_name="Бюджет", max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField(verbose_name="Год", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    rating = models.FloatField(verbose_name="Рейтинг", blank=True, null=True, validators=RatingValidator)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    actors = models.ManyToManyField(Actor, verbose_name="Актёры")
    directors = models.ManyToManyField(Director, verbose_name="Режиссёры")

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __unicode__(self):
        return self.title
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film', kwargs={'pk': self.pk})


class Comment(models.Model):
    film = models.ForeignKey(Film, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Тема", max_length=100, null=True, blank=True)
    content = models.TextField(verbose_name="Рецензия", blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name="Дата комментария", default=timezone.now)

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('create_or_update_comment', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_comment', kwargs={'pk': self.pk})


