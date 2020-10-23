from social.test import TestCase


class TestIndex(TestCase):
    def test_not_authenticated(self):
        self.get_check_200("core:index")
