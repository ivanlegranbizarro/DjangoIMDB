import os
import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render
from films.models import Film, Rating
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import random

module_dir = os.path.dirname(__file__)


def add_films(request):
    file_path = os.path.join(module_dir, "imdb_top_films.json")

    # Leer el archivo JSON
    with open(file_path, "r", encoding="utf-8") as f:
        films_data = json.load(f)

    for film_data in films_data:
        try:
            # Extraer el año y convertirlo a fecha
            released_year = int(film_data["Released_Year"])
            released_date = datetime.date(released_year, 1, 1)

            # Convertir duración a minutos
            duration_minutes = int(film_data["Runtime"].replace(" min", "").strip())

            # Convertir género al formato del modelo
            genre = film_data["Genre"].upper().replace(" ", "_")

            # Convertir certificado al formato del modelo
            certificate = film_data["Certificate"]
            if certificate not in [choice[0] for choice in Film.Certification.choices]:
                certificate = "PG-13"  # valor por defecto si no coincide

            new_film = Film(
                poster=film_data["Poster_Link"],
                title=film_data["Series_Title"],
                released=released_date,
                certificate=certificate,
                duration=duration_minutes,
                genre=genre,
                director=film_data["Director"],
                star1=film_data["Star1"],
                star2=film_data["Star2"],
                star3=film_data["Star3"],
                star4=film_data["Star4"],
                overview=film_data["Overview"],
            )
            new_film.save()

        except Exception as e:
            print(
                f"Error processing film {film_data.get('Series_Title', 'Unknown')}: {str(e)}"
            )
            continue

    return HttpResponse("Films added successfully")


def homepage(request):
    films = Film.objects.all()
    paginator = Paginator(films, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    random_number = round(random.uniform(1, 10), 2)
    context = {"films": films, "random_number": random_number, "page_obj": page_obj}
    return render(request, "films/homepage.html", context)


def film_detail(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    context = {"film": film}
    return render(request, "films/film_detail.html", context)
