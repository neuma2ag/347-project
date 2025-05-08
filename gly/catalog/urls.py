from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/import', views.import_recipe, name='recipe-import'),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/update', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('tags/', views.tags, name='tags'),
]
