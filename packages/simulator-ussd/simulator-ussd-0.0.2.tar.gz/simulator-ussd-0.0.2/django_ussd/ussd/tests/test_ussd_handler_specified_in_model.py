__author__ = 'Mwaaas'
__email__ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'


"""
This test ussd creation via models
"""

from django_ussd.ussd.core import UssdAppModelView, UssdRequest, UssdAppView, SessionStore
from django_ussd.http.views import UssdSimulatorView
from django_ussd.ussd.models import *
from django.http import HttpResponse
from django.test import TestCase, LiveServerTestCase
from django.views.generic import View
from rest_framework import status
from django.http import HttpResponse
import json
from django.test import Client
from django.core.urlresolvers import reverse
import unittest
from collections import OrderedDict
import random
import mock
from datetime import datetime

import os

# create ussd view that uses model to create ussd handlers ( ussd screens )
class SampleUssdModelView(UssdAppModelView):

    # initial handler should be an model instance
    initial_handler = "Welcome_screen"

    def get(self, req):
        language = req.GET.get('language', 'en')
        return UssdRequest(req.GET['msisdn'],
                           req.GET['sessionId'],
                           req.GET['input'],
                           language=language
                           )

    def ussd_response_handler(self, ussd_response):
        response = HttpResponse(str(ussd_response))
        response['Freeflow'] = 'FB'
        if ussd_response.status:
            response['Freeflow'] = 'FC'
        return response

class SampleUssdSimulator(UssdSimulatorView):
    ussd_view = SampleUssdModelView
    ussd_view_url_name = 'sample_ussd_view'
    phoneNumber = 'msisdn'
    session_id = 'sessionId'
    input = 'input'
    language = 'LANGUAGE'
    login_required = False

    def response_handler(self, response):
        response_status = response.headers['Freeflow']
        response_message = response.content

        if response_status == 'FB':
            return False, response_message
        return True, response_message


class MockMenuLookupToUse(View):
    def get(self, req, msisdn):
        data = dict(
            status=200,
            loan_offers=["300", "200", "100"],
            repayment={"300": {7: 350, 5: 250},
                       "200": {7: 300}, 100: {8: 500}}
            )
        data = '{"status": "has_loan_offers", "loan_offers": [ "300", "200", "100" ],' \
               '"repayment": { "300": { "7": 350,"5": 250},"200": {"7": 250, "5": 230},"100": {"7": 150, "5": 130}}}'

        # msisdn for user has no loan offers
        if msisdn == '423':
            data = '{"status": "no_loan_offers", "loan_offers": [ "300", "200", "100" ],' \
               '"repayment": { "300": { "7": 350,"5": 250},"200": {"7": 300},"100": {"8": 500}}}'

        # msisdn for user not qualified
        if msisdn == '403':
            data = '{"status": "ineligible_user", "loan_offers": [ "300", "200", "100" ],' \
               '"repayment": { "300": { "7": 350,"5": 250},"200": {"7": 300},"100": {"8": 500}}}'

        # msisdn with a pending loan
        if msisdn == '456':
            data = '{"status": "has_pending_loan", "pending_loan":600}'


        return HttpResponse(data, status=status.HTTP_200_OK)

