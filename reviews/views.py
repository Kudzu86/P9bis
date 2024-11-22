from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Ticket, UserFollows
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, TicketForm, ReviewForm
from itertools import chain
from django.db.models import CharField, Value, Q


def register_view(request):
    """Vue pour gérer l'inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('feed')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def get_users_viewable_reviews(user):
    """Retourne les critiques des utilisateurs suivis par l'utilisateur donné
        et ses propres critiques."""
    # Récupère les utilisateurs suivis par l'utilisateur donné
    followed_users = UserFollows.objects.filter(user=user).values_list(
        'followed_user', flat=True
    )

    # Obtenir les critiques des utilisateurs suivis et les critiques
    # de l'utilisateur lui-même
    reviews = Review.objects.filter(user__in=followed_users).union(
        Review.objects.filter(user=user)
    )

    return reviews  # Retourne les critiques trouvées


def get_users_viewable_tickets(user):
    """Retourne les tickets des utilisateurs suivis par l'utilisateur donné
        et ses propres tickets."""
    # Récupère les utilisateurs suivis par l'utilisateur donné
    followed_users = UserFollows.objects.filter(user=user).values_list(
        'followed_user', flat=True
    )

    # Obtenir les tickets des utilisateurs suivis et les tickets
    #  de l'utilisateur lui-même
    tickets = Ticket.objects.filter(user__in=followed_users).union(
        Ticket.objects.filter(user=user)
    )

    return tickets  # Retourne les tickets trouvés


@login_required
def feed(request):
    user = request.user

    # Récupérer les utilisateurs suivis par l'utilisateur
    followed_users = UserFollows.objects.filter(user=user).values_list(
        'followed_user', flat=True
    )

    # Vérifier si la case pour afficher les posts de l'utilisateur est cochée
    show_user_posts = request.GET.get('show_user_posts', None) == 'on'

    # Récupérer les tickets qui ne sont pas des réponses
    tickets = Ticket.objects.filter(
        (Q(user=user) | Q(user__in=followed_users)) & Q(is_response=False)
    ).annotate(content_type=Value('TICKET', CharField()))

    # Récupérer toutes les critiques
    reviews = Review.objects.filter(
        Q(user=user) | Q(user__in=followed_users)
    ).annotate(content_type=Value('REVIEW', CharField()))

    # Ajouter l'attribut is_response pour chaque critique
    for review in reviews:
        review.is_critique_complete = (
            review.ticket is not None and review.user == review.ticket.user
        )
        review.is_response = (
            review.ticket is not None and review.ticket.user != request.user
        )
        review.is_reply = (
            review.ticket is not None and review.user != review.ticket.user
            if review.ticket else False
        )

    # Récupérer les critiques sur les tickets de l'utilisateur
    reviews_on_user_tickets = Review.objects.filter(
        ticket__user=user
    ).annotate(content_type=Value('REVIEW', CharField()))

    # Combiner les posts tout en éliminant les doublons
    combined_posts = list(chain(tickets, reviews, reviews_on_user_tickets))

    # Filtrer les posts en fonction de la case à cocher
    if not show_user_posts:
        combined_posts = [post for post in combined_posts if post.user != user]

    seen = set()
    unique_posts = []
    for post in combined_posts:
        if post.id not in seen:
            unique_posts.append(post)
            seen.add(post.id)

    # Trier les posts par date de création
    posts = sorted(
        unique_posts,
        key=lambda post: post.time_created,
        reverse=True
    )

    # Passer la valeur de show_user_posts au template
    return render(
        request, 'feed.html',
        {'posts': posts, 'show_user_posts': show_user_posts}
    )


def login_view(request):
    """Gère la connexion de l'utilisateur."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:  # Vérifie si l'utilisateur existe
                login(request, user)  # Connecte l'utilisateur
                messages.success(request, f"Bienvenue {username} !")
                return redirect('feed')
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe incorrect."
                )  # Message d'erreur si l'authentification échoue
        else:
            messages.error(
                request, "Erreur lors de la soumission du formulaire."
            )  # Message d'erreur si le formulaire est invalide
    else:
        # Crée un formulaire vide pour la première fois
        form = AuthenticationForm()
    # Rendu du template avec le formulaire d'authentification
    return render(request, 'login.html', {'form': form})


