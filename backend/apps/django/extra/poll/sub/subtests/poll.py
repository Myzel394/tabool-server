from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.test import override_settings

from apps.django.authentication.user.mixins import UserTestMixin
from apps.django.extra.poll.mixins.tests import PollTestMixin
from apps.django.extra.poll.models import Poll, Vote
from apps.django.extra.poll.utils import add_user_vote, get_results, has_voted


class PollModelTest(UserTestMixin, PollTestMixin):
    def test_create_invalid_max_vote_choices(self):
        poll = self.Create_poll(choices=["Ja", "Nein"])

        with self.assertRaises(ValidationError):
            poll.max_vote_choices = 2
            poll.save()

    def test_create_invalid_min_vote_choices_over_max_vote_choices(self):
        poll = self.Create_poll(choices=["Ja", "Nein", "Vielleicht", "Bla", "Blaaa"])

        with self.assertRaises(ValidationError):
            poll.max_vote_choices = 2
            poll.min_vote_choices = 4
            poll.save()

    def test_qs(self):
        user = self.Login_student()
        poll = self.Create_poll()
        add_user_vote(
            poll=poll,
            choices=[poll.choices[0].id],
            user=user
        )
        self.assertIn(poll, Poll.objects.voted(user))
        self.assertEqual(1, Poll.objects.voted(user).count())
        self.assertNotIn(poll, Poll.objects.not_voted(user))
        self.assertEqual(0, Poll.objects.not_voted(user).count())

    def test_get_results(self):
        get_results(self.Create_poll())


class PollAPITest(UserTestMixin, PollTestMixin):
    def setUp(self):
        self.user = self.Login_student()
        self.__class__.associated_student = self.user
        self.poll = self.Create_poll()

    def vote(self, **kwargs):
        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [self.poll.choices[0].id],
            **kwargs
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertTrue(has_voted(self.poll, self.user))
        self.assertEqual(1, Vote.objects.filter(associated_user=self.user).count())

        return response

    def test_vote(self):
        self.vote()

    def test_vote_two_times_invalid(self):
        self.vote()
        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [self.poll.choices[1].id],
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
        self.assertTrue(has_voted(self.poll, self.user))
        self.assertEqual(1, Vote.objects.filter(associated_user=self.user).count())

    def test_invalid_choices(self):
        other_poll = self.Create_poll(["Ja", "Nein"])

        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [other_poll.choices[0].id],
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)

    def test_get_empty_selections_before_vote(self):
        response = self.client.get(f"/api/student/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(None, response.data["user_vote"])

    def test_get_correct_selections_after_vote(self):
        self.vote()

        response = self.client.get(f"/api/student/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        self.assertEqual(1, len(response.data["user_vote"]["choices"]))
        self.assertEqual([self.poll.choices[0].id], list(response.data["user_vote"]["choices"]))

    def test_with_feedback(self):
        self.vote(feedback="Test")

    @override_settings(SHOW_VOTES_RESULTS=True)
    def test_dont_show_results(self):
        self.poll.show_results_date = datetime.now() + timedelta(days=2)
        self.poll.save()

        response = self.vote()
        self.assertIsNone(response.data["results"])

    @override_settings(SHOW_VOTES_RESULTS=True)
    def test_dont_show_results_before_vote(self):
        response = self.client.get(f"/api/student/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        # Ensure no results visible
        self.assertIsNone(response.data["results"])

    @override_settings(SHOW_VOTES_RESULTS=True)
    def test_show_results_after_vote(self):
        self.vote()
        response = self.client.get(f"/api/student/poll/{self.poll.id}/")
        self.assertStatusOk(response.status_code)
        self.assertIsNotNone(response.data["results"])


class PollAPIChoicesAmountTest(UserTestMixin, PollTestMixin):
    def setUp(self):
        self.user = self.Login_user()
        self.__class__.associated_student = self.user

        choices = ["Ja", "Nein", "Vielleicht", "A", "B"]
        min_vote_choices = 2
        max_vote_choices = 4
        self.poll = self.Create_poll(
            choices=choices,
            min_vote_choices=min_vote_choices,
            max_vote_choices=max_vote_choices,
        )

    def test_too_much(self):
        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [
                self.poll.choices[0].id,
                self.poll.choices[1].id,
                self.poll.choices[2].id,
                self.poll.choices[3].id,
                self.poll.choices[4].id,
            ],
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)

    def test_too_little(self):
        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [
                self.poll.choices[0].id,
            ],
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)

    def test_ok(self):
        response = self.client.post(f"/api/student/poll/{self.poll.id}/vote/", {
            "choices": [
                self.poll.choices[0].id,
                self.poll.choices[1].id,
            ],
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
