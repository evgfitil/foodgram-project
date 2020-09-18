from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField()
    checkbox_style = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(max_length=30)
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)
    image = models.ImageField(upload_to='recipes/')
    description = models.TextField(max_length=1200)
    ingredients = models.ManyToManyField(
        Ingredient, through='Amount', through_fields=('recipe', 'ingredient')
    )
    tag = models.ManyToManyField(Tag, related_name='tag')
    prep_time = models.DurationField()

    def __str__(self):
        return self.name


class Amount(models.Model):
    units = models.IntegerField()
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient'
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ShopList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_to_shop'
    )
