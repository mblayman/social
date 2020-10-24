from social.test import TestCase


class TestUserDetail(TestCase):
    def test_unauthenticated_access(self):
        user = self.make_user()

        self.assertLoginRequired("users:detail", user.username)

    def test_ok(self):
        user = self.make_user()

        with self.login(user):
            self.get_check_200("users:detail", user.username)
