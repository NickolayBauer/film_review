import uuid

from .filters import FilmFilter
from .models import Film, User, Comment
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from main.forms import CommentForm
from main.forms import LoginForm
from main.forms import RegistrationForm
from main.models import Comment
from main.models import User
from main.permissions import anonymous_only
from django.http import JsonResponse
from django.core import serializers
import json


def index(request):
    return render(request, "main/index.html", {'users': len(User.objects.all()),'reviews':len(Comment.objects.all()), 'films': Film.objects.all()})


def random_film(request):
    return render(request, "main/random_film.html", {'film': Film.objects.order_by('?').first()})


def logout_user(request):
    logout(request)
    return redirect('/')


def films(request):
    fltr = FilmFilter(request.GET, request=request, queryset=Film.objects.all())

    page = request.GET.get('page', 1)
    paginator = Paginator(fltr.qs, 8)
    paginated_films = paginator.get_page(page)

    return render(request, "main/films.html", {'paginated_films': paginated_films, 'filter': fltr})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    red = redirect(request.META.get('HTTP_REFERER', '/'))
    if comment.user != request.user:
        return red
    comment.delete()
    return red


def film(request, pk):
    film = get_object_or_404(Film, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        form.instance.film = film
        form.save()
        return redirect(film)
    return render(request, 'main/film.html', {'film': film, "form": form})


@anonymous_only
def login_user(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                login_form.add_error(
                    None, "Пользователь с таким логином или паролем не существует")
                return render(request, 'main/login.html', {'login_form': login_form})

    return render(request, 'main/login.html', {'login_form': login_form})


@anonymous_only
def registration(request):
    edit_form = RegistrationForm()
    if request.method == 'POST':
        edit_form = RegistrationForm(data=request.POST)
        if edit_form.is_valid():
            user = edit_form.save(commit=False)
            user.username = str(uuid.uuid4().int)[:10]
            user.save()
            return redirect('login')

    return render(request, 'main/registration.html', {'edit_form': edit_form})


def profile(request, pk):
    user = get_object_or_404(User, id=pk)
    return render(request, 'main/profile.html', {'user': user})

def find_random_film(request):
    print("great!")
    film = Film.objects.order_by('?').first()
    film_data = serializers.serialize('json',[film], ensure_ascii=False)[1:-1]
    return JsonResponse({"film":film_data, "film_url":film.get_absolute_url()}, safe=False) 