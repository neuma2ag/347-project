from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            help_text="Enter a tag for recipes")

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

    prep_time = models.IntegerField(help_text="Enter the minutes of prep time")

    cook_time = models.IntegerField(help_text="Enter the minutes of cook time")

    servings = models.IntegerField(help_text="Enter the number of servings")

    tag = models.ManyToManyField(Tag, help_text="Select a tag for this recipe")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])
