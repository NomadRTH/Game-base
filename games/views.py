from django.http import  Http404
from .models import Game
from .models import Review
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
 
def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        review = ReviewForm()
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    return render (request, "games/detail.html", {"game": game, "review": review })


def index(request):
    games = Game.objects.all()
    genre = request.GET.get("genre")
    if genre:
        games = games.filter(genre=genre)
    title = request.GET.get("title")
    if title:
        games = games.filter(title__icontains=title)
    paginator = Paginator(games, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    genres = Game.objects.values_list("genre", flat=True).distinct().order_by("genre")
    titles = Game.objects.values_list("title", flat=True).distinct().order_by("title")
    return render(request, "games/index.html", {"page_obj": page_obj,"genres": genres,"selected_genre": genre, "query": title if title else "", })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/games/")
    else:
        form = UserCreationForm()
    return render(request, "games/register.html", {"form": form})   
            

def person(request):
    context = {
        "user":request.user
    }
    return render(request, "games/person.html", context)


def add_review(request, game_id):
    if request.method != "POST":
        return redirect("games:detail", game_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
       review = form.save(commit=False)
       review.game = Game.objects.get(pk=game_id)
       review.user = request.user
       review.save()
       return redirect("games:detail", game_id)
    return render(request, "games/detail.html",  {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user:
        return redirect("games:detail", game_id=review.game.id)
    
    game_id = review.game.id
    review.delete()
    
    return redirect("games:detail", game_id=game_id)
    
