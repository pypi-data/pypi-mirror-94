__author__ = 'mwas'
__created_date__ = '7/27/15'
__email___ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'

import json
from collections import OrderedDict
import unittest

from django.test import TestCase
from django_ussd.ussd_template.template_engine import UssdTemplate, InvalidText, InvalidIterable
from django_ussd.ussd.handlers import ListItem


class TestHappyCase(TestCase):
    def setUp(self):
        # data to be used to render template
        self.data = '{"status": 200,"balance": 500,"loan_amount": "200","loan_offers": ["300","200","100"],"repayment": {"100": {"7": 130,"14": 250},"200": {"7": 230,"14": 250},"300": {"7": 330,"14": 350}}}'

        self.data = json.loads(self.data, object_pairs_hook=OrderedDict)
        # data to be stored in session

    def test_display_single_object(self):
        expected_rendered_text = "Dear customer your balance is 500"
        actual_text = UssdTemplate("Dear customer your balance is {{balance}}", self.data).render()
        self.assertEqual(expected_rendered_text, actual_text)

    def test_display_list_of_items_from_list_data_stucture_context(self):
        actual_text = UssdTemplate("Ksh {{item}}\n", self.data, 'loan_offers').render()

        expected_list_item_objects = [ListItem("Ksh 300\n", "300"), ListItem("Ksh 200\n", "200"),
                                     ListItem("Ksh 100\n", "100")
                                     ]

        self.assertEqual(expected_list_item_objects, actual_text)

    def test_display_list_of_items_from_dict_data_structure(self):
        actual_text = UssdTemplate("Ksh {{item}}\n", self.data,
                                   'repayment').render()

        expected_list_item_objects = [
            ListItem("Ksh 100\n", "100"), ListItem("Ksh 200\n", "200"),
            ListItem("Ksh 300\n", "300")
        ]


        self.assertEqual(expected_list_item_objects, actual_text)

    def test_display_list_of_items_from_dict_using_both_key_and_value(self):
        actual_text = UssdTemplate("Repay Ksh {{value}} in {{item}} days\n", self.data,
                                   "repayment[loan_amount]").render()

        expected_list_item_objects = [
            ListItem("Repay Ksh 230 in 7 days\n", "7"),
            ListItem('Repay Ksh 250 in 14 days\n', '14')
        ]

        self.assertEqual(expected_list_item_objects, actual_text)

    def test_we_can_have_template_syntax_in_iterable_template(self):

        actual_text = UssdTemplate("Ksh {{item}} {{balance}}\n", self.data, 'loan_offers').render()

        expected_list_item_objects = [
            ListItem("Ksh 300 500\n", "300"),
            ListItem("Ksh 200 500\n", "200"),
            ListItem("Ksh 100 500\n", "100")
        ]
        self.assertEqual(actual_text, expected_list_item_objects)

    def test_having_a_different_value_in_list_item_object(self):

        actual_text = UssdTemplate("Repay Ksh {{value}} in {{item}} days\n", self.data,
                                   "repayment[loan_amount]", value='value').render()

        expected_list_item_objects = [
            ListItem("Repay Ksh 230 in 7 days\n", "230"),
            ListItem('Repay Ksh 250 in 14 days\n', '250')
        ]

        self.assertEqual(expected_list_item_objects, actual_text)

@unittest.skip("validation for UssdTemplate has not been implemented")
class SanityCheck(TestCase):
    def setUp(self):
        # data to be used to render template
        self.data = {
            "status": 200,
            "balance": 500,
            "loan_amount": 200,
            "loan_offers": [300, 200, 100],
            "repayment": {
                300: {7: 330, 14: 350},
                200: {7: 230, 14: 250},
                100: {7: 130, 14: 250}
            }

        }

    def test_if_iterable_is_defined_then_word_item_shouldbe_present_in_text_parameter(self):
        self.assertRaises(InvalidText, UssdTemplate,
                          "template without the required keyword and render is defined",
                          self.data, 'loan_amount')

    def test_iterable_is_defined_but_cannot_be_accessed_in_context_provided(self):
        self.assertRaises(InvalidIterable, UssdTemplate,
                          "valid text but invalid template {{item}}",
                          self.data, 'not_found')

        self.assertRaises(InvalidIterable, UssdTemplate,
                          "valid text but invalid template {{item}}",
                          self.data, 'repayment[balance]')

    def test_both_text_and_iterable_are_invalid(self):
        self.assertRaises(InvalidText, UssdTemplate,
                          "template without the required keyword and render is defined",
                          self.data, 'invalid_iterable')
