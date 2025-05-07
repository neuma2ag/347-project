from django.shortcuts import render

from .models import Tag, Recipe

# Create your views here.


def index(request):
    num_tags = Tag.objects.all().count()
    num_recipes = Recipe.objects.all().count()

    context = {
        'num_tags': num_tags,
        'num_recipes': num_recipes,
    }

    return render(request, 'index.html', context=context)
