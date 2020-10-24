from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from social.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # The view needs to deconflict with the user context
    # that the auth system injects to the context.
    context_object_name = "viewed_user"
    slug_field = "username"
    slug_url_kwarg = "username"