# Vue pour ajouter un billet
@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()

    return render(request, 'add_ticket.html', {'form': form})


# Vue pour modifier un billet existant
@login_required
def edit_ticket(request, ticket_id):
    # Récupère le billet à modifier grâce à son ID
    ticket = Ticket.objects.get(id=ticket_id)

    # Vérifie que l'utilisateur connecté est bien l'auteur du billet
    if ticket.user != request.user:
        return redirect('feed')

    if request.method == 'POST':
        # Remplit le formulaire avec les données soumises
        #  et les données du billet existant
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # Si une image est ajoutée
            # elle sera automatiquement gérée par le formulaire
            form.save()
            return redirect('feed')
    else:
        # Pré-remplit le formulaire avec les informations du billet existant
        form = TicketForm(instance=ticket)

    # Inclure le ticket dans le contexte
    context = {
        'form': form,
        'ticket': ticket,  # Inclut le ticket pour le header du template
    }
    return render(request, 'edit_ticket.html', context)


# Vue pour supprimer un billet
@login_required
def delete_ticket(request, ticket_id):
    # Récupère le billet à supprimer grâce à son ID
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        return redirect('feed')

    if request.method == 'POST':
        ticket.delete()  # Supprime le billet
        return redirect('feed')

    return render(request, 'delete_ticket.html', {'ticket': ticket})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')

    # Vérifier si l'utilisateur a déjà soumis une critique pour ce ticket
    user_review = reviews.filter(user=request.user).first()

    for review in reviews:
        # Vérifiez si la critique est une réponse à une critique autonome
        review.is_reply = (
            review.ticket is not None and review.user != review.ticket.user
        )

    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'reviews': reviews,
        'user_review': user_review,  # Passer la critique de l'utilisateur
    })


@login_required
def add_review(request):
    if request.method == "POST":
        # Récupérer l'ID du ticket à partir des données POST
        ticket_id = request.POST.get('ticket_id')

        if not ticket_id:
            return render(request, 'add_review.html', {
                'error': 'Aucun ID de ticket fourni.'
            })

        # Récupérer le ticket correspondant
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # Récupérer les données du formulaire
        rating = request.POST.get('rating')
        headline = request.POST.get('headline')
        body = request.POST.get('body')

        # Validation des champs requis
        if not headline or not rating:
            return render(request, 'add_review.html', {
                'error': 'Le titre et la note sont obligatoires.',
                'ticket': ticket
            })

        # Créer et enregistrer la critique associée au ticket
        review = Review(
            rating=rating,
            headline=headline,
            body=body,
            user=request.user,
            ticket=ticket
        )
        review.save()

        # Rediriger vers le détail du ticket
        return redirect('ticket_detail', ticket_id=ticket.id)

    # Si la méthode est GET
    ticket_id = request.GET.get('ticket_id')
    if ticket_id:
        # Tenter de récupérer le ticket
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        # Si aucun ticket_id n'est fourni, afficher un message d'erreur
        return render(request, 'add_review.html', {
            'error': 'Aucun ticket sélectionné pour ajouter une critique.'
        })

    # Afficher le formulaire avec le ticket existant
    return render(
        request, 'add_review.html',
        {'ticket': ticket, 'ticket_id': ticket.id}
    )


@login_required
def add_ticket_and_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid():
            # Sauvegarder le ticket en premier
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.is_response = True
            ticket.save()

            # Créer la critique associée au ticket créé
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket  # Associer le ticket fraîchement créé
            review.save()

            # Redirection vers la page de détails du ticket ou vers le feed
            return redirect('ticket_detail', ticket_id=ticket.id)

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'add_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


# Édition d'un avis existant
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket = review.ticket  # On récupère le ticket lié à l'avis

    # Vérifie si l'utilisateur connecté est le créateur du ticket et de l'avis
    is_creator = review.user == request.user and ticket.user == request.user

    if request.method == 'POST':  # Si le formulaire est soumis
        review.headline = request.POST.get('headline')
        review.body = request.POST.get('body')
        review.rating = request.POST.get('rating')
        review.save()  # Sauvegarde de la critique

        # Mise à jour des champs du ticket si l'utilisateur est le créateur
        if is_creator:
            ticket.title = request.POST.get('title', ticket.title)
            ticket.description = request.POST.get(
                'description', ticket.description
            )
            if 'image' in request.FILES:
                ticket.image = request.FILES['image']
            ticket.save()  # Sauvegarde des modifications du ticket

        # Redirection vers la vue de détail du ticket associé
        return redirect('ticket_detail', ticket_id=ticket.id)

    # Affiche un formulaire pré-rempli avec les données actuelles
    # de l'avis et du ticket si l'utilisateur est le créateur
    context = {
        'review': review,
        'ticket': ticket if is_creator else None
    }
    return render(request, 'edit_review.html', context)


