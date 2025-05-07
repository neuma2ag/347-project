from django import forms
from django.core.exceptions import ValidationError
from recipe_scrapers import scrape_me
from recipe_scrapers import WebsiteNotImplementedError

from .models import Recipe, Instruction, Ingredient


class ImportRecipeForm(forms.Form):
    url = forms.URLField(
        max_length=2000, help_text="Enter the URL of the recipe to import")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        url = cleaned_data['url']
        try:
            scraper = scrape_me(url)
        except WebsiteNotImplementedError:
            raise ValidationError("This website is not currently supported")

        if not scraper.title():
            raise ValidationError(
                "This website failed to provide a title for the recipe")
        cleaned_data['title'] = scraper.title()

        if scraper.prep_time():
            cleaned_data['prep_time'] = scraper.prep_time()

        if scraper.cook_time():
            cleaned_data['cook_time'] = scraper.cook_time()

        if scraper.yields():
            cleaned_data['servings'] = scraper.yields()

        instructions = []
        for content in scraper.instructions_list():
            instruction = Instruction()
            instruction.content = content
            instruction.save()
            instructions.append(instruction)
        cleaned_data['instructions'] = instructions

        ingredients = []
        for content in scraper.ingredients():
            ingredient = Ingredient()
            ingredient.content = content
            ingredient.save()
            ingredients.append(ingredient)
        cleaned_data['ingredients'] = ingredients

        cleaned_data['creator'] = self.user

        return cleaned_data

    def save(self):
        recipe = Recipe()
        cleaned_data = self.cleaned_data
        recipe.title = cleaned_data['title']
        recipe.prep_time = cleaned_data['prep_time']
        recipe.cook_time = cleaned_data['cook_time']
        recipe.servings = cleaned_data['servings']
        recipe.url = cleaned_data['url']
        recipe.creator = cleaned_data['creator']
        recipe.save()
        recipe.instructions.set(cleaned_data['instructions'])
        recipe.ingredients.set(cleaned_data['ingredients'])
        return recipe
