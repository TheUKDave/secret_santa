import random
import itertools
import hashlib

from django.db import models
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse


class SantaList(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    organiser_email = models.EmailField(max_length=200, verbose_name="Your email")
    email_subject = models.CharField(max_length=200)
    email_content = models.TextField()
    secure_hash = models.CharField(max_length=12, unique=True, null=True)

    def __str__(self):
        return "{0}".format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        orig_slug = self.slug
        for i in itertools.count(1):
            if not SantaList.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
                break

            self.slug = '%s-%d' % (orig_slug, i)

        super().save(*args, **kwargs)

        if not self.secure_hash:
            token = "{0}{1}".format(self.pk, self.slug)
            self.secure_hash = hashlib.md5(token.encode('utf-8')).hexdigest()[:12]
            self.save()
        else:
            path = reverse('santa:signup', kwargs={'secure_hash': self.secure_hash, 'slug': self.slug})
            send_mail(
                'You created a Secret Santa list',
                'Here is the link: {0}'.format(path),
                settings.DEFAULT_FROM_EMAIL,
                [self.organiser_email]
            )

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
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    santa_list = models.ForeignKey(SantaList)

    def __str__(self):
        return "{0} - ({1})".format(self.name, self.email)
