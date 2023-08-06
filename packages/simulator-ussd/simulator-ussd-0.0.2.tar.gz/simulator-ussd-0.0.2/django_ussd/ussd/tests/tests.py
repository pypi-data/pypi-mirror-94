from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from django.utils.translation import ugettext_lazy as _
from copy import copy

import mock
import datetime
from django_ussd.ussd.core import UssdRequest, UssdResponse, UssdAppView, _handlers
from django_ussd.ussd.handlers import Handler, Input, ValidationError, MissingAttribute, HandlerMeta, \
    Menu, MenuOption, List, ListItem, Quit



import re

# Demonstration handlers for testing purposes
class enter_name(Handler):
    def handle(self, req):
        if not req.input:
            req.session['steps'].append({'start': datetime.datetime.now(), })
            return UssdResponse('Enter name:')
        else:
            req.session['name'] = req.input
            req.session['steps'][-1].update(
                dict(
                    end=datetime.datetime.now(),
                    selection=req.input
                )
            )
            return req.forward('enter_email')


class enter_email(enter_name):
    def handle(self, req):
        return UssdResponse('Enter email:')


class HandlerMetaTest(TestCase):
    def test_init(self):
        """Tests handler metaclass actions"""

        # An instance of each new handler class is automatically
        # registered.
        assert(isinstance(_handlers['enter_name'], enter_name))
        assert(isinstance(_handlers['enter_email'], enter_email))

        attrs = {'foo': None, 'bar': None}

        # If there are no required attributes, the class is created
        # normally.
        try:
            HandlerMeta('handler_1', (Input, Handler, object), attrs)
        except MissingAttribute:
            self.fail()

        # If any required attributes are missing, an excecption is raised.
        attrs['__required_attrs__'] = ('bar', 'baz',)
        with self.assertRaisesRegex(MissingAttribute, 'baz'):
            HandlerMeta('handler_2', (Input, Handler, object), attrs)


class RequestTest(TestCase):
    def setUp(self):
        self.ussd_req = UssdRequest(phone_number='12345', session_id='314159',
                                input_='foo',
                                session=SessionStore(session_key='abc'),
                                language='en')

    def test_ussd_request_initialization(self):
        """Tests that USSD request is properly initialized"""
        self.assertEqual(('12345', '314159', 'foo'),
                         (self.ussd_req.phone_number,
                          self.ussd_req.session_id,
                          self.ussd_req.input))
        self.assertEqual(self.ussd_req.session.session_key, 'abc')

    def test_forward(self):
        """
        Tests that request forwarding returns a new request with input
        cleared
        """
        new_request, handler_name = self.ussd_req.forward('enter_age')
        self.assertEqual(handler_name, 'enter_age')
        self.assertEqual(new_request.input, '')
        self.assertIsNot(new_request, self.ussd_req)


class ResponseTest(TestCase):
    def setUp(self):
        self.session = SessionStore(session_key='foo bar')

    def test_ussd_response_serialization(self):
        """Tests that USSD response is properly serialized"""
        res = UssdResponse('message', 1, True, self.session)
        self.assertEqual(str(res), 'message')

class enter_color(Input):
    def get_prompt(self, req):
        return 'Enter color:'

    session_key = 'color'
    next_handler = 'quit'

    def validate(self, input):
        if len(input) < 3:
            raise ValidationError("Please enter a valid color:")


class quit(Handler):
    def handle(self, req):
        return UssdResponse('Goodbye!', status=STOP)


class InputHandlerTest(TestCase):
    def setUp(self):
        self.session = SessionStore()
        self.session['_ussd_state'] = {'next_handler': 'enter_color'}
        self.session['steps'] = []
        self.request = UssdRequest('12345', '3141459', '', self.session, language='en')
        self.handler = enter_color()

    def test_validate(self):
        with self.assertRaises(ValidationError):
            self.handler.validate('x')

    def test_handle_empty_input(self):
        """
        Tests the first call to an input handler. Ensures that the
        prompt is returned in the response, and that the input handler
        is registered to handle the next request.
        """
        response = self.handler.handle(self.request)
        self.assertEqual(response.text, 'Enter color:')
        self.assertEqual(response.status, True)
        self.assertEqual(self.session['_ussd_state']['next_handler'],
                         'enter_color')

    def test_handle_invalid_input(self):
        """
        Tests a call to an input handler with invalid input. Ensures
        that the appropriate error message is shown, and that invalid
        input is not stored.
        """
        self.handler.handle(self.request)
        self.request.input = 'x'
        response = self.handler.handle(self.request)
        self.assertIn('Please enter a valid color:', response.text)
        assert 'color' not in self.session
        self.assertEqual(self.request.session['_ussd_state']['next_handler'],
                         'enter_color')

    def test_handle_valid_input(self):
        """
        Tests the second call to an input handler. Ensures that
        control is forwarded to the next handler, and that user input
        is persisted to session storage.
        """
        self.handler.handle(self.request)
        self.request.input = 'dark green'
        new_request, next_handler = self.handler.handle(self.request)
        self.assertEqual(next_handler, 'quit')
        self.assertEqual(new_request.session['color'], 'dark green')

    def test_recording_of_interaction(self):
        """
        Tests if interaction with this handler is recorded in the session
        """
        self.handler.handle(self.request)

        # assert interaction entry has been added to session on first interaction
        self.assertTrue(len(self.session['steps']))
        self.assertEqual(self.session['steps'][-1]['name'], self.handler.__class__.__name__)
        self.assertIn(self.handler.get_prompt(self.request), self.session['steps'][-1]['screen_text'])
        self.assertTrue('start' in self.session['steps'][-1])
        self.assertFalse('end' in self.session['steps'][-1])

        # assert extra interaction entries have been added to session on second interaction
        self.request.input = 'dark green'
        self.handler.handle(self.request)
        self.assertTrue('end' in self.session['steps'][-1])
        self.assertEqual(self.session['steps'][-1]['selection'], self.request.input)


