"""
This modules tests you can have custom ussd view in ussd model view
"""
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.test import LiveServerTestCase, Client
from ..models import *
from ..handlers import Input, Handler, UssdResponse
from ..core import UssdRequest


class EnterPin(Input):

    def handle(self, req):
        self.prompt = "Enter your age\n"
        self.next_handler = req.session['_ussd_state']['next_model_handler']
        self.session_key = 'age'

        return super().handle(req)


class EnterAge2(Input):

    def handle(self, req):
        self.prompt = "Enter your age\n"
        self.next_handler = "EnterName"
        self.session_key = 'age'

        return super(EnterAge2, self).handle(req)


class EnterName(Input):

    def handle(self, req):
        self.prompt = "Enter your name\n"
        self.next_handler = req.session['_ussd_state']['next_model_handler']
        self.session_key = "name"
        return super().handle(req)


class PinValidation(Handler):

    def handle(self, req):
        self.next_handler = req.session['_ussd_state']['next_model_handler']

        # get pin
        pin = req.session.get('pin')

        validate = RegexValidator(regex=r'^[0-9]{1,4}$', message='Not a valid PIN. Please enter your Airtel Money PIN')

        try:
            validate(pin)
        except ValidationError as e:
            return UssdResponse(e.messages.pop())

        return req.forward(self.next_handler)


class TestModelMenuOptionDirectingToCustomeHandler(LiveServerTestCase):

    def setUp(self):
                # Menu screen
        welcome_screen = UssdHandler.objects.create(
            name="Welcome_screen",
        )
        welcome_screen.text.add(
            Translation.objects.create(
                language='en',
                text="Welcome to lenders:\n",
            )
        )

        show_age = UssdHandler.objects.create(
            name="ShowAge",
            session_state=False
        )
        show_age.text.add(
            Translation.objects.create(
                language='en',
                text="Your age is {{age}}\n",
            )
        )

        MenuOptions.objects.create(
            plugin=PluginHandler.objects.create(
                plugin="EnterPin",
                next_handler=show_age
            ),
            ussd_handler=welcome_screen,
            index=1,
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Enter your age",
            )
        )

        # ussd view url
        self.url = "http://localhost:8081{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="1234",
            input=''
        )
        self.client = Client()

    def test(self):

        # send ussd request
        response = self.client.get(self.url, self.params)

        expected_welcome_screen = "Welcome to lenders:\n1. Enter your age\n"

        self.assertEqual(response.content.decode(), expected_welcome_screen)
        self.assertEqual(response['Freeflow'], 'FC')

        # selects option 1 ( to enter age)
        self.params['input'] = 1

        response = self.client.get(self.url, self.params)

        expected_response = "Enter your age\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FC')

        # enter your age
        self.params['input'] = 22

        response = self.client.get(self.url, self.params)

        self.assertEqual(response.content.decode(), "Your age is 22\n")
        self.assertEqual(response['Freeflow'], 'FB')


class TestTwoCustomInputHandlerInModelUssdView(LiveServerTestCase):
    def setUp(self):
        welcome_screen = UssdHandler.objects.create(
            name="Welcome_screen",
        )
        welcome_screen.text.add(
            Translation.objects.create(
                language='en',
                text="Welcome to lenders:\n",
            )
        )

        show_age_name = UssdHandler.objects.create(
            name="ShowAgeName",
            session_state=False
        )
        show_age_name.text.add(
            Translation.objects.create(
                language='en',
                text="Your age is {{age}} and your name is {{name}}\n",
            )
        )


        MenuOptions.objects.create(
            plugin=PluginHandler.objects.create(
                plugin="EnterAge2",
                next_handler= show_age_name
            ),
            ussd_handler = welcome_screen,
            index=1,
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Enter your age",
            )
        )

        # ussd view url
        self.url = "http://localhost:8081{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="12345",
            input=''
        )
        self.client = Client()

    def test(self):

        # send ussd request
        response = self.client.get(self.url, self.params)

        expected_welcome_screen = "Welcome to lenders:\n1. Enter your age\n"

        self.assertEqual(response.content.decode(), expected_welcome_screen)
        self.assertEqual(response['Freeflow'], 'FC')

        # selects option 1 ( to enter age)
        self.params['input'] = 1

        response = self.client.get(self.url, self.params)

        expected_response = "Enter your age\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FC')

        # enter your age
        self.params['input'] = 22


        response = self.client.get(self.url, self.params)

        self.assertEqual(response.content.decode(), "Enter your name\n")
        self.assertEqual(response['Freeflow'], 'FC')

        # enter your name
        self.params['input'] = "mwaside"

        response = self.client.get(self.url, self.params)

        expected_response = "Your age is 22 and your name is mwaside\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FB')


