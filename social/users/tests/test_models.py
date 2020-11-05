from social.invites.models import Invite
from social.invites.tests.factories import InviteFactory
from social.test import TestCase


class TestUser(TestCase):
    def test_factory(self):
        user = self.make_user()

        assert user.username is not None

    def test_remaining_connections(self):
        """A user has a count of its remaining available connections."""
        # TODO: Include real connections when available.
        user = self.make_user()
        InviteFactory(from_user=user)
        InviteFactory(from_user=user, status=Invite.InviteStatus.ACCEPTED)

        assert user.remaining_connections == 499
