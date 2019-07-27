from django.core.management.base import BaseCommand
from main.models import Film, Genre, Actor, Director
from data_generate.parser import need_dict


class Command(BaseCommand):
    help = "Создание новых фильмов"

    def add_arguments(self, parser):
        parser.add_argument('link', nargs='+', type=str)

    def handle(self, *args, **options):

        link = need_dict(options["link"][0])
        film, create = Film.objects.update_or_create(title=link["title"],
                                                     img=link["img"],
                                                     box_office=link["box_office"],
                                                     budget=link["budget"],
                                                     year=link["year"],
                                                     description=link["description"],
                                                     rating=link["rating"],
                                                     )

        [film.genres.add(Genre.objects.get_or_create(name=elem)[0]) for elem in link["genres"]]
        [film.actors.add(Actor.objects.get_or_create(name=elem)[0]) for elem in link["actors"]]
        [film.directors.add(Director.objects.get_or_create(name=elem)[0]) for elem in link["directors"]]

        if create:
            self.stdout.write(self.style.SUCCESS('SUCCESS CREATE: %s !'% film))
        else:
            self.stdout.write(self.style.SUCCESS('SUCCESS UPDATE: %s !' % film))
