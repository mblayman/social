from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from social.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
