from django import template

from api.models import Follow, Favorite
from recipes.models import ShopList

register = template.Library()


@register.filter(name='get_filter_values')
def get_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()


@register.filter(name='shopping_count')
def shopping_count(request, user_id):
    return ShopList.objects.filter(user=user_id).count()


@register.filter(name='shopping_recipe')
def shopping_recipe(recipe, user):
    return ShopList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_following')
def is_following(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()