class TestModelInputHandlerDirectingToCustomeHandler(LiveServerTestCase):

    def setUp(self):
        welcome_screen = UssdHandler.objects.create(
            name="Welcome_screen",
        )
        welcome_screen.text.add(
            Translation.objects.create(
                language='en',
                text="Welcome to lenders:\n",
            )
        )

        show_age_name = UssdHandler.objects.create(
            name="ShowAgeName",
            session_state=False,
        )
        show_age_name.text.add(
            Translation.objects.create(
                language='en',
                text="Your age is {{age}} and your name is {{name}}\n",
            )
        )

        enter_age = UssdHandler.objects.create(
            name="enter_age",
            plugin=PluginHandler.objects.create(
                plugin="EnterName",
                next_handler=show_age_name
            ),
            session_key='age'
        )
        enter_age.text.add(
            Translation.objects.create(
                language='en',
                text="Enter your age\n",
            )
        )

        MenuOptions.objects.create(
            next_handler=enter_age,
            ussd_handler=welcome_screen,
            index=1,
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Enter your age",
            )
        )

        # ussd view url
        self.url = "http://localhost:8081{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="1234589",
            input=''
        )
        self.client = Client()

    def test(self):

        # send ussd request
        response = self.client.get(self.url, self.params)

        expected_welcome_screen = "Welcome to lenders:\n1. Enter your age\n"

        self.assertEqual(response.content.decode(), expected_welcome_screen)
        self.assertEqual(response['Freeflow'], 'FC')

        # selects option 1 ( to enter age)
        self.params['input'] = 1

        response = self.client.get(self.url, self.params)

        expected_response = "Enter your age\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FC')

        # enter your age
        self.params['input'] = 22


        response = self.client.get(self.url, self.params)

        self.assertEqual(response.content.decode(), "Enter your name\n")
        self.assertEqual(response['Freeflow'], 'FC')

        # enter your name
        self.params['input'] = "mwaside"

        response = self.client.get(self.url, self.params)

        expected_response = "Your age is 22 and your name is mwaside\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FB')


class TestUssdHandlerWithPluginSet(LiveServerTestCase):

    def setUp(self):
        your_pin = UssdHandler.objects.create(
            name="show your pin",
            session_state=False
        )
        your_pin.text.add(
            Translation.objects.create(
                language='en',
                text="Your pin is {{pin}}",
            )
        )

        pin_plugin = PluginHandler.objects.create(
                plugin="PinValidation",
                next_handler=your_pin
            )
        pin_validation = UssdHandler.objects.create(
            name="pin_validation",
        )
        pin_validation.plugin = pin_plugin
        pin_validation.save()

        UssdHandler.objects.create(
            name="Welcome_screen",
            session_key='pin',
            next_handler=pin_validation
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Enter pin\n",
            )
        )

         # ussd view url
        self.url = "http://localhost:8081{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="12345",
            input=''
        )
        self.client = Client()

    def test_plugin_is_called(self):

        # send ussd request
        response = self.client.get(self.url, self.params)

        expected_input_screen = "Enter pin\n"

        self.assertEqual(response.content.decode(),
                         expected_input_screen
                         )
        self.assertEqual(response['Freeflow'], 'FC')

        self.params['input'] = '1234'

        response = self.client.get(self.url, self.params)

        expected_response = "Your pin is 1234"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'], 'FB')

    def test_pin_was_validated(self):
        self.params['sessionId'] = '4567'
        # send ussd request
        ussd_response = self.client.get(self.url, self.params)

        self.assertEqual(ussd_response.content.decode(),
                         "Enter pin\n"
                         )
        self.assertEqual(ussd_response['Freeflow'], 'FC')

        self.params['input'] = 'abc13434'

        ussd_response = self.client.get(self.url, self.params)

        self.assertEqual(ussd_response.content.decode(),
                         'Not a valid PIN. Please enter your Airtel Money PIN'
                         )
        self.assertEqual(ussd_response['Freeflow'], 'FC')



