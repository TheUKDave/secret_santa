from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from . import default_email_content_template, default_email_subject_template
from .forms import ListCreationForm, PersonAddingForm
from .models import SantaList, Person


class HomepageView(TemplateView):
    template_name = 'santa/homepage.html'


class ListCreationView(CreateView):
    model = SantaList
    template_name_suffix = '_add'
    form_class = ListCreationForm

    def get_success_url(self):
        return reverse('santa:created', kwargs={'slug': self.object.slug})

    def get_initial(self):
        return {
            'email_content': default_email_content_template,
            'email_subject': default_email_subject_template
        }

    def form_valid(self, form):
        resp = super().form_valid(form)

        signup_url = self.object.get_signup_url(self.request)
        review_url = self.object.get_review_url(self.request)
        email = 'Congratulations.  You have created a Secret Santa list!\n\n'
        email += 'Here is the link that people can use to sign up to the list: {0}\n'
        email += 'And here is the link that you can use to review, and close the list: {1}'
        send_mail(
            'You created a Secret Santa list',
            email.format(signup_url, review_url),
            settings.DEFAULT_FROM_EMAIL,
            [self.object.organiser_email]
        )

        return resp


class ListCreatedView(DetailView):
    template_name = 'santa/created.html'
    model = SantaList

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['signup_url'] = self.object.get_signup_url(self.request)
        context['review_url'] = self.object.get_review_url(self.request)
        return context


class ReviewListView(TemplateView):
    template_name = 'santa/review.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug')
        secure_hash = self.kwargs.get('secure_hash')
        context['santa_list'] = get_object_or_404(SantaList, slug=slug, secure_hash_review=secure_hash)
        return context


class CloseListView(ReviewListView):
    template_name = 'santa/close.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        santa_list = context.pop('santa_list')
        santa_list.finish_list()
        return context


class SignupView(CreateView):
    model = Person
    template_name_suffix = '_add'
    form_class = PersonAddingForm
    success_url = '/thanks/'

    def get_initial(self):
        slug = self.kwargs.get('slug')
        secure_hash = self.kwargs.get('secure_hash')
        santa_list = get_object_or_404(SantaList, slug=slug, secure_hash_signup=secure_hash)
        return {'santa_list': santa_list}


class ThanksView(TemplateView):
    template_name = 'santa/thanks.html'
