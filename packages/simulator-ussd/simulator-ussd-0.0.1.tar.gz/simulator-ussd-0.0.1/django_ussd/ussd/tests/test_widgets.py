"""
Test widgets used in Ussd screens
"""
from django.core.urlresolvers import reverse

from django.test import LiveServerTestCase, Client
from django_ussd.ussd.models import UssdHandler, HttpRequest, MenuOptions, Widget, Translation
from collections import OrderedDict
import random


class TestWidget(LiveServerTestCase):

    def setUp(self):
        Widget.objects.create(
            logic='def status(status):\n    return "Franc: {}".format(status)'
        )

        welcome_screen = UssdHandler.objects.create(
            name="Welcome_screen",
            http_request=HttpRequest.objects.create(
                name='lookup',
                method='get',
                url="http://localhost:8081/sample/menu/lookup/{{phone_number}}"
            )
        )
        welcome_screen.text.add(
            Translation.objects.create(
                language='en',
                text="Welcome to lenders {{status(lookup.status)}}:\n",
            )
        )

        # list screen
        loan_offers = UssdHandler.objects.create(
            name="loan_offers"
        )
        loan_offers.text.add(
            Translation.objects.create(
                language='en',
                text="Select one of the loans:\n",
            )
        )
        # List/Menu option
        repayment_plan = UssdHandler.objects.create(
            name="loan_repayment_plan",
        )
        repayment_plan.text.add(
            Translation.objects.create(
                language='en',
                text="Choose repayment plan:\n",
            )
        )

        # repaying loan
        repay_loan = UssdHandler.objects.create(
            name="repay_loan",
        )
        repay_loan.text.add(
            Translation.objects.create(
                language='en',
                text="You don't have any loan at the moment",
            )
        )
        # Menu option screen
        about_us = UssdHandler.objects.create(
            name="about_us",
        )
        about_us.text.add(
            Translation.objects.create(
                language='en',
                text="We are rendering company\n",
            )
        )
        # Quit screen
        quit_screen = UssdHandler.objects.create(
            name="quit_screen",
            session_state=False,
        )
        quit_screen.text.add(
            Translation.objects.create(
                language='en',
                text="Thanks for checking our app\n",
            )
        )

        # Menu options for welcome screen
        welcome_options = OrderedDict()
        welcome_options["Request a loan {{status(lookup.status)}}"] = loan_offers
        welcome_options["Repay a loan"] = repay_loan
        welcome_options["About us"] = about_us
        welcome_options["Quit"] = quit_screen

        i = 1
        for key, value in list(welcome_options.items()):
            MenuOptions.objects.create(
                ussd_handler=welcome_screen,
                next_handler=value,
                index=i
            ).text.add(
                Translation.objects.create(
                language='en',
                text=key,
            )
            )
            i += 1

        # Menu options for about screen
        MenuOptions.objects.create(
            ussd_handler=about_us,
            next_handler=welcome_screen,
            index=1,
            in_put="* "
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back",
            )
        )
        # Ussd submission
        ussd_submission = HttpRequest.objects.create(
            url="http://localhost:8081/ussd/submission",
            params='{"action": "loan_request", "loan_amount": {{loan_amount}}, "duration": {{repayment_plan}}}'
        )

        # ussd view url
        self.url = "http://localhost:8000{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="1234",
            input=''
        )
        self.client = Client()

        self.session_in_progress = 'FC'
        self.end_of_session = 'FB'

    def send_ussd_request(self):
        return self.client.get(self.url, data=self.params)

    def test_screens_with_out_list_items(self):
        # new session
        self.params["sessionId"] = random.randint(0, 10)

        # get welcome screen
        response = self.send_ussd_request()

        expected_welcome_screen = "Welcome to lenders Franc: has_loan_offers:\n1. Request a loan Franc: has_loan_offers\n" \
                                  "2. Repay a loan\n3. About us\n4. Quit\n"

        expected_session_status = 'FC'

        self.assertEqual(response.content.decode(), expected_welcome_screen)

        self.assertEqual(response['Freeflow'], expected_session_status)