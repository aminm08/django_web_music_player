from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    MUSIC_CATG_CHOICES = (
        ('po','pop'),
        ('cl','classic'),
        ('ro','rock'),
        ('hi','hip hop'),
    )
    MUSIC_instrument_CHOICES = (
        ('pi', 'piano'),
        ('vi', 'violin'),
        ('gu', 'guitar'),
        ('fl', 'flute'),
    )

    favorite_musics = models.CharField(choices=MUSIC_CATG_CHOICES,max_length=2)
    favorite_instrument = models.CharField(choices=MUSIC_instrument_CHOICES,max_length=2)