from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ticket, Review

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'}),
        error_messages={'invalid': 'Veuillez entrer une date valide au format JJ-MM-AAAA.'}
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'gender')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du livre/article'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']  # Utilisation des champs que vous souhaitez

        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la critique'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre commentaire ici...'}),
        }
