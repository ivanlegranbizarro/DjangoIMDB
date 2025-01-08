from django.db import models
from django.conf import settings


class Film(models.Model):
    class Genre(models.TextChoices):
        ACTION = "ACTION", "Action"
        DRAMA = "DRAMA", "Drama"
        COMEDY = "COMEDY", "Comedy"
        ROMANCE = "ROMANCE", "Romance"
        THRILLER = "THRILLER", "Thriller"
        HORROR = "HORROR", "Horror"
        SCIENCE_FICTION = "SCIENCE_FICTION", "Science Fiction"
        FANTASY = "FANTASY", "Fantasy"
        ANIMATION = "ANIMATION", "Animation"
        DOCUMENTARY = "DOCUMENTARY", "Documentary"
        HISTORY = "HISTORY", "History"
        CRIME = "CRIME", "Crime"
        FAR_WEST = "FAR_WEST", "Far West"

    class Certification(models.TextChoices):
        G = "G", "G"
        PG = "PG", "PG"
        PG_13 = "PG-13", "PG-13"
        R = "R", "R"
        NC_17 = "NC-17", "NC-17"

    title = models.CharField(max_length=250)
    released = models.DateField(auto_now=False, auto_now_add=False)
    certificate = models.CharField(max_length=5, choices=Certification.choices)
    duration = models.IntegerField(default=0)
    genre = models.CharField(max_length=250, choices=Genre.choices)
    director = models.CharField(max_length=250)
    star1 = models.CharField(max_length=250)
    star2 = models.CharField(max_length=250)
    star3 = models.CharField(max_length=250)
    star4 = models.CharField(max_length=250)
    overview = models.TextField(max_length=1000)
    poster = models.URLField(max_length=200)

    def __str__(self):
        return self.title


class Rating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.film} - {self.user}"
