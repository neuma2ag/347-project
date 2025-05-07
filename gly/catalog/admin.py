from django.contrib import admin
from .models import Tag, Recipe, Instruction, Ingredient

# Register your models here.
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Instruction)
admin.site.register(Ingredient)
