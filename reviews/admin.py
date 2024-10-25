from django.contrib import admin
from .models import CustomUser, Ticket, Review, UserFollows

# Enregistrer les modèles dans l'administration
admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
