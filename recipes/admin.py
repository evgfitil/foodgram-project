from django.contrib import admin

from api.models import Favorite, Follow

from .models import Amount, Ingredient, Recipe, Tag, ShopList


class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tag', 'ingredients',)
    list_filter = ('author', 'name', 'tag',)
    list_display = (
        'name', 'author', 'count_favorited'
    )
    ordering = ['name', ]
    autocomplete_fields = ('ingredients',)
    readonly_fields = ('count_favorited',)

    def count_favorited(self, obj):
        count = Favorite.objects.filter(recipe=obj).count()
        return count


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    ordering = ['name', ]
    list_filter = ('name',)
    search_fields = ('name',)


class AmountAdmin(admin.ModelAdmin):
    list_display = ('units', 'ingredient', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(ShopList)
