from django.urls import path
from films.views import homepage, film_detail, add_films

app_name = "films"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("<int:film_id>/", film_detail, name="detail"),
    path("add_films/", add_films, name="add_films"),
]
