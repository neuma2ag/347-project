from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/import', views.import_recipe, name='recipe-import'),
    path('recipe/<int:pk>/delete',
         views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/update',
         views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag-detail'),
    path('tags/', views.tags, name='tags'),
    path('tag/<int:pk>/delete', views.TagDeleteView.as_view(), name='tag-delete'),
    path('tag/<int:pk>/update', views.TagUpdateView.as_view(), name='tag-update'),
    path('tag/create', views.TagCreateView.as_view(), name='tag-create'),
]