class select_activity(Menu):
    prompt = _('Welcome to the stock exchange.\n')
    error_prompt = _('Please enter a valid choice\n')
    options = (MenuOption(_('Buy shares'), 'buy_shares'),
               MenuOption(_('Sell shares'), 'sell_shares'),
               MenuOption(_('Look up a share price'), 'lookup_price'),
               MenuOption(_('Back'), 'back', '*'),
               MenuOption(_('BackTesting'), 'backTest', 'a ', 'a')
    )


class MenuTest(TestCase):
    def setUp(self):
        self.session = SessionStore()
        self.session['_ussd_state'] = {'next_handler': 'select_activity'}
        self.session['steps'] = []
        self.request = UssdRequest('12345', '3141459', '', self.session, language='en')
        self.handler = select_activity()

    def test_handle_empty_input(self):
        """
        Tests the first call to a menu.
        """
        # First the prompt is shown, along with the menu options
        response = self.handler.handle(self.request)
        for string in ('Welcome', '1. Buy', '2. Sell', '3. Look up', re.escape('* Back'), re.escape('a  BackTesting')):
            self.assertRegex(response.text, string)

        # The next call is handled by the same menu
        self.assertEqual(response.status, True)
        self.assertEqual(self.session['_ussd_state']['next_handler'],
                         'select_activity')

    def test_handle_valid_input(self):
        """
        Tests a valid choice from a menu.
        """
        self.handler.handle(self.request)
        self.request.input = '2'
        new_request, next_handler = self.handler.handle(self.request)

        # Control is forwarded to the corresponding handler
        self.assertEqual(next_handler, 'sell_shares')

    def test_handle_invalid_input(self):
        """
        Tests an invalid choice from a menu.
        """
        self.request.input = 'wrong'
        response = self.handler.handle(self.request)

        # Menu options are repeated, along with an error message
        for string in ('Please enter a valid choice', '1. Buy',
                       '2. Sell', '3. Look up'):
            self.assertRegex(response.text, string)

        # Control returns to the menu handler
        self.assertEqual(self.request.session['_ussd_state']['next_handler'],
                         'select_activity')

    def test_handle_takes_given_input_of_menu_options(self):
        """
        Test that input_text parameter given by MenuOption
        is working
        """
        self.handler.handle(self.request)

        self.request.input = '*'
        new_request, next_handler = self.handler.handle(self.request)

        # Control is forwarded to the corresponding handler
        self.assertEqual(next_handler, 'back')

    def test_handle_takes_given_input_of_menu_option_with_input_value(self):
        """
        Test that input_value parameter given by MenuOption is working
        """
        self.handler.handle(self.request)

        self.request.input = 'a'

        new_request, next_handler = self.handler.handle(self.request)

        # Control is forwarded to the corresponding handler
        self.assertEqual(next_handler, 'backTest')

    def test_recording_of_interaction(self):
        """
        Tests if interaction with this handler is recorded in the session
        """
        self.handler.handle(self.request)

        # assert interaction entry has been added to session on first interaction
        self.assertTrue(len(self.session['steps']))
        self.assertEqual(self.session['steps'][-1]['name'], self.handler.__class__.__name__)
        self.assertIn(str(self.handler.prompt), self.session['steps'][-1]['screen_text'])
        self.assertTrue('start' in self.session['steps'][-1])
        self.assertFalse('end' in self.session['steps'][-1])

        # assert extra interaction entries have been added to session on second interaction
        self.request.input = '2'
        self.handler.handle(self.request)
        self.assertTrue('end' in self.session['steps'][-1])
        self.assertEqual(self.session['steps'][-1]['selection'], self.request.input)


