from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.conf import settings
import random


def random_color():
    color = random.randrange(0, 2**24)
    color = hex(color)
    color = "#" + color[2:]
    return color


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            help_text="Enter a tag for recipes")

    color = models.CharField(max_length=7, default=random_color)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular tag instance."""
        return reverse('tag-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='tag_name_case_insensitive_unique',
                violation_error_message="Tag already exists (case insensitive match)"
            ),
        ]


class Recipe(models.Model):
    title = models.CharField(
        max_length=128, help_text="Enter the title of the recipe")

    prep_time = models.IntegerField(
        help_text="Enter the minutes of prep time", default=0)

    cook_time = models.IntegerField(
        help_text="Enter the minutes of cook time", default=0)

    servings = models.CharField(max_length=32,
                                help_text="Enter the number of servings", default="")

    tag = models.ManyToManyField(
        Tag, help_text="Select a tag for this recipe", default=[])

    url = models.CharField(
        max_length=2000, help_text="The original recipe URL", null=True, blank=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    picture = models.ImageField(upload_to="images/", default="food.jpg")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])


class Instruction(models.Model):
    content = models.CharField(
        max_length=256, help_text="Enter the text for the instruction")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='instructions')
    step = models.IntegerField(help_text="Enter the step number")

    def __str__(self):
        return self.content


class Ingredient(models.Model):
    content = models.CharField(
        max_length=256, help_text="Enter the text for the ingredient")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.content
