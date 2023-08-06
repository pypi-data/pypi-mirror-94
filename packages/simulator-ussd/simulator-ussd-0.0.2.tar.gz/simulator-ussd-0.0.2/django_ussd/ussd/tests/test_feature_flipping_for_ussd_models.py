"""
Tests feature flipping in ussd handled by models
"""

from django.test import TestCase
from ..feature_flipping import *
import unittest
#todo test for screens using custom handler

@unittest.skip("not done with model implementation yet")
class TestCreationOfFlag(TestCase):

    def test_input_screen(self):
        age_screen = UssdHandler.objects.create(
            name="age_screen",
            title="Your age is",
            session_state=False
        )
        # test input screen
        input_screen = UssdHandler.objects.create(
            name="input_screen",
            title="Enter your name",
            session_key="name",
            next_handler=age_screen
        )

        create_ussd_handler_flag("change_of_age", input_screen)

        # a new ussd_handler should be created with name prefixed
        # with flag name
        expected_handler = UssdHandler.objects.get(
            name="change_of_age:input_screen"
        )

        self.assertEqual(expected_handler.title, "Enter your name")
        self.assertEqual(expected_handler.session_key, "name")
        self.assertEqual(expected_handler.next_handler, age_screen)

    def test_input_screen_with_custom_next_handler(self):

        input_screen = UssdHandler.objects.create(
            name="input_screen_with_custom_handler",
            title="Enter your name",
            session_key="name",
            next_custom_handler="AgeHandler",
        )

        create_ussd_handler_flag("change_of_title", input_screen)

        expected_handler = UssdHandler.objects.get(
            name="input_screen_with_custom_handler"
        )

        self.assertEqual(expected_handler.title, "Enter your name")
        self.assertEqual(expected_handler.session_key, "name")
        self.assertEqual(expected_handler.next_custom_handler, "AgeHandler")

    def test_quit_screen(self):
        quit_screen = UssdHandler.objects.create(
            name="quit_screens",
            title="Thanks for using this screen",
            session_state=False
        )

        create_ussd_handler_flag("quit_screen_change", quit_screen)

        expected_handler = UssdHandler.objects.get(name="quit_screen_change:quit_screens")

        self.assertEqual(expected_handler.title, "Thanks for using this screen")
        self.assertEqual(expected_handler.session_state, False)

    @unittest.skip("issue with feature flipping will fix this later")
    def test_list_item_screen(self):
        pricing = UssdHandler.objects.create(
            name="pricing",
            title="select one of the price"
        )
        list_items = ListItems.objects.create(
            text="fruits",
            iterable="{{fruits}}",
            value="item"
        )

        list_item_screen = UssdHandler.objects.create(
            name="list_item_screens",
            title="Choose your favourite fruits",
            list_items=list_items,
            next_handler=pricing
        )

        create_ussd_handler_flag('list_item_change', list_item_screen)

        expected_handler = UssdHandler.objects.get(name="list_item_screens")

        self.assertEqual(expected_handler.title, "Choose your favourite fruits")
        self.assertEqual(expected_handler.next_handler, pricing)
        self.assertEqual(expected_handler.list_items, list_item_screen.list_items)

        # test for screen with a custom next handler
        list_item_with_custom_handler = UssdHandler.objects.create(
            name="list_item_screens_",
            title="Choose your favourite fruits",
            list_items=list_items,
            next_custom_handler="pricing"
        )

        expected_handler = UssdHandler.objects.get(name='list_item_screens_')

        self.assertEqual(expected_handler.title, "Choose your favourite fruits")
        self.assertEqual(expected_handler.next_custom_handler, "pricing")
        self.assertEqual(expected_handler.list_items, list_item_screen.list_items)

    @unittest.skip("issue with feature flipping will fix this later")
    def test_menu_options_with_list_items(self):
        pricing = UssdHandler.objects.create(
            name="pricing",
            title="select one of the price"
        )
        list_items = ListItems.objects.create(
            text="fruits",
            iterable="{{fruits}}",
            value="key"
        )
        welcome = UssdHandler.objects.create(
            name='welcome',
            title="Enter your name"
        )
        # menu screen that we are testing
        menu_screens = UssdHandler.objects.create(
            name="menu_screen",
            title="choose your options",
            list_items=list_items,
            next_handler=pricing,
        )

        MenuOptions.objects.create(
            name="Welcome",
            next_handler=welcome,
            ussd_handler=menu_screens,
            index=1,
        )
        MenuOptions.objects.create(
            name="with_custom_next_handler",
            next_custom_handler='Age',
            ussd_handler=menu_screens,
            index=2,
        )

        create_ussd_handler_flag('menu_option_flag', menu_screens)

        expected_handler = UssdHandler.objects.get(name='menu_option_flag:menu_screen')

        self.assertEqual(expected_handler.title, "choose your options")
        self.assertEqual(expected_handler.next_handler, pricing)
        self.assertEqual(expected_handler.list_items, list_items)

        expected_menu_options = MenuOptions.objects.filter(ussd_handler=expected_handler)

        menu_options = MenuOptions.objects.filter(ussd_handler=menu_screens)

        self.assertEqual(len(menu_options), len(expected_menu_options))

        for i, o in enumerate(menu_options):
            flag_menu = expected_menu_options[i]
            self.assertEqual(flag_menu.name, o.name)
            self.assertEqual(flag_menu.next_handler, o.next_handler)
            self.assertEqual(flag_menu.next_custom_handler, o.next_custom_handler)
            self.assertEqual(flag_menu.index, o.index)
            self.assertEqual(flag_menu.in_put, o.in_put)



