from .core import UssdAppView, UssdRequest


class Client(object):
    """
    Mock USSD client, used for integration tests.
    """

    def __init__(self, phone_number, handler, session_id=1, language='en'):
        """
        Creates a simulated session with the USSD application.
        """
        self.phone_number = phone_number
        self.session_id = session_id
        self.session = dict()
        self.language = language
        self.session = {'_ussd_state': {'next_handler': handler}, 'steps': [], 'language': 'en'}

    def send(self, user_input, level=2):
        """
        Simulates sending input to the USSD application. Returns a
        ussd Response object.
        """
        request = UssdRequest(self.phone_number, self.session_id,
                              user_input, self.session, language=self.language)

        return UssdAppView().run_handlers(request)
