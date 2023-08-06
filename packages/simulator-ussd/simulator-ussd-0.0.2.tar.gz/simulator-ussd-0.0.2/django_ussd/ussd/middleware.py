from django.utils.cache import patch_vary_headers
from django.utils import translation
from .core import SessionStore
from structlog import get_logger

class AirtelTzLocaleMiddleware(object):
    """
    This Middleware saves the desired content language in the user session.
    The SessionMiddleware has to be activated.
    """
    def process_request(self, request):
        logger = get_logger(__name__).bind(get_params=request.GET)
        if 'SESSIONID' not in request.GET:
            return

        session = SessionStore(session_key=request.GET['SESSIONID'])
        if 'language' in session:
            language = session['language']
            logger.debug('language_found', source='session', 
                         language=language)
        elif request.method == 'GET' and 'LANGUAGE' in request.GET:
            language = request.GET['LANGUAGE']
            session['language'] = language
            session.save()
            logger.debug('language_found', source='request', 
                         language=language)
        else:
            logger.debug('language_not_found')
            return

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response