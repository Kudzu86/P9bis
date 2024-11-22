"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
# Importations nécessaires pour la configuration des URLs
from django.contrib import admin
from django.urls import path
from reviews import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.login_view, name='login'),
    path('', views.feed, name='feed'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ticket/add/', views.add_ticket, name='add_ticket'),
    path(
        'ticket/<int:ticket_id>/edit/', views.edit_ticket,
        name='edit_ticket'
    ),
    path(
        'ticket/<int:ticket_id>/delete/', views.delete_ticket,
        name='delete_ticket'
    ),
    path('review/add/', views.add_review, name='add_review'),
    path(
        'review/<int:review_id>/edit/', views.edit_review,
        name='edit_review'
    ),
    path(
        'review/<int:review_id>/delete/', views.delete_review,
        name='delete_review'
    ),
    path('follows/', views.manage_follows, name='manage_follows'),
    path(
        'follows/<int:follow_id>/remove/', views.remove_follow,
        name='remove_follow'
    ),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path(
        'ticket/<int:ticket_id>/response/', views.response_ticket,
        name='response_ticket'
    ),
    path('posts/', views.user_posts, name='posts'),
    path(
        'add_ticket_and_review/', views.add_ticket_and_review,
        name='add_ticket_and_review'
    )

]

# Configuration pour servir les fichiers médias en mode débogage
# (lorsque settings.DEBUG est True)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