# Suppression d'un avis
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ticket = review.ticket  # On récupère le ticket lié à l'avis

    # Vérifie si l'utilisateur connecté est le créateur du ticket et de l'avis
    is_creator = review.user == request.user and ticket.user == request.user

    if request.method == 'POST':
        # Supprime l'avis de la base de données
        review.delete()

        # Si l'utilisateur est aussi le créateur du ticket, on le supprime
        if is_creator:
            ticket.delete()

        # Redirection vers le flux ou autre page pertinente après suppression
        return redirect('feed')

    # Si la méthode est GET, affiche une page de confirmation de suppression
    return render(
        request, 'delete_review.html',
        {'review': review, 'ticket': ticket if is_creator else None}
    )


@login_required
def manage_follows(request):
    """Vue unique pour gérer les abonnements et les abonnés."""

    # Gérer l'ajout d'un nouvel utilisateur à suivre
    if request.method == 'POST':
        username_to_follow = request.POST.get('username')
        try:
            user_to_follow = get_user_model().objects.get(
                username=username_to_follow
            )  # Cherche l'utilisateur dans la base de données
            if user_to_follow == request.user:
                messages.error(
                    request, "Vous ne pouvez pas vous suivre vous-même."
                )
            elif UserFollows.objects.filter(
                user=request.user, followed_user=user_to_follow
            ).exists():  # Si déjà suivi
                messages.error(request, "Vous suivez déjà cet utilisateur.")
            else:
                UserFollows.objects.create(
                    user=request.user, followed_user=user_to_follow
                )  # Créer la relation de suivi
                messages.success(
                    request,
                    f"Vous suivez maintenant {user_to_follow.username}."
                )
        except get_user_model().DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas.")

        return redirect('manage_follows')

    # Récupérer les abonnements (users suivis par l'utilisateur connecté)
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).select_related('followed_user')

    # Récupérer les abonnés (utilisateurs qui suivent l'utilisateur connecté)
    followers = UserFollows.objects.filter(
        followed_user=request.user
    ).select_related('user')

    print("ici")
    print(followers)

    context = {
        'followed_users': followed_users,
        'followers': followers,
    }

    return render(request, 'manage_follows.html', context)


@login_required
def remove_follow(request, follow_id):
    """Vue pour supprimer un utilisateur suivi."""
    try:
        follow = UserFollows.objects.get(id=follow_id, user=request.user)
        follow.delete()
        messages.success(
            request,
            f"Vous avez cessé de suivre {follow.followed_user.username}."
        )
    except UserFollows.DoesNotExist:
        messages.error(request, "Relation de suivi introuvable.")

    return redirect('manage_follows')


def user_posts(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Récupérer les tickets, reviews et réponses de l'utilisateur connecté
    tickets = Ticket.objects.filter(user=request.user, is_response=False)
    reviews = Review.objects.filter(
        user=request.user, ticket__user=request.user
    )

    # Filtrer les réponses basées sur les critiques
    responses = Review.objects.filter(user=request.user).exclude(
        ticket__user=request.user
    )

    return render(request, 'posts.html', {
        'tickets': tickets,
        'reviews': reviews,
        'responses': responses,
    })


def response_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()  # Sauvegarder la critique
            return redirect(
                'ticket_detail', ticket_id=ticket.id
            )  # Redirection vers le détail du ticket
    else:
        form = ReviewForm()

    return render(
        request,
        'response_ticket.html',
        {'ticket': ticket, 'form': form}
    )


@login_required
def response_detail(request, review_id):
    # Récupérer la critique par ID
    review = get_object_or_404(Review, id=review_id)
    ticket = review.ticket  # Récupérer le ticket associé

    return render(request, 'response_detail.html', {
        'review': review,
        'ticket': ticket
    })
