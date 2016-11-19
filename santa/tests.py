from django.test import TestCase
from .models import EmailTemplate, Person, SantaList


class TestSantaList(TestCase):
    def test_model_linking(self):
        e = EmailTemplate.objects.create(subject='Secret Santa', content="Hi {giver}, you are matched with {receiver}")
        self.list = SantaList.objects.create(email_template=e)

        p1 = Person.objects.create(name='Dave', email='dave@example.com', santa_list=self.list)
        p2 = Person.objects.create(name='Bob', email='bob@example.com', santa_list=self.list)
        p3 = Person.objects.create(name='Fred', email='fred@example.com', santa_list=self.list)
