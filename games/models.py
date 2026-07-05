from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    year_of_release = models.IntegerField()
    genre = models.CharField(max_length = 50)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game.title} - {self.rating}/10"