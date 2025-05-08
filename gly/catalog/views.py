from django.shortcuts import render, redirect
from django.views import generic

from .models import Tag, Recipe
from .forms import ImportRecipeForm


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


def import_recipe(request):
    if request.method == 'POST':
        form = ImportRecipeForm(request.POST, user=request.user)
        if form.is_valid():
            recipe = form.save()
            return redirect(recipe.get_absolute_url())
    else:
        form = ImportRecipeForm()

    context = {
        'form': form
    }
    return render(request, 'catalog/recipe_import.html', context=context)


class RecipeDeleteView(generic.DeleteView):
    model = Recipe
    success_url = '/catalog'


def tags(request):
    context = {
        'tags': Tag.objects.all()
    }
    return render(request, 'catalog/tags.html', context=context)
