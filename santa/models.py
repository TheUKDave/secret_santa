import random

from django.db import models
from django.core.mail import send_mass_mail


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()


class SantaList(models.Model):
    email_template = models.ForeignKey(EmailTemplate)


class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    santa_list = models.ForeignKey(SantaList)

    def __str__(self):
        return "{0} - ({1})".format(self.name, self.email)
