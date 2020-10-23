from social.test import TestCase


class TestIndex(TestCase):
    def test_not_authenticated(self):
        self.get_check_200("core:index")

    def test_ok(self):
        user = self.make_user()

        with self.login(user):
            self.get_check_200("core:index")
