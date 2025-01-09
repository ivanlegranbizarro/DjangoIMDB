from django.db import models
from django.conf import settings
from django.forms import ValidationError


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
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Rating(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        # Asegura que un usuario solo puede dar un rating por película
        unique_together = ["film", "user"]

    def clean(self):
        # Validación del rating (por ejemplo, entre 1 y 5)
        if not 1 <= self.rating <= 5:
            raise ValidationError("El rating debe estar entre 1 y 5")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta las validaciones
        super().save(*args, **kwargs)

        # Recalcula el promedio y el total
        avg = (
            Rating.objects.filter(film=self.film).aggregate(models.Avg("rating"))[
                "rating__avg"
            ]
            or 0
        )

        # Actualiza el film
        Film.objects.filter(id=self.film.id).update(
            average_rating=avg,
            total_ratings=Rating.objects.filter(film=self.film).count(),
        )

    def __str__(self):
        return f"{self.film} - {self.user}"
