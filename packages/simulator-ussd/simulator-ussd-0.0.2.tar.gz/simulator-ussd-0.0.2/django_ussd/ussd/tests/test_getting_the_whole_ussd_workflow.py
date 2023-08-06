"""
Test ussd workflow are got in the correct order from the db
"""
from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase, Client
from ..models import *
from ..core import get_ussd_workflow
import unittest

class TestGettingUssdWorkflow(LiveServerTestCase):
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
        Widget.objects.create(
            logic='def status(status):\n    return "Franc: {}".format(status)'
        )

        welcome_screen = UssdHandler.objects.create(
            name="welcome_screen",
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

        repay_loan_router = UssdHandler.objects.create(
            name='repay_loan_router'
        )
         # repaying loan
        has_no_loan_to_repay = UssdHandler.objects.create(
            name="has_no_loan_to_repay",
            session_state=False
        )
        has_no_loan_to_repay.text.add(
            Translation.objects.create(
                language='en',
                text="You don't have any loan at the moment",
            )
        )

        UssdRouterHandler.objects.create(
            ussd_handler=repay_loan_router,
            next_handler=has_no_loan_to_repay,
            expression='lookup["status"]!="has_pending_loan"',
            index=1,
        )
        confirm_loan_repayment = UssdHandler.objects.create(
            name='confirm_loan_repayment',
            session_state=False
        )
        confirm_loan_repayment.text.add(
            Translation.objects.create(
                language='en',
                text="Thanks for your repayment you will "
                     "receive your sms shortly"
            )
        )
        repay_loan = UssdHandler.objects.create(
            name="repay_loan",
        )
        repay_loan.text.add(
            Translation.objects.create(
                language='en',
                text="Confirm to pay you loan of {{lookup.pending_loan}}\n"
            )
        )
        MenuOptions.objects.create(
            index=1,
            ussd_handler=repay_loan,
            next_handler=confirm_loan_repayment
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Confirm"
            )
        )
        MenuOptions.objects.create(
            index=2,
            in_put='* ',
            in_put_value='*',
            ussd_handler=repay_loan,
            next_handler=welcome_screen
        ).text.add(
            Translation.objects.create(
                language='en',
                text="Back"
            )
        )
        UssdRouterHandler.objects.create(
            ussd_handler=repay_loan_router,
            next_handler=repay_loan,
            expression='True',
            index=2,
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
        enter_your_age = UssdHandler.objects.create(
            name='enter_your_age',
            next_handler=welcome_screen,
            session_key='age',
        )
        enter_your_age.text.add(
            Translation.objects.create(
                language='en',
                text="Hi {{name}} now enter your age"
            )
        )
        enter_name = UssdHandler.objects.create(
            name='enter_name',
            session_key='name',
            next_handler=enter_your_age
        )
        enter_name.text.add(
            Translation.objects.create(
                language='en',
                text="Enter your name\n"
            )
        )

        # Menu options for welcome screen
        welcome_options = OrderedDict()
        welcome_options["Repay a loan"] = repay_loan_router
        welcome_options["About us"] = about_us
        welcome_options["Quit"] = quit_screen
        welcome_options["Enter your name"] = enter_name

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
            in_put="* ",
            in_put_value='*'
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
            in_put="* ",
            in_put_value='*'
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
            in_put="* ",
            in_put_value="*"
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

        # another ussd journey
        thank_you_2 = UssdHandler.objects.create(
            name="thank_you_2",
            session_state=False
        )
        thank_you_2.text.add(
            Translation.objects.create(
                language='en',
                text="Thank you for your loan application. your loan will " \
                   "be processed and you will be notified\n",
            )
        )
        enter_your_age_2 = UssdHandler.objects.create(
            name='enter_your_age_2',
            next_handler=thank_you_2,
            session_key='age',
        )
        enter_your_age_2.text.add(
            Translation.objects.create(
                language='en',
                text="Hi {{name}} now enter your age"
            )
        )
        enter_name_2 = UssdHandler.objects.create(
            name='enter_name_2',
            session_key='name',
            next_handler=enter_your_age_2
        )
        enter_name_2.text.add(
            Translation.objects.create(
                language='en',
                text="Enter your name\n"
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

        #this covers for all types of ussd screens we have
        #       - input
        #       - list screen
        #       - menu screen
        #       _ menu/list screen
        #       - router screen
        #       - quit screen
        self.expected_ussd_workflow = dict(
            welcome_screen=dict(
                loan_offers=dict(input='1'),
                repay_loan_router=dict(input='2'),
                about_us=dict(input='3'),
                quit_screen=dict(
                    input='4',
                ),
                enter_name=dict(
                    input='5'
                )
            ),
            loan_offers=dict(
                loan_repayment_plan=dict(
                    input='loan_amount'
                ),
                welcome_screen=dict(
                    input='*',
                )
            ),
            loan_repayment_plan=dict(
                confirm_loan=dict(
                    input='repayment_plan'
                ),
                welcome_screen=dict(
                    input='*'
                )
            ),
            confirm_loan=dict(
                thank_you_screen=dict(
                    input='2',
                ),
                loan_repayment_plan=dict(
                    input='1'
                )
            ),
            repay_loan_router=dict(
                has_no_loan_to_repay=dict(
                    input='lookup["status"]!="has_pending_loan"'
                ),
                repay_loan=dict(
                    input='True'
                )
            ),
            repay_loan=dict(
                confirm_loan_repayment=dict(
                    input='1',
                ),
                welcome_screen=dict(
                    input='*',
                )

            ),
            about_us=dict(
                welcome_screen=dict(
                    input="*",
                )
            ),
            enter_name=dict(
                enter_your_age=dict(
                    input="name"
                )
            ),
            enter_your_age=dict(
                welcome_screen=dict(
                    input="age"
                )
            )

        )
        self.screen_nodes = dict(
            welcome_screen=dict(
                text=dict(
                    en="Welcome to lenders {{status(lookup.status)}}:\n"
                       "1. Request a loan {{status(lookup.status)}}\n"
                       "2. Repay a loan\n3. About us\n4. Quit\n5. Enter your name\n",
                    ksw="Karibu kwa wakopaji {{status(lookup.status)}}:\n"
                        "1. Omba mkopo {{status(lookup.status)}}\n"
                        "2. Repay a loan\n3. About us\n4. Quit\n5. Enter your name\n"
                ),
            ),
            loan_offers=dict(
                text=dict(
                    en="Select one of the loans:\n* Back\n",
                    ksw="Chagua moja ya mkopo:\n* Rudi\n"
                )
            ),
            loan_repayment_plan=dict(
                text=dict(
                    en="Choose repayment plan:\n* Back\n"
                )
            ),
            confirm_loan=dict(
                text=dict(
                    en="Confirm your loan application of "
                       "Ksh {{loan_amount}} to be paid by "
                       "interest of Ksh {{lookup.repayment[loan_amount][repayment_plan]"
                       "}} in {{repayment_plan}} days\n2. Confirm\n1. Back\n"
                )
            ),
            repay_loan_router=dict(
                text=dict()
            ),
            has_no_loan_to_repay=dict(
                text=dict(
                    en="You don't have any loan at the moment"
                )
            ),
            repay_loan=dict(
                text=dict(
                    en="Confirm to pay you loan of {{lookup.pending_loan}}\n"
                       "1. Confirm\n* Back\n"
                )
            ),
            confirm_loan_repayment=dict(
                text=dict(
                    en="Thanks for your repayment you will "
                       "receive your sms shortly"
                )
            ),
            about_us=dict(
                text=dict(
                    en="We are rendering company\n* Back\n"
                )
            ),
            quit_screen=dict(
                text=dict(
                    en="Thanks for checking our app\n"
                )
            ),
            enter_name=dict(
                text=dict(
                    en="Enter your name\n"
                )
            ),
            thank_you_screen=dict(
                text=dict(
                    en='Thank you for your loan application. '
                       'your loan will be processed and you will be notified\n'
                )
            ),
            enter_your_age=dict(
                text=dict(
                    en='Hi {{name}} now enter your age'
                )
            )
        )

    def test_ussd_workflow(self):
        ussd_journey = get_ussd_workflow('welcome_screen')
        ussd_workflow = ussd_journey['edges']
        ussd_content = ussd_journey['nodes']
        for screen in self.expected_ussd_workflow.keys():
            if ussd_workflow.get(screen):
                print('screen', screen)
                print("actual", ussd_workflow[screen])
                print('expected', self.expected_ussd_workflow[screen])
                self.assertEqual(ussd_workflow[screen],
                                 self.expected_ussd_workflow[screen]
                                 )
            else:
                self.assertTrue(False,
                                "missing this screen {}".format(self.expected_ussd_workflow[screen]))

        for screen in ussd_workflow.keys():
            if self.expected_ussd_workflow.get(screen):
                print('screen', screen)
                print("actual", ussd_workflow[screen])
                print('expected', self.expected_ussd_workflow[screen])
                self.assertEqual(ussd_workflow[screen],
                                 self.expected_ussd_workflow[screen]
                                 )
            else:
                self.assertTrue(False,
                                "missing this screen {}".format(ussd_workflow[screen]))


        self.assertEqual(ussd_workflow, self.expected_ussd_workflow)
        # import pdb; pdb.set_trace()
        for screen in self.screen_nodes.keys():
            if ussd_content.get(screen):
                print("screen", screen)
                print("actual", ussd_content[screen])
                print('expected', self.screen_nodes[screen])
                self.assertEqual(ussd_content[screen], self.screen_nodes[screen])
            else:

                self.assertTrue(False,
                                "missing this screen {0}:{1}".format(
                                    screen,
                                    self.screen_nodes[screen])
                                )
        for screen in ussd_content.keys():
            if self.screen_nodes.get(screen):
                print("screen", screen)
                print("actual", ussd_content[screen])
                print('expected', self.screen_nodes[screen])
                self.assertEqual(ussd_content[screen], self.screen_nodes[screen])
            else:

                self.assertTrue(False,
                                "missing this screen {0}:{1}".format(
                                    screen,
                                    ussd_content[screen])
                                )
        self.assertEqual(ussd_content, self.screen_nodes)

    def test_getting_ussd_workflow_from_input_screen(self):

        expected_edges = dict(
                enter_name_2=dict(
                        enter_your_age_2=dict(
                        input="name"
                        )
                ),
                enter_your_age_2=dict(
                        thank_you_2=dict(
                                input="age"
                        )
                )
        )
        expected_nodes = dict(
            enter_name_2=dict(
                text=dict(
                    en="Enter your name\n"
                )
            ),
            enter_your_age_2=dict(
                text=dict(
                    en='Hi {{name}} now enter your age'
                )
            ),
            thank_you_2=dict(
                text=dict(
                    en='Thank you for your loan application. '
                       'your loan will be processed and you will be notified\n'
                )
            ),
        )

        ussd_workflow = get_ussd_workflow('enter_name_2')
        ussd_journey = ussd_workflow['edges']
        ussd_content = ussd_workflow['nodes']

        self.assertEqual(ussd_journey, expected_edges)
        self.assertEqual(ussd_content, expected_nodes)

