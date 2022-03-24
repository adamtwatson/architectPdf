from unittest import TestCase

from jwt.exceptions import InvalidSignatureError
from . import src

def x(r): print(r)


class Test(TestCase):

    def setUp(self):
        self.user = {'id': 1, 'username': 'tester', 'email': 'test@user.com', 'first_name': 'Test', 'last_name': 'User'}
        # simulate a logged-in user by setting generating a jwt for the user.
        self.jwt = jwt_auth.generate_jwt(self.user, secret_key='secret')

        # Get the last character and change the case recreate the JWT
        self.tampered_jwt = self.jwt[0:-1] + self.jwt[-1].swapcase()

        # Test authenticate as if someone user a bad secret
        self.bad_secret_jwt = jwt_auth.generate_jwt(self.user, secret_key='bad-secret')

    def test_generate_jwt(self):
        self.assertIsNotNone(self.jwt)

    def test_authenticate_jwt(self):
        self.assertEqual(self.jwt, jwt_auth.authenticate_jwt(self.jwt, 'secret'))

        # logger.debug(authenticate_jwt(tampered_jwt, secret_key='secret'))
        with self.assertRaises(InvalidSignatureError):
            jwt_auth.authenticate_jwt(jwt_token=self.tampered_jwt, secret_key='secret')
            jwt_auth.authenticate_jwt(jwt_token=self.bad_secret_jwt, secret_key='secret')

    def test_jwt_auth(self):
        request = dict()
        logger.debug(jwt_auth.jwt_auth(x(request)))
        with self.assertRaises(exceptions.PermissionDenied):
            jwt_auth.jwt_auth(x(request))
