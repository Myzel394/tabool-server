from django.core.exceptions import ValidationError

from apps.django.extra.poll.mixins.tests import PollTestMixin
from apps.django.extra.poll.models import Vote
from apps.django.extra.poll.utils import has_voted
from apps.django.utils.tests import ClientTestMixin, UserTestMixin


class PollTest(UserTestMixin, PollTestMixin):
    def test_create_invalid_max_vote_choices(self):
        poll = self.Create_poll(choices=["Ja", "Nein"])
        
        with self.assertRaises(ValidationError):
            poll.max_vote_choices = 2
            poll.save()


class APITest(ClientTestMixin, UserTestMixin, PollTestMixin):
    def setUp(self):
        self.user = self.Login_user()
        self.__class__.associated_user = self.user
        self.poll = self.Create_poll()
    
    def vote(self):
        response = self.client.post(f"/api/data/poll/{self.poll.id}/vote/", {
            "poll": self.poll.id,
            "choices": [self.poll.choices[0].id],
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertTrue(has_voted(self.poll, self.user))
        self.assertEqual(1, Vote.objects.filter(associated_user=self.user).count())
    
    def test_vote(self):
        self.vote()
    
    def test_vote_two_times_invalid(self):
        self.vote()
        response = self.client.post(f"/api/data/poll/{self.poll.id}/vote/", {
            "poll": self.poll.id,
            "choices": [self.poll.choices[1].id],
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
        self.assertTrue(has_voted(self.poll, self.user))
        self.assertEqual(1, Vote.objects.filter(associated_user=self.user).count())
    
    def test_get_empty_selections_before_vote(self):
        response = self.client.get(f"/api/data/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        self.assertEqual([], response.data["user_selections"])
    
    def test_get_correct_selections_after_vote(self):
        self.vote()
        
        response = self.client.get(f"/api/data/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(1, len(response.data["user_selections"]))
        self.assertEqual([self.poll.choices[0].id], list(response.data["user_selections"]))
