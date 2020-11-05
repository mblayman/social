from django import forms

from social.users.models import User

from . import constants
from .models import Invite


class SendInviteForm(forms.Form):
    """Set a pending a invite if valid."""

    from_user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=True, widget=forms.HiddenInput()
    )
    to_user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=True, widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        from_user = cleaned_data.get("from_user")
        to_user = cleaned_data.get("to_user")

        self._check_user(from_user)
        self._check_user(to_user)
        self._check_max_connections(from_user)
        self._check_existing_invite(from_user, to_user)
        self._check_self_invite(from_user, to_user)
        self._check_in_flight_invites(from_user)

    def _check_user(self, user):
        if user is None:
            raise forms.ValidationError("The user is invalid.")

    def _check_max_connections(self, from_user):
        if from_user.remaining_connections <= 0:
            raise forms.ValidationError(
                "You are at your maximum number of connections."
            )

    def _check_existing_invite(self, from_user, to_user):
        if Invite.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise forms.ValidationError("You have already sent an invitation.")

    def _check_self_invite(self, from_user, to_user):
        if from_user == to_user:
            raise forms.ValidationError(
                "You may not invite yourself. You're already here!"
            )

    def _check_in_flight_invites(self, from_user):
        if (
            Invite.objects.filter(
                from_user=from_user, status__in=Invite.IN_FLIGHT_STATUSES
            ).count()
            >= constants.MAX_IN_FLIGHT_INVITES
        ):
            raise forms.ValidationError(
                "You have too many sent invitations out currently."
            )

    def save(self):
        """Create a pending invite."""
        Invite.objects.create(
            from_user=self.cleaned_data["from_user"],
            to_user=self.cleaned_data["to_user"],
        )
