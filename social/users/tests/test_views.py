from social.test import TestCase
from social.users.tests.factories import UserFactory


class TestUserDetail(TestCase):
    def test_unauthenticated_access(self):
        user = self.make_user()

        self.assertLoginRequired("users:detail", user.username)

    def test_ok_self(self):
        user = self.make_user()

        with self.login(user):
            self.get_check_200("users:detail", user.username)

    def test_ok_other(self):
        """The other user is in the context with a different name."""
        user = self.make_user()
        other_user = UserFactory()

        with self.login(user):
            self.get_check_200("users:detail", other_user.username)

        assert self.get_context("user") == user
        assert self.get_context("viewed_user") == other_user
