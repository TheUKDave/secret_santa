from django import forms
from .models import SantaList, Person


class PersonAddingForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = []
        widgets = {'santa_list': forms.HiddenInput()}


class ListCreationForm(forms.ModelForm):

    class Meta:
        model = SantaList
        exclude = ['slug', 'secure_hash']
