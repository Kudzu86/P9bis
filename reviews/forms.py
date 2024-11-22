from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ticket, Review


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY', 'id': 'id_birth_date'}),  
        error_messages={
            'invalid': 'Veuillez entrer une date valide au format JJ-MM-AAAA.'
        }
    )

    # Ajout d'un id explicite pour `username` et `password1`
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'id': 'id_username'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'id': 'id_password1'})
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'id': 'id_password2'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'gender')



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Titre du livre/article'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Description'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Titre de la critique'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Votre commentaire ici...'
                }
            ),
        }
