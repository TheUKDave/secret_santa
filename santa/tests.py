from django.test import TestCase
from .models import Person, SantaList


class TestSantaList(TestCase):
    def setUp(self):
        subject = 'Secret Santa'
        content = "Hi {giver}, you are matched with {receiver}"
        self.list = SantaList.objects.create(name='test list', email_subject=subject, email_content=content)

        p1 = Person.objects.create(first_name='dave', last_name='x', email='dave@example.com', santa_list=self.list)
        p2 = Person.objects.create(first_name='bob', last_name='x', email='bob@example.com', santa_list=self.list)
        p3 = Person.objects.create(first_name='fred', last_name='x', email='fred@example.com', santa_list=self.list)

    def testShuffle(self):
        matched_pairs = self.list.shuffle_recipients()
        for pair in matched_pairs:
            self.assertNotEquals(pair[0], pair[1])

    def testData(self):
        matched_pairs = self.list.shuffle_recipients()
        email_data = self.list.get_email_data(matched_pairs)

    def testFinishList(self):
        self.list.finish_list()
        list_count = SantaList.objects.count()
        person_count = Person.objects.count()
        self.assertEquals(list_count, 0)
        self.assertEquals(person_count, 0)
