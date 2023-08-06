import logging

from django.contrib import auth
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin  # https://stackoverflow.com/questions/42232606/django
                                                      # -exception-middleware-typeerror-object-takes-no-parameters
from django.conf import settings

from ...permissions import is_authenticated
from ...utils import set_session_key
from ... import app_settings

logger = logging.getLogger('django_sso_app.core.middleware')


ADMIN_URL = '/{}'.format(settings.ADMIN_URL)
PROFILE_INCOMPLETE_ENABLED_PATHS = [
    reverse('javascript-catalog'),
    reverse('profile.complete'),
]


class DjangoSsoAppAuthenticationBaseMiddleware(MiddlewareMixin):
    """
    See django.contrib.auth.middleware.RemoteUserMiddleware.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = app_settings.APIGATEWAY_CONSUMER_CUSTOM_ID_HEADER
    anonymous_header = app_settings.APIGATEWAY_ANONYMOUS_CONSUMER_HEADER

    @staticmethod
    def _clear_response_jwt(request):
        set_session_key(request, '__dssoa__clear_response_jwt', True)

    @staticmethod
    def _remove_invalid_user(request):
        """
        Removes the current authenticated user in the request which is invalid.
        """

        if is_authenticated(request.user):
            logger.info('removing invalid user "{}"'.format(request.user))

            auth.logout(request)

    @staticmethod
    def _is_admin_path(request):
        return request.path.startswith(ADMIN_URL)

    @staticmethod
    def _request_path_is_disabled_for_incomplete_users(request):
        request_path = request.path
        return (request_path not in PROFILE_INCOMPLETE_ENABLED_PATHS) and \
                not (request_path.startswith('/static/')) and \
                not (request_path.startswith('/media/')) and \
                not (request_path.startswith('/logout/')) and \
                not (request_path.startswith('/password/reset/')) and \
                not (request_path.startswith('/api/v1/auth/users/') and request.method == 'PATCH') and \
                not (request_path.startswith('/confirm-email/'))

                # not (request_path.startswith('/api/v1/')) and \

    def process_request(self, request):
        raise NotImplementedError('process_request')

    def process_response(self, request, response):
        raise NotImplementedError('process_response')
