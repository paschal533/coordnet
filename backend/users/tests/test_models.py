from users.tests import factories
from utils.testcases import BaseAPITransactionTestCase


class TestUserModel(BaseAPITransactionTestCase):
    def test_user_get_absolute_url(self) -> None:
        user = factories.UserFactory()
        self.assertEqual(user.get_absolute_url(), f"/users/{user.pk}/")
