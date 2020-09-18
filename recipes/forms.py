from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Tag, Recipe


class TagsFilter(forms.Form):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple(),
        to_field_name='slug'
    )


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'name', 'image', 'description', 'tag', 'prep_time'
        )
        widgets = {'tag': forms.CheckboxSelectMultiple(), }
