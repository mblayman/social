import factory

from social.users.tests.factories import UserFactory


class InviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "invites.Invite"

    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
