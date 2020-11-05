from django.contrib.auth.models import AbstractUser

from social.invites.models import Invite

from . import constants


class User(AbstractUser):
    """A custom user for extension"""

    @property
    def remaining_connections(self):
        """Get the number of remaining available connections."""
        return (
            constants.MAX_USER_CONNECTIONS
            - Invite.objects.filter(from_user=self)
            .exclude(status=Invite.InviteStatus.ACCEPTED)
            .count()
        )
