import datetime

from django.utils import timezone

from social.invites.models import Invite
from social.invites.tests.factories import InviteFactory
from social.test import TestCase


class TestInvite(TestCase):
    def test_factory(self):
        invite = InviteFactory()

        assert invite.created_at is not None
        assert invite.sent_at is None
        assert invite.from_user is not None
        assert invite.to_user is not None
        assert invite.status == Invite.InviteStatus.PENDING

    def test_bulk_expire(self):
        """Old invites are expired."""
        now = timezone.now()
        the_past = now - datetime.timedelta(days=1)
        invite = InviteFactory(status=Invite.InviteStatus.SENT, sent_at=the_past)
        accepted_invite = InviteFactory(
            status=Invite.InviteStatus.ACCEPTED, sent_at=the_past
        )

        Invite.bulk_expire(now)

        invite.refresh_from_db()
        assert invite.status == Invite.InviteStatus.EXPIRED
        accepted_invite.refresh_from_db()
        assert accepted_invite.status == Invite.InviteStatus.ACCEPTED

    def test_send(self):
        """A sent invite sends email, records the timestamp, and sets the status."""
        invite = InviteFactory()

        invite.send()

        # TODO: Assert that email is sent.
        assert invite.sent_at is not None
        assert invite.status == Invite.InviteStatus.SENT

    def test_accept(self):
        """An invite can be accepted."""
        invite = InviteFactory()

        invite.accept()

        assert invite.status == Invite.InviteStatus.ACCEPTED

    def test_reject(self):
        """An invite can be rejected."""
        invite = InviteFactory()

        invite.reject()

        assert invite.status == Invite.InviteStatus.REJECTED
