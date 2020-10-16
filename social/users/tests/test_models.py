from social.test import TestCase


class TestUser(TestCase):
    def test_factory(self):
        user = self.make_user()

        assert user.username is not None
