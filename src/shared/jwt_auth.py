from functools import wraps

import jwt
from shared.exceptions import PermissionDenied
from shared.settings import logger

# logger = settings.logger


def generate_jwt(user, secret_key="secret"):
    user_data = {
        "id": user['id'],
        "username": user['username'],
        "first_name": user['first_name'],
        "last_name": user['last_name'],
    }
    encoded = jwt.encode(user_data, secret_key, algorithm="HS256")
    return encoded


def authenticate_jwt(jwt_token, secret_key="secret"):
    jwt.decode(jwt_token, secret_key, algorithms="HS256")
    # data = await arc.tables()
    # cat = await data.cats.get({catID, pplID})
    return jwt_token


def jwt_auth(func):
    """
    Decorator to make a view check for JWT authorization and add the user to the request.  Usage::

        @jwt_auth()
        def my_view(request):
            # I can assume now that the request will have a request.user associated with it
            # ...
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        logger.debug(request)
        jwt_token = request.headers.get('Authorization')
        logger.debug(jwt_token)
        if not jwt_token:
            logger.debug('jwt not found in headers')
            # We didnt find a JWT in the headers, check the query string
            query_string_jwt = request.GET.get('jwt', None)
            if query_string_jwt:
                # Still no JWT, this user is not allowed to be here.
                raise PermissionDenied('No JWT Found!')
            # If we got this far we must have a JWT from the querystring!
            jwt_token = query_string_jwt

        # This should add the user to the request, or fail
        request.user = authenticate_jwt(jwt_token)

        if not request.user:
            # Authenticate should have done a database query and added a user to the request.
            raise PermissionDenied('No User Found!')

        return func(request, *args, **kwargs)
    return inner