class select_language(List):
    session_key = 'language_id'
    prompt = _('Choose a language\n')
    items_per_page = 2
    next_handler = 'select_framework'
    items = (ListItem(_('Python'), 10),
             ListItem(_('Ruby'), 11),
             ListItem(_('Java'), 12),
             ListItem(_('Haskell'), 13))
    options = (MenuOption(_('Languages'), 'select_language'),
               MenuOption(_('Home'), 'enter_name'),
               MenuOption(_('Back'), 'back', '*'),
    )


class select_framework(List):
    session_key = 'framework_id'
    prompt = _('Choose a framework')
    items_per_page = 2
    next_handler = 'enter_rating'

    def get_items(self, req):
        return (ListItem(_('Flask'), 21),
                ListItem(_('Django'), 22),
                ListItem(_('CherryPy'), 23))


class select_silver_bullet(List):
    items = []
    prompt = _('Choose a silver bullet')
    empty_prompt = _('No such thing')
    items_per_page = 5
    session_id = 'silver_bullet_id'


class ListHandlerTest(TestCase):
    def setUp(self):
        self.session = SessionStore()
        self.session['_ussd_state'] = {'next_handler': 'select_language'}
        self.session['steps'] = []
        self.request = UssdRequest('12345', '3141459', '', self.session, language='en')
        self.handler = select_language()

    def test_handle_empty_list(self):
        handler = select_silver_bullet()

        # View empty list
        response = handler.handle(self.request)

        # 'Empty prompt' is shown
        self.assertIn('No such thing', response.text)

        # Populate list
        handler.items = (ListItem('Sufficiently smart compiler', 1),
                         ListItem('Supernatural programmer', 2))

        # View populated list
        response = handler.handle(self.request)

        # Normal prompt is shown
        self.assertIn('Choose a silver bullet', response.text)

    def test_handle_first_page(self):
        """
        Tests actions on the first page of a List handler.
        """

        # We see a prompt, along with the first page of items and
        # an option to view more
        response = self.handler.handle(self.request)
        for string in ('Choose', '1. Python', '2. Ruby', '3. More',
                       '4. Languages', '5. Home', re.escape('* Back')):
            self.assertRegex(response.text, string)

        # Only the first page of items is shown
        self.assertNotRegex(response.text, r'(Java|Haskell)')
        # The current page number is stored in session
        self.assertEqual(self.session['_ussd_state']['page'], 1)

        # We make an out-of-range request
        self.request.input = '99'
        response = self.handler.handle(self.request)

        # Choices are repeated with an error notice
        for string in ('valid', '1. Python', '2. Ruby', '3. More',

                       '4. Languages', '5. Home', re.escape('* Back')):
            self.assertRegex(response.text, string)

        # We make a non-numeric  request
        self.request.input = 'wrong'
        response = self.handler.handle(self.request)

        # Choices are repeated with an error notice
        for string in ('valid', '1. Python', '2. Ruby', '3. More',
                       '4. Languages', '5. Home', re.escape('* Back')):
            self.assertRegex(response.text, string)

        # We request an item on this page
        self.request.input = '2'
        new_request, next_handler = self.handler.handle(self.request)

        # The value of our chosen language is stored in session
        self.assertEqual(self.session['language_id'], 11)

        # The next handler is correctly set
        self.assertEqual(next_handler, 'select_framework')

        del self.session['language_id']

        # We request a menu option
        self.request.input = '5'
        new_request, next_handler = self.handler.handle(self.request)

        # The next handler is correctly set
        self.assertEqual(next_handler, 'enter_name')

        # we request a menu option which has a custom input_text
        self.request.input = '*'
        new_request, next_handler = self.handler.handle(self.request)

        self.assertEqual(next_handler, 'back')

        # No item is stored in session
        with self.assertRaises(KeyError):
            self.session['language_id']

        # Clear session state for next test
        del self.session['_ussd_state']['page']

    def test_handle_second_page(self):
        """
        Tests navigating to the second page of a List.
        """
        # We request the first page
        self.handler.handle(self.request)

        # We request the second page
        self.session['_ussd_state']['page'] = 1
        self.request.input = '3'
        response = self.handler.handle(self.request)

        # The page number is stored in session
        self.assertEqual(self.session['_ussd_state']['page'], 2)

        # The second page is displayed
        for string in ('Choose', '3. Java', '4. Haskell',
                       '5. Languages', '6. Home'):
            self.assertRegex(response.text, string)

        # There are no more items, so 'More' is not displayed
        self.assertNotRegex(response.text, 'More')

        # Items from the first page are not displayed
        self.assertNotRegex(response.text, r'(Python|Ruby)')

        # We request an item on this page
        self.request.input = '3'
        new_request, new_handler = self.handler.handle(self.request)

        # The value of our item is stored in session
        self.assertEqual(self.session['language_id'], 12)

        # Next handler is correctly set
        self.assertEqual(new_handler, 'select_framework')

        # Clear session state for next test
        del self.session['language_id']
        del self.session['_ussd_state']['page']

    def test_get_items(self):
        handler = select_framework()
        self.session['_ussd_state']['next_handler'] = 'select_framework'

        # We request the first page
        self.request.input = ''

        # First page is shown
        response = handler.handle(self.request)
        for s in ('Choose a framework', '1. Flask', '2. Django', '3. More'):
            self.assertRegex(response.text, s)

    def test_recording_of_interaction(self):
        """
        Tests if interaction with this handler is recorded in the session
        """
        self.handler.handle(self.request)

        # assert interaction entry has been added to session on first interaction
        self.assertTrue(len(self.session['steps']))
        self.assertEqual(self.session['steps'][-1]['name'], self.handler.__class__.__name__)
        self.assertIn(str(self.handler.prompt), self.session['steps'][-1]['screen_text'])
        self.assertTrue('start' in self.session['steps'][-1])
        self.assertFalse('end' in self.session['steps'][-1])

        # assert extra interaction entries have been added to session on second interaction
        self.request.input = '2'
        self.handler.handle(self.request)
        self.assertTrue('end' in self.session['steps'][-1])
        self.assertEqual(self.session['steps'][-1]['selection'], self.request.input)


