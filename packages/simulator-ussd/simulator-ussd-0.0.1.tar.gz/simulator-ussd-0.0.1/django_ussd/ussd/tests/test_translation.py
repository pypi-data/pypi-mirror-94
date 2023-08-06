from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase
from django.test import Client
from ..models import *
from collections import OrderedDict
import random

class TestUssdTranslation(LiveServerTestCase):
    """
    testing ussd handler text supports multiple language
    """
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
            ),
            Translation.objects.create(
                language='ksw',
                text="Karibu kwa wakopaji {{status(lookup.status)}}:\n"
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
            ),
            Translation.objects.create(
                language='ksw',
                text="Chagua moja ya mkopo:\n",
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


        MenuOptions.objects.create(
                ussd_handler=welcome_screen,
                next_handler=loan_offers,
                index=1
            ).text.add(
                Translation.objects.create(
                language='en',
                text="Request a loan {{status(lookup.status)}}",
            ),
            Translation.objects.create(
                language='ksw',
                text="Omba mkopo {{status(lookup.status)}}",
            )

        )
        # Menu options for welcome screen
        welcome_options = OrderedDict()
        welcome_options["Repay a loan"] = repay_loan
        welcome_options["About us"] = about_us
        welcome_options["Quit"] = quit_screen

        i = 2
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
            ),
            Translation.objects.create(
                language='ksw',
                text="Rudi"
            )
        )
        loan_offers_list_items = ListItems.objects.create(
            iterable="lookup.loan_offers",
            value="item"
        )
        loan_offers_list_items.text.add(
            Translation.objects.create(
                language='en',
                text="Ksh {{item}}\n",
            ),
            Translation.objects.create(
                language='ksw',
                text="Kisw {{item}}\n"
            )
        )
        loan_offers.list_items = loan_offers_list_items

        loan_offers.session_key="loan_amount"
        loan_offers.next_handler = repayment_plan
        MenuOptions.objects.create(
            next_handler=welcome_screen,
            ussd_handler=loan_offers,
            index=1,
            in_put="* "
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back",
            ),
            Translation.objects.create(
                language='ksw',
                text="Rudi",
            )
        )
        loan_offers.save()

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
        self.session_in_progress = 'FC'
        self.end_of_session = 'FB'

    def send_ussd_request(self):
        client = Client()
        return client.get(self.url, data=self.params)

    def test_english(self):
        # new session id
        self.params['sessionId'] = random.randint(0, 10)
        self.params['language'] = 'en'

        response = self.send_ussd_request()

        # welcome screen
        expected_welcome_screen = "Welcome to lenders Franc: has_loan_offers:\n" \
                                  "1. Request a loan Franc: has_loan_offers\n" \
                                  "2. Repay a loan\n3. About us\n4. Quit\n"

        self.assertEqual(response.content.decode(),
                         expected_welcome_screen
                         )

        # select Request a loan
        self.params['input'] = 1
        response = self.send_ussd_request()

        expected_response = "Select one of the loans:\n" \
                            "1. Ksh 300\n2. Ksh 200\n3. Ksh 100\n* Back\n"

        self.assertEqual(response.content.decode(),
                         expected_response
                         )

    def test_kiswahili(self):
        # new session
        self.params['sessionId'] = random.randint(0, 10)
        self.params['language'] = 'ksw'

        response = self.send_ussd_request()

        # welcome screen
        expected_welcome_screen = "Karibu kwa wakopaji Franc: has_loan_offers:\n" \
                                  "1. Omba mkopo Franc: has_loan_offers\n" \
                                  "2. Repay a loan\n3. About us\n4. Quit\n"
        self.assertEqual(response.content.decode(),
                         expected_welcome_screen
                         )

        # select Omba mkopp
        self.params['input'] = 1

        response = self.send_ussd_request()

        expected_response = "Chagua moja ya mkopo:\n" \
                            "1. Kisw 300\n2. Kisw 200\n3. Kisw 100\n* Rudi\n"

        self.assertEqual(response.content.decode(),
                         expected_response
                         )