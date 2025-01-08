from django.shortcuts import render
from films.models import Film, Rating
from django.shortcuts import get_object_or_404
import random

# Create your views here.


def homepage(request):
    films = Film.objects.all()
    random_number = round(random.uniform(1, 10), 2)
    context = {"films": films, "random_number": random_number}
    return render(request, "films/homepage.html", context)


def film_detail(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    context = {"film": film}
    return render(request, "films/film_detail.html", context)