class TestUssdHandler(LiveServerTestCase):
    """
    test ussd by creating ussd screens by models instead of creating Handler classes

    # Test the following workflow

    A) welcome screen
    ---------------------------
     Welcome to renders:
            1. Request a loan
            2. Repay a loan
            3. About us
            4. Quit

    B) Option 1 selected
    --------------------------------

        Select one of the loans:
            1. Ksh 300
            2. Ksh 200
            3. Ksh 100
            4. Back

    C) Option 1 selected
    ----------------------------------

        Choose repayment plan
            1. KSH 350 in 7 days
            2. KSH 250 in 5 days
            3. Back

    D) Option 2 selected

        Confirm your loan application of Ksh 300 to be paid by
        interest of Ksh 330 in 7 days
            1. Confirm
            2. Back

    E) select option 1 ( to confirm the loan application)

        Thank you for your loan application . your loan will be
        processed and you will be notified



    The above workflow tests the following screens and functionality:
        - Menu screen
        - Menu and screen
        - Input screen
        - Quit screen

    example of menu lookup:
        {
        status=200,
        loan_offers=[300, 200, 100],
        repayment={300:{7:350, 5:250}, 200:{7: 300}, 100:{8:500} }
        }

    """
    maxDiff = None
    def setUp(self):
        # Menu screen
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
                text="Welcome to lenders:\n",
            )
        )
        # list screen
        loan_offers = UssdHandler.objects.create(
            name="loan_offers",
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
        welcome_options["Request a loan"] = loan_offers
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

        loan_offers_list_items = ListItems.objects.create(
            iterable="lookup.loan_offers",
            value="item"
        )
        loan_offers_list_items.text.add(
            Translation.objects.create(
                language='en',
                text="Ksh {{item}}\n",
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
            )
        )
        loan_offers.save()

        repayment_plan_list_items = ListItems.objects.create(
            iterable="lookup.repayment[loan_amount]",
            value='item'
        )
        repayment_plan_list_items.text.add(
            Translation.objects.create(
                language='en',
                text="Ksh {{value}} in {{item}} days\n",
            )
        )
        repayment_plan.list_items = repayment_plan_list_items
        repayment_plan.session_key = 'repayment_plan'

        confirm_loan = UssdHandler.objects.create(
            name="confirm_loan",
        )
        confirm_loan.text.add(
            Translation.objects.create(
                language='en',
                text="Confirm your loan application of "
                  "Ksh {{loan_amount}} to be paid by "
                  "interest of Ksh {{lookup.repayment[loan_amount][repayment_plan]"
                  "}} in {{repayment_plan}} days\n",
            )
        )
        repayment_plan.next_handler = confirm_loan

        repayment_plan.save()

        MenuOptions.objects.create(
            next_handler=welcome_screen,
            ussd_handler=repayment_plan,
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

        ThankYou = UssdHandler.objects.create(
            name="thank_you_screen",
            session_state = False,
            http_request=ussd_submission

        )
        ThankYou.text.add(
            Translation.objects.create(
                language='en',
                text="Thank you for your loan application. your loan will " \
                   "be processed and you will be notified\n",
            )
        )

        MenuOptions.objects.create(
            next_handler=ThankYou,
            ussd_handler=confirm_loan,
            index=2
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Confirm",
            )
        )
        MenuOptions.objects.create(
            next_handler=repayment_plan,
            ussd_handler=confirm_loan,
            index=1
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back",
            )
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

    def send_ussd_reqeust(self):
        return self.client.get(self.url, data=self.params)

    def test_screens_with_out_list_items(self):
        # new session
        self.params["sessionId"] = random.randint(0, 10)

        # get welcome screen
        response = self.send_ussd_reqeust()

        expected_welcome_screen = "Welcome to lenders:\n1. Request a loan\n" \
                                  "2. Repay a loan\n3. About us\n4. Quit\n"

        expected_session_status = 'FC'


        self.assertEqual(response.content.decode(), expected_welcome_screen)

        self.assertEqual(response['Freeflow'], expected_session_status)

        # select option 3 ( About us )
        self.params['input'] = 3

        response = self.send_ussd_reqeust()

        expected_about_screen = "We are rendering company\n* Back\n"
        self.assertEqual(response.content.decode(), expected_about_screen)
        self.assertEqual(response['Freeflow'], expected_session_status)

        # go back
        self.params['input'] = '*'
        response = self.send_ussd_reqeust()

        self.assertEqual(response.content.decode(), expected_welcome_screen)
        self.assertEqual(response['Freeflow'], expected_session_status)

        # select option 4 ( Quit )
        self.params['input'] = 4
        response = self.send_ussd_reqeust()

        self.assertEqual(response.content.decode(), "Thanks for checking our app\n")
        self.assertEqual(response['Freeflow'], 'FB')

    @mock.patch("django_ussd.ussd.core.datetime")
    @mock.patch("django_ussd.ussd.core.requests.post")
    def test_list_item_screen(self, request_post_mock, datetime_mock):
        request_post_mock.return_value.content = b''
        request_post_mock.return_value.status_code = 200
        time = datetime.now()

        datetime_mock.now.return_value = time
        # new session
        self.params["sessionId"] = random.randint(11, 20)

        # dial in to welcome screen
        response = self.send_ussd_reqeust()

        # select 1 to request a loan
        self.params['input'] = 1

        response = self.send_ussd_reqeust()

        expected_response = "Select one of the loans:\n" \
                            "1. Ksh 300\n2. Ksh 200\n3. Ksh 100\n* Back\n"


        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'],
                         self.session_in_progress)


        # choose loan amount of 300
        self.params['input'] = 1

        response = self.send_ussd_reqeust()

        expected_response = "Choose repayment plan:\n" \
                            "1. Ksh 350 in 7 days\n" \
                            "2. Ksh 250 in 5 days\n" \
                            "* Back\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'],
                         self.session_in_progress)

        # select one of the repayment plan
        self.params['input'] = 2

        response = self.send_ussd_reqeust()

        expected_response = "Confirm your loan application of Ksh 300 " \
                            "to be paid by interest of Ksh 250 in 5 days\n" \
                            "1. Back\n" \
                            "2. Confirm\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'],
                         self.session_in_progress)

        # confirm loan application
        self.params['input'] = 2

        response = self.send_ussd_reqeust()

        expected_response = "Thank you for your loan application. your loan will " \
                   "be processed and you will be notified\n"

        self.assertEqual(response.content.decode(), expected_response)
        self.assertEqual(response['Freeflow'],
                         self.end_of_session)

        # test ussd submission function is called
        request_post_mock.assert_called_once_with(
            'http://localhost:8081/ussd/submission',
            data='{"action": "loan_request", "loan_amount": 300, "duration": 5}',
            headers={'Content-Type': 'application/json'}, timeout=10
        )

        # confirm ussd steps have recorded
        #time = datetime.now()

        process = [
            dict(
                duration=0,
                start=time,
                end=time,
                name="Welcome_screen",
                screen_text="Welcome to lenders:\n1. Request a loan\n2. Repay a loan\n3. About us\n4. Quit\n",
                selection='1'
            ),
            dict(
                duration=0,
                start=time,
                end=time,
                name="loan_offers",
                screen_text="Select one of the loans:\n1. Ksh 300\n2. Ksh 200\n3. Ksh 100\n* Back\n",
                selection='1'
            ),
            dict(
                duration=0,
                start=time,
                end=time,
                name="loan_repayment_plan",
                screen_text="Choose repayment plan:\n" \
                            "1. Ksh 350 in 7 days\n" \
                            "2. Ksh 250 in 5 days\n" \
                            "* Back\n",
                selection='2'
            ),
            dict(
                duration=0,
                start=time,
                end=time,
                name="confirm_loan",
                screen_text="Confirm your loan application of Ksh 300 " \
                            "to be paid by interest of Ksh 250 in 5 days\n" \
                            "1. Back\n" \
                            "2. Confirm\n",
                selection='2'
            ),
            dict(
                duration=None,
                start=time,
                name="thank_you_screen",
                screen_text="Thank you for your loan application. your loan will " \
                   "be processed and you will be notified\n"
            )
        ]

        session = SessionStore(self.params['sessionId'])
        steps = session['steps']

        for i, screen in enumerate(process):
            self.assertEqual(screen, steps[i])
        self.assertEqual(process, steps)

