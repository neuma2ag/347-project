from django.shortcuts import render
from django.views import generic

from .models import Tag, Recipe

def index(request):
    num_tags = Tag.objects.all().count()
    num_recipes = Recipe.objects.all().count()
    recipes = Recipe.objects.all()

    context = {
        'num_tags': num_tags,
        'num_recipes': num_recipes,
        'recipes': recipes,
    }

    return render(request, 'index.html', context=context)


class RecipeDetailView(generic.DetailView):
    model = Recipe
