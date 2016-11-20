from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .forms import ListCreationForm, PersonAddingForm
from .models import SantaList, Person


class HomepageView(TemplateView):
    template_name = 'homepage.html'


class ListCreationView(CreateView):
    model = SantaList
    template_name_suffix = '_add'
    form_class = ListCreationForm

    def get_success_url(self):
        return reverse('santa:created', kwargs={'slug': self.object.slug})


class ListCreatedView(DetailView):
    template_name = 'santa/created.html'
    model = SantaList


class SignupView(CreateView):
    model = Person
    template_name_suffix = '_add'
    form_class = PersonAddingForm
    success_url = '/thanks/'

    def get_initial(self):
        santa_list = get_object_or_404(SantaList, slug=self.kwargs.get('slug'))
        return {'santa_list': santa_list}


class ThanksView(TemplateView):
    template_name = 'santa/thanks.html'
