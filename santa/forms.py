from django import forms
from .models import SantaList, Person


class PersonAddingForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = []
        widgets = {'santa_list': forms.HiddenInput()}
        labels = {
            "email": "Your email"
        }


class ListCreationForm(forms.ModelForm):

    class Meta:
        model = SantaList
        exclude = ['slug', 'secure_hash_signup', 'secure_hash_review']
        labels = {
            "name": "List name",
            "organiser_email": "Your email"
        }
