from django.conf import settings
from django.db import models
from django.utils import timezone


class Invite(models.Model):
    """An invitation from one user to another to establish a connection

    The invite counts against a user's max total connections
    if the invitation ends with no connection between users
    (i.e., rejected or expired).

    This behavior is a linchpin to help reduce abuse and spammy requests.
    """

    class InviteStatus(models.IntegerChoices):
        PENDING = 1
        SENT = 2
        ACCEPTED = 3
        REJECTED = 4
        EXPIRED = 5

    IN_FLIGHT_STATUSES = [InviteStatus.PENDING, InviteStatus.SENT]

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_invites"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_invites",
    )
    status = models.IntegerField(
        choices=InviteStatus.choices, default=InviteStatus.PENDING
    )

    @classmethod
    def bulk_expire(cls, older_than):
        """Expire sent invites that are older than the provided datetime."""
        cls.objects.filter(status=cls.InviteStatus.SENT, sent_at__lt=older_than).update(
            status=cls.InviteStatus.EXPIRED
        )

    def send(self):
        """Send the invite via email.

        Note: This invokes email sending so it should be handled outside
        of the request/response lifecycle.
        """
        # TODO: Send the email.
        self.sent_at = timezone.now()
        self.status = self.InviteStatus.SENT
        self.save()

    def accept(self):
        """Accept an invite.

        The two users are connected.
        """
        # TODO: Create a connection.
        self.status = self.InviteStatus.ACCEPTED
        self.save()

    def reject(self):
        """Reject an invite."""
        self.status = self.InviteStatus.REJECTED
        self.save()
