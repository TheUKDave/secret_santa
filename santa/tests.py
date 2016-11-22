from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse

from . import default_email_subject_template, default_email_content_template
from .models import Person, SantaList


class TestSantaList(TestCase):
    def setUp(self):
        subject = 'Secret Santa'
        content = "Hi {giver}, you are matched with {receiver}"
        self.list = SantaList.objects.create(name='test list', email_subject=subject, email_content=content)

        p1 = Person.objects.create(first_name='dave', last_name='x', email='dave@example.com', santa_list=self.list)
        p2 = Person.objects.create(first_name='bob', last_name='x', email='bob@example.com', santa_list=self.list)
        p3 = Person.objects.create(first_name='fred', last_name='x', email='fred@example.com', santa_list=self.list)

    @patch('django.core.mail.send_mail')
    def testCreateList(self, mail_mock):
        response = self.client.get(reverse('santa:create'))
        form_data = {
            'name': 'test list 2',
            'organiser_email': 'test@example.com',
            'email_subject': default_email_subject_template,
            'email_content': default_email_content_template,
        }
        response = self.client.post(reverse('santa:create'), form_data)

        # Check we now have a second list in the system
        list_count = SantaList.objects.count()
        self.assertEquals(list_count, 2)
        # We should still only have the original 3 persons in the system
        person_count = Person.objects.count()
        self.assertEquals(person_count, 3)

        # Check an email was sent out
        self.assertEquals(mail_mock.called, True)

    def testShuffle(self):
        matched_pairs = self.list.shuffle_recipients()
        for pair in matched_pairs:
            self.assertNotEquals(pair[0], pair[1])

    def testData(self):
        matched_pairs = self.list.shuffle_recipients()
        email_data = self.list.get_email_data(matched_pairs)

    @patch('django.core.mail.send_mass_mail')
    def testFinishList(self, mail_mock):
        self.list.finish_list()
        list_count = SantaList.objects.count()
        person_count = Person.objects.count()
        self.assertEquals(list_count, 0)
        self.assertEquals(person_count, 0)
        self.assertEquals(mail_mock.called, True)
