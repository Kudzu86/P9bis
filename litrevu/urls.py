"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
# Importations nécessaires pour la configuration des URLs
from django.contrib import admin
from django.urls import path
from reviews import views  # Import des vues personnalisées dans l'application "reviews"
from django.contrib.auth.views import LogoutView  # Vue par défaut pour la déconnexion
from django.conf import settings  # Pour accéder aux paramètres de l'application
from django.conf.urls.static import static  # Pour servir les fichiers statiques durant le développement

# Définition des routes de l'application
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # URL pour l'accès à l'interface d'administration
    path('login/', views.login_view, name='login'),  # Route pour la connexion des utilisateurs
    path('', views.feed, name='feed'),  # Route pour le fil d'actualité (page d'accueil)
    path('register/', views.register_view, name='register'),  # Route pour l'inscription d'un nouvel utilisateur
    path('logout/', LogoutView.as_view(), name='logout'),  # Route pour la déconnexion des utilisateurs
    path('ticket/add/', views.add_ticket, name='add_ticket'),  # Route pour ajouter un ticket (livre/article)
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),  # Route pour éditer un ticket existant
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),  # Route pour supprimer un ticket
    path('review/add/', views.add_review, name='add_review'),  # Route pour ajouter une critique
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),  # Route pour éditer une critique existante
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),  # Route pour supprimer une critique
    path('follows/', views.manage_follows, name='manage_follows'),  # Route pour gérer les suivis
    path('follows/<int:follow_id>/remove/', views.remove_follow, name='remove_follow'),  # Route pour retirer un suivi
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),  # Route pour afficher le détail d'un ticket
    path('ticket/<int:ticket_id>/response/', views.ticket_response, name='ticket_response'),  # Route pour répondre à un ticket
    path('posts/', views.user_posts, name='posts'),  # Route pour afficher les posts d'un utilisateur
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),  # Route pour afficher le détail d'une critique
    path('add_ticket_and_review/', views.add_ticket_and_review, name='add_ticket_and_review'),
]

# Configuration pour servir les fichiers médias en mode débogage (lorsque settings.DEBUG est True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
