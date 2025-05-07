from django import forms
from django.core.exceptions import ValidationError
from recipe_scrapers import scrape_me
from recipe_scrapers import WebsiteNotImplementedError

from .models import Recipe, Instruction, Ingredient, Tag


class ImportRecipeForm(forms.Form):
    url = forms.URLField(
        max_length=2000, help_text="Enter the URL of the recipe to import")
    tag_text = forms.CharField(
        max_length=256, help_text="Enter a comma-separated list of tags", required=False)

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

        tag_text = cleaned_data['tag_text']
        if not tag_text:
            tag_text = ''
        tag_texts = [x.strip() for x in cleaned_data['tag_text'].split(',')]
        tag_texts = [x for x in tag_texts if x]
        tags = []
        for name in tag_texts:
            existing_tag = Tag.objects.filter(name=name).first()
            if existing_tag:
                tag = existing_tag
            else:
                tag = Tag()
                tag.name = name
                tag.save()
            tags.append(tag)
        cleaned_data['tags'] = tags

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
        recipe.tag.set(cleaned_data['tags'])
        return recipe