class TestUssdRequestForwarder(LiveServerTestCase):

    def setUp(self):

        # This screen is displayed to all users
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
                text="Welcome to lenders:\n",
            )
        )

        # loan_choices_router
        loan_choices_router = UssdHandler.objects.create(
            name="loan_choices_router"
        )

        # loan_offers
        loan_offers = UssdHandler.objects.create(
            name="loan_offers",
        )
        loan_offers.text.add(
            Translation.objects.create(
                language='en',
                text="Select one of the loans:\n",
            )
        )

        loan_offers_list_items = ListItems.objects.create(
            iterable="lookup.loan_offers",
            value="item")
        loan_offers_list_items.text.add(
            Translation.objects.create(
                language='en',
                text="Ksh {{item}}\n",
            )
        )
        loan_offers.list_items = loan_offers_list_items
        loan_offers.session_key = "loan_amount"
        loan_offers.save()
        # use with no loan offers
        no_loan_offers= UssdHandler.objects.create(
            name="not_qualified_for_loan_offers",
        )
        no_loan_offers.text.add(
            Translation.objects.create(
                language='en',
                text="Continue using this service to qualify for "
                  "loan offers\n",
            )
        )
        MenuOptions.objects.create(
            next_handler=welcome_screen,
            ussd_handler=no_loan_offers,
            index=1,
            in_put="* "
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back",
            )
        )

        # ineligible user
        not_qualified_user = UssdHandler.objects.create(
            name="ineligible",
        )
        not_qualified_user.text.add(
            Translation.objects.create(
                language='en',
                text="You are ineligible user wait for 6 months\n",
            )
        )
        MenuOptions.objects.create(
            next_handler=welcome_screen,
            ussd_handler=not_qualified_user,
            index=1,
            in_put="* ",
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back",
            )
        )
        UssdRouterHandler.objects.create(
            ussd_handler=loan_choices_router,
            next_handler=loan_offers,
            expression='lookup["status"]=="has_loan_offers"',
            index=1,
        )

        UssdRouterHandler.objects.create(
            ussd_handler=loan_choices_router,
            next_handler=no_loan_offers,
            expression='lookup["status"]=="no_loan_offers"',
            index=2,
        )
        UssdRouterHandler.objects.create(
            ussd_handler=loan_choices_router,
            next_handler=not_qualified_user,
            expression='lookup["status"]=="ineligible_user"',
            index=3,
        )

        MenuOptions.objects.create(
            ussd_handler=welcome_screen,
            next_handler=loan_choices_router,
            index=1,
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Loan offers",
            )
        )

        # ussd view url
        self.url = "http://localhost:8000{}".format(reverse('sample_ussd_view'))
        self.params = dict(
            msisdn="0702729654",
            sessionId="1234",
            input=''
        )
        self.client = Client()

    def send_ussd_reqeust(self, msisdn, session_id, input_=0):
        params = dict(
            msisdn=msisdn,
            sessionId=session_id,
            input=input_
        )
        return self.client.get(self.url, data=params)

    def check_first_screen(self, response):
        expected_response = "Welcome to lenders:\n1. Loan offers\n"

        self.assertEqual(expected_response, response.content.decode())

    def test_status_has_loan_offers(self):
        session_id = random.randint(0, 10)
        # send a request
        response = self.send_ussd_reqeust(msisdn=200,
                                          session_id=session_id,
                                          )

        self.check_first_screen(response)

        # select loan offers
        response = self.send_ussd_reqeust(msisdn=200, session_id=session_id, input_=1)

        expected_response = "Select one of the loans:\n1. Ksh 300\n2. Ksh 200\n3. Ksh 100\n"

        self.assertEqual(response.content.decode(), expected_response)


    def test_status_has_no_loan_offers(self):
        session_id = random.randint(10, 100)

        response = self.send_ussd_reqeust(msisdn=423, session_id=session_id, input_=1)

        self.check_first_screen(response)

        response = self.send_ussd_reqeust(msisdn=423, session_id=session_id, input_=1)

        expected_response = "Continue using this service to qualify for loan offers\n* Back\n"

        self.assertEqual(response.content.decode(), expected_response)

    def test_status_ineligible(self):
        session_id = random.randint(100, 1000)

        response = self.send_ussd_reqeust(msisdn=403, session_id=session_id, input_=1)

        self.check_first_screen(response)

        response = self.send_ussd_reqeust(msisdn=403, session_id=session_id, input_=1)

        expected_response = "You are ineligible user wait for 6 months\n* Back\n"

        self.assertEqual(response.content.decode(), expected_response)