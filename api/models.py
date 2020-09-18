from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe


User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userfav'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favrecipe'
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
