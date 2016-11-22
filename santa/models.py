import random
import itertools
import hashlib

from django.db import models
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site

from . import creation_email_subject, creation_email_content


class SantaList(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    organiser_email = models.EmailField(max_length=200)
    email_subject = models.CharField(max_length=200)
    email_content = models.TextField()

    # For people to sign up
    secure_hash_signup = models.CharField(max_length=12, unique=True, null=True)
    # For the organiser to review/close
    secure_hash_review = models.CharField(max_length=12, unique=True, null=True)

    def __str__(self):
        return "{0}".format(self.name)

    def get_signup_url(self, request):
        current_site = get_current_site(request)
        secure_hash = self.secure_hash_signup
        slug = self.slug
        signup_path = reverse('santa:signup', kwargs={'secure_hash': secure_hash, 'slug': slug})
        return "{0}{1}".format(current_site.domain, signup_path)

    def get_review_url(self, request):
        current_site = get_current_site(request)
        secure_hash = self.secure_hash_review
        slug = self.slug
        review_path = reverse('santa:review', kwargs={'secure_hash': secure_hash, 'slug': slug})
        return "{0}{1}".format(current_site.domain, review_path)

    def send_creation_email(self, request):
        signup_url = self.get_signup_url(self.request)
        review_url = self.get_review_url(self.request)
        send_mail(
            creation_email_subject,
            creation_email_content.format(signup_url, review_url),
            settings.DEFAULT_FROM_EMAIL,
            [self.organiser_email]
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        orig_slug = self.slug
        for i in itertools.count(1):
            if not SantaList.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
                break

            self.slug = '%s-%d' % (orig_slug, i)

        super().save(*args, **kwargs)

        if not self.secure_hash_signup or not self.secure_hash_review:
            token = "{0}{1}".format(self.pk, self.slug)
            md5 = hashlib.md5(token.encode('utf-8')).hexdigest()
            self.secure_hash_signup = md5[:12]
            self.secure_hash_review = md5[12:24]
            self.save()

    def get_email_data(self, pairs):
        data_list = []
        for giver, receiver in pairs:
            email_to = ["Santa's Little Helper <{0}>".format(giver.email)]
            content = self.email_content.format(giver=giver.name, receiver=receiver.name)
            subject = self.email_subject.format(giver=giver.name, receiver=receiver.name)
            data_item = (subject, content, settings.DEFAULT_FROM_EMAIL, email_to)
            data_list.append(data_item)

        return tuple(data_list)

    def shuffle_recipients(self):
        matches = {}
        # Get all the people on this list, and shuffle them
        person_list = list(self.person_set.all())
        random.shuffle(person_list)

        # Now that the list is randomised, just match each person, to the next person in the list
        for i, person in enumerate(person_list):
            try:
                matches[person] = person_list[i+1]
            except IndexError:
                # This is the last person on the list, so match them to the first person, who's currently unmatched
                matches[person] = person_list[0]

        # Return a tuple of ((giver, receiver,) ...)
        return matches.items()

    def finish_list(self):
        pairs = self.shuffle_recipients()
        data = self.get_email_data(pairs)
        send_mass_mail(data)
        self.person_set.all().delete()
        self.delete()


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    santa_list = models.ForeignKey(SantaList)

    @property
    def name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{0} - ({1})".format(self.name, self.email)