class quit(Quit):
    message = "Goodbye!"


class QuitHandlerTest(TestCase):
    def setUp(self):
        self.session = SessionStore()
        self.session['_ussd_state'] = {}
        self.session['steps'] = []
        self.handler = quit()

    def test_handle(self):
        response = self.handler.handle(UssdRequest('12345', '314159', '', self.session, language='en'))

        # Goodbye message is shown
        self.assertRegex(response.text, 'Goodbye')

        # Gateway is signalled to end session
        self.assertEqual(response.status, False)

    def test_recording_of_interaction(self):
        """
        Tests if interaction with this handler is recorded in the session
        """
        self.handler.handle(UssdRequest('12345', '314159', '', self.session, language='en'))

        # assert interaction entry has been added to session on first interaction
        self.assertTrue(len(self.session['steps']))
        self.assertEqual(self.session['steps'][-1]['name'], self.handler.__class__.__name__)
        self.assertIn(self.handler.message, self.session['steps'][-1]['screen_text'])
        self.assertTrue('start' in self.session['steps'][-1])
        self.assertTrue('end' in self.session['steps'][-1])
        self.assertEqual(self.session['steps'][-1]['selection'], "")

class UssdController(UssdAppView):
    initial_handler = "enter_name"

    def post(self, req):
        return UssdRequest(req.POST['phoneNumber'],
                           req.POST['sessionId'],
                           req.POST['text'],)


class DispatchTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request_params = {'phoneNumber': '12345',
                               'sessionId': '314159',
                               'text': '',
                               'LANGUAGE': 'en'}

        self.url_template = '/ussd/'
        self.http_request = self._post(self.request_params)

    def _post(self, params):
        return self.factory.post(self.url_template, params)

    def test_ignore_initial_input(self):
        """
        Tests handling of a request with initial level and input.
        """

        # We make a request with level 1 and input 15
        params = copy(self.request_params)
        params['text'] = 15
        request = self._post(params)
        response = UssdController.as_view()(request)

        # Input should be ignored
        self.assertContains(response, 'Enter name')

    def test_dispatch(self):
        """
        Tests that USSD request is dispatched correctly, and that
        USSD application state is persisted to session storage.
        """
        request_1 = self.http_request
        response_1 = UssdController.as_view()(request_1)
        self.assertEqual(response_1.content.decode(), 'Enter name:')
        s = SessionStore(session_key=self.request_params.get('sessionId'))
        self.assertEqual(s['_ussd_state'], {'next_handler': 'enter_name'})
        self.assertTrue('steps' in s, 'session does not contain key named %s' % 'steps')
        self.request_params.update({'text': 'mike'})
        request_2 = self._post(self.request_params)
        response_2 = UssdController.as_view()(request_2)
        self.assertEqual(response_2.content.decode(), 'Enter email:')
        s2 = SessionStore(session_key=self.request_params.get('sessionId'))
        self.assertEqual(s2['_ussd_state'],
                              {'next_handler': 'enter_email'})
        self.assertEqual(s2['name'], 'mike')

        # confirm usage statistics are accurate
        # correct handler name in session record
        self.assertTrue(s2.get('steps', False))
        self.assertTrue(len(s2['steps']))

        # assert accurate timing logic
        start = s2['steps'][-1]['start']
        stop = s2['steps'][-1]['end']
        self.assertGreater(stop, start)
