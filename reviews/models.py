from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    is_response = models.BooleanField(default=False)  # Nouveau champ pour indiquer si le ticket est une réponse

    def __str__(self):
        return self.title

class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(  # Champ pour la note, un entier positif
        # valide que la note doit être entre 0 et 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])  # Validateurs pour limiter les valeurs
    headline = models.CharField(max_length=255)  # Titre de la critique
    body = models.TextField()  # Corps de la critique
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Champ d'image pour la critique
    time_created = models.DateTimeField(auto_now_add=True)  # Date de création du ticket

    def __str__(self):
        return self.headline

class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')  # Utilisateur qui suit
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'followed_user')  # Chaque relation de suivi doit être unique

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

