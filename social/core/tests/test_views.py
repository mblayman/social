from social.test import TestCase


class TestIndex(TestCase):
    def test_not_authenticated(self):
        response = self.get("core:index")
        print(response.get("Location"))
        print(response)
        print(dir(response))
        print(response.content)
        print(list(response.items()))
        assert False

    def test_ok(self):
        user = self.make_user()

        with self.login(user):
            self.get_check_200("core:index")
