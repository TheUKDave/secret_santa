from django.test import TestCase
from .models import Person, SantaList


class TestSantaList(TestCase):
    def setUp(self):
        subject = 'Secret Santa'
        content = "Hi {giver}, you are matched with {receiver}"
        self.list = SantaList.objects.create(name='test list', email_subject=subject, email_content=content)

        p1 = Person.objects.create(name='Dave', email='dave@theukdave.com', santa_list=self.list)
        p2 = Person.objects.create(name='Bob', email='bob@theukdave.com', santa_list=self.list)
        p3 = Person.objects.create(name='Fred', email='fred@theukdave.com', santa_list=self.list)

    def testShuffle(self):
        matched_pairs = self.list.shuffle_recipients()
        for pair in matched_pairs:
            self.assertNotEquals(pair[0], pair[1])

    def testData(self):
        matched_pairs = self.list.shuffle_recipients()
        email_data = self.list.get_email_data(matched_pairs)
        self.list.send_email()
