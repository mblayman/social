from django.contrib.messages import get_messages

from social.invites.models import Invite
from social.test import TestCase
from social.users.tests.factories import UserFactory


class TestSendInvite(TestCase):
    def test_unauthenticated_access(self):
        user = self.make_user()

        self.assertLoginRequired("invites:send_invite", user.username)

    def test_get_ok(self):
        user = self.make_user()
        to_user = UserFactory()

        with self.login(user):
            self.get_check_200("invites:send_invite", to_user.username)

        form = self.get_context("form")
        assert form.is_valid()
        assert self.get_context("to_user") == to_user

    def test_invalid_to_user(self):
        """An invalid to_user is a 404."""
        user = self.make_user()

        with self.login(user):
            response = self.get("invites:send_invite", "nothere")

        assert response.status_code == 404

    def test_post_ok(self):
        """A successful post creates an invite."""
        user = self.make_user()
        to_user = UserFactory()
        data = {"from_user": str(user.id), "to_user": str(to_user.id)}

        with self.login(user):
            response = self.post("invites:send_invite", to_user.username, data=data)

        assert Invite.objects.count() == 1
        assert response.status_code == 302
        assert response["Location"] == self.reverse("core:index")
        message = list(get_messages(response.wsgi_request))[0]
        assert str(message) == f"Invite sent to {to_user.username}."
