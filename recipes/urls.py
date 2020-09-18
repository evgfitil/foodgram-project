from django.urls import path

from .views import(
    AuthorRecipeListView, FavoriteListView, MyFollowListView, RecipeCreateFormView,
    RecipeEditFormView, RecipeDetailView, RecipeDelete, RecipeIndexListView,
    ShopingList, shoplist_download
)


urlpatterns = [
    path('author/<pk>/', AuthorRecipeListView.as_view(), name='author'),
    path('new', RecipeCreateFormView.as_view(), name='newrecipe'),
    path('favorites/', FavoriteListView.as_view(), name='favorites'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe'),
    path(
        'recipe/<int:pk>/edit/', RecipeEditFormView.as_view(), name='edit_recipe'
    ),
    path('recipe/<int:pk>/delete/', RecipeDelete.as_view(), name='delete_recipe'),
    path('mysubscriptions', MyFollowListView.as_view(), name='mysubscriptions'),
    path('shoplist', ShopingList.as_view(), name='shoplist'),
    path('shoplist/download/', shoplist_download, name='shoplist_download'),
    path('', RecipeIndexListView.as_view(), name='index'),
]
