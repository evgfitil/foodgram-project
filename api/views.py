import json

from django.db.models import F
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Ingredient, ShopList
from .models import Favorite, Follow, User


class FavoriteView(View):

    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if recipe_id is None or recipe is None:

            return JsonResponse({'success': False})

        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():

            return JsonResponse({'success': False})

        Favorite.objects.get_or_create(user=request.user, recipe=recipe)

        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).delete()
        if removed:
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


class SubscribeView(View):

    def post(self, request):
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)

        if request.user == author or Follow.objects.filter(
                user=request.user, author=author).exists():
            return JsonResponse({'success': False})

        Follow.objects.create(user=request.user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()
        if removed:
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


class GetIngredientsView(View):

    def get(self, request):
        qs = request.GET.get('query')
        ingredients = list(Ingredient.objects.filter(
            name__istartswith=qs).annotate(
            title=F('name'), dimension=F('unit')).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class PurchasesView(View):

    def post(self, request):
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        ShopList.objects.get_or_create(user=request.user, recipe=recipe)

        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        count, _ = ShopList.objects.filter(
            user=request.user,
            recipe=recipe_id,
        ).delete()

        return JsonResponse({'success': True if count else False})
