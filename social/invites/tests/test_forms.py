from unittest import mock

from social.invites.forms import SendInviteForm
from social.invites.models import Invite
from social.invites.tests.factories import InviteFactory
from social.test import TestCase
from social.users.tests.factories import UserFactory


class TestSendInviteForm(TestCase):
    def test_valid(self):
        """Two users with no existing invites between them are valid."""
        from_user = UserFactory()
        to_user = UserFactory()
        data = {"from_user": str(from_user.id), "to_user": str(to_user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert is_valid

    def test_invite_exists(self):
        """An existing invite is an error."""
        invite = InviteFactory()
        data = {
            "from_user": str(invite.from_user.id),
            "to_user": str(invite.to_user.id),
        }
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert "You have already sent an invitation." in form.non_field_errors()

    def test_no_self_invite(self):
        """A user may not invite themself."""
        user = self.make_user()
        data = {"from_user": str(user.id), "to_user": str(user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert (
            "You may not invite yourself. You're already here!"
            in form.non_field_errors()
        )

    @mock.patch("social.invites.forms.constants")
    def test_in_flight_invites(self, mock_constants):
        """The user can't submit more than the max in flight."""
        mock_constants.MAX_IN_FLIGHT_INVITES = 1
        from_user = self.make_user()
        to_user = UserFactory()
        InviteFactory(from_user=from_user)
        data = {"from_user": str(from_user.id), "to_user": str(to_user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert (
            "You have too many sent invitations out currently."
            in form.non_field_errors()
        )

    def test_invalid_from_user(self):
        """An invalid from_user is an error."""
        user = self.make_user()
        data = {"from_user": "0", "to_user": str(user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert "The user is invalid." in form.non_field_errors()

    def test_invalid_to_user(self):
        """An invalid to_user is an error."""
        user = self.make_user()
        data = {"from_user": str(user.id), "to_user": "0"}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert "The user is invalid." in form.non_field_errors()

    def test_valid_save(self):
        """A valid form creates an invite."""
        from_user = UserFactory()
        to_user = UserFactory()
        data = {"from_user": str(from_user.id), "to_user": str(to_user.id)}
        form = SendInviteForm(data=data)
        form.is_valid()

        form.save()

        assert (
            Invite.objects.filter(
                from_user=from_user, to_user=to_user, status=Invite.InviteStatus.PENDING
            ).count()
            == 1
        )

    @mock.patch("social.invites.forms.users_constants")
    def test_max_connections(self, mock_users_constants):
        """A user may not send any invites when they are at their max connections."""
        mock_users_constants.MAX_USER_CONNECTIONS = 1
        from_user = UserFactory()
        to_user = UserFactory()
        InviteFactory(from_user=from_user)
        data = {"from_user": str(from_user.id), "to_user": str(to_user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert (
            "You are at your maximum number of connections." in form.non_field_errors()
        )

    @mock.patch("social.invites.forms.users_constants")
    def test_max_connections_accepted_invite(self, mock_users_constants):
        """An accepted invite does not count against the max connections total."""
        mock_users_constants.MAX_USER_CONNECTIONS = 1
        from_user = UserFactory()
        to_user = UserFactory()
        InviteFactory(from_user=from_user, status=Invite.InviteStatus.ACCEPTED)
        data = {"from_user": str(from_user.id), "to_user": str(to_user.id)}
        form = SendInviteForm(data=data)

        is_valid = form.is_valid()

        assert is_valid
