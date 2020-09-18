import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.http import Http404, HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import redirect, reverse

from api.models import Follow

from .extras import create_ingredients_amounts, get_all_tags
from .forms import RecipeForm
from .models import Recipe, ShopList, User


class RecipeIndexListView(ListView):

    model = Recipe
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(tag__slug__in=filters).distinct()

        return qs.order_by('-pub_date')

    def get_user_favorites(self):
        user = self.request.user
        return Recipe.objects.filter(favrecipe__user=user).values_list(
            'id', flat=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})

        if self.request.user.is_authenticated:
            context.update({'user_favorites': self.get_user_favorites()})

        return context


class RecipeDetailView(DetailView):

    model = Recipe
    template_name = 'recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            fav_recipes = Recipe.objects.filter(
                favrecipe__user=self.request.user
            ).values_list(
                'id', flat=True
            )
            if self.object.id in fav_recipes:
                context.update({'is_favorite': True})
        return context


class AuthorRecipeListView(RecipeIndexListView):

    model = Recipe
    template_name = 'author.html'
    paginate_by = 6

    def get_queryset(self):
        cur_user = User.objects.get(id=self.kwargs['pk'])
        qs = Recipe.objects.filter(author=cur_user)

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(tag__slug__in=filters).distinct()

        return qs.order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = User.objects.get(id=self.kwargs['pk'])
        context['username'] = author
        if self.request.user.is_authenticated:
            fav_authors = Follow.objects.filter(
                user=self.request.user
            ).values_list(
                'id', flat=True
            )
            if author.id in fav_authors:
                context.update({'is_following': True})
        return context


class FavoriteListView(LoginRequiredMixin, RecipeIndexListView):

    model = Recipe
    template_name = 'favorite.html'
    paginate_by = 6

    def get_queryset(self):
        author = self.request.user
        qs = Recipe.objects.filter(favrecipe__user=author).all()

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(tag__slug__in=filters).distinct()

        return qs.order_by('-pub_date')


class MyFollowListView(LoginRequiredMixin, ListView):

    model = Recipe
    template_name = 'mysubscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_user = self.request.user
        authors = User.objects.filter(following__user=cur_user)
        context['authors'] = authors
        fav_recipes = {}
        for author in authors:
            fav_recipes[author] = Recipe.objects.filter(
                author=author
            ).order_by('-pub_date')[:3]
        context['fav_recipes'] = fav_recipes

        return context


class RecipeCreateFormView(LoginRequiredMixin, CreateView):

    form_class = RecipeForm
    template_name = 'formrecipe.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        form_data = form.data
        instance.save()
        create_ingredients_amounts(instance, form_data)
        form.save_m2m()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})

        return context


class RecipeEditFormView(LoginRequiredMixin, UpdateView):

    form_class = RecipeForm
    model = Recipe
    template_name = 'formrecipe.html'
    template_name_field = 'instance'

    def form_valid(self, form):
        instance = form.save(commit=False)
        form_data = form.data
        instance.amount_set.all().delete()
        instance.save()
        create_ingredients_amounts(instance, form_data)
        form.save_m2m()
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404('Вы не являетесь автором данного рецепта')

        return super(RecipeEditFormView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('recipe', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': get_all_tags()})
        context.update({'is_edit': True})

        return context


class RecipeDelete(LoginRequiredMixin, DeleteView):

    model = Recipe
    success_url = '/'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_object(self, queryset=None):
        instance = super(RecipeDelete, self).get_object()
        if instance.author != self.request.user:
            raise Http404('Вы не являетесь автором данного рецепта')

        return instance


class ShopingList(ListView):

    model = ShopList
    template_name = 'shoplist.html'


def shoplist_download(request):
    recipes = Recipe.objects.filter(recipe_to_shop__user=request.user)
    ingredients = recipes.annotate(
        title=F('amount__ingredient__name'),
        units=F('amount__ingredient__unit')
    ).values('title', 'units').order_by('title').annotate(
        total=Sum('amount__units'
    ))
    response = HttpResponse(content_type='text/text')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'

    writer = csv.writer(response)
    writer.writerow([f'Список покупок: {request.user.get_full_name()}'])
    writer.writerow([])
    writer.writerow(['Блюда:'])
    for recipe in recipes:
        writer.writerow([recipe.name])
    writer.writerow([])
    writer.writerow(['Ингредиенты:'])
    for ingredient in ingredients:
        if ingredient['title']:
            name = ingredient['title']
            dimension = ingredient['units']
            total = ingredient['total']
            writer.writerow([f'{name} - {total} {dimension}'])

    return response
