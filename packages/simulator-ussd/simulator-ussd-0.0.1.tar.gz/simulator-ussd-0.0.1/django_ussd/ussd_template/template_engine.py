__author__ = 'mwas'
__created_date__ = '7/27/15'
__email___ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'

from jinja2 import Template
from ..ussd.models import Widget


class InvalidText(Exception):
    pass

class InvalidIterable(Exception):
    pass

class UssdTemplate(object):
    # todo: look for way to import this with out cyclic import

    def __init__(self, text, context, iterable=None, value='item'):
        """
        This a template engine that extends jinja template by adding custom iterable syntax

        # Iterable syntax

        If iterable is defined then the text should have ""{item}}" - Keyword or keyword "{{value}}"
        if in the text the keyword there is keyword "{{value}}" then context should be should be dictionary

        Only List or dict are the supported iterable.

        iterable : its a string that results to an iterable object when accessed in context
        if its not found in context then results in Invalid iterable object


        # Example of iterable syntax for this template engine

            data = {
                "status": 200,
                "balance": 500,
                "loan_amount": 300,
                "loan_offers": [300, 200, 100],
                "repayment": {
                    300: {7: 330, 14: 350},
                    200: {7: 230, 14: 250},
                    100: {7: 130, 14: 250}
                }

            }


            UssdTemplate("Ksh item ", data, "loan_offers").render()
            it returns:
                    "1.Ksh 300 2.Ksh 200 3. 100"

            Another example

            UssdTemplate("Ksh {{value}} in {{key}} days ", data, "repayment[loan_amount]")
            it returns:
                "1.Ksh 300 in 7 days 2. Ksh 345 in 14 days "

        The other template syntax are the same as the ones in jinja template

        eg.
            UssdTemplate("Dear customer your balance is {{balance}}", {"balance":200}).render()
            results in Dear customer your balance is 200


        :return:
        """

        self.text = text
        self.value = value
        self.context = context
        self.iterable = iterable
        self.rendered_text = None

    def render(self):
        # todo: find a way of importing ListItem with out cyclic import
        from django_ussd.ussd.handlers import ListItem

        list_items = []

        def populate_list_items(text, value):
            list_items.append(ListItem(text, value))

        if not self.iterable:
            template = Template(self.text, keep_trailing_newline=True)
        else:
            template = Template(self._create_jinja_for_loop())


        for widget in Widget.objects.all():
            exec(widget.logic, locals())

        template.globals['populate_list_items'] = populate_list_items
        namespace = locals()
        template.globals.update(namespace)

        rendered_text = template.render(self.context)
        if not self.iterable:
            return rendered_text

        return list_items


    def _create_jinja_for_loop(self):

        # jinja to call populate_list_items function with text and the value

        for_body_template = "{% set text %}"+ self.text +"{% endset %}" \
                            "{{ populate_list_items(text, value_selected)}}" \
                            "{% endfor %}"
        if "{{value}}" in self.text:
            template = "{% for item, value in "+self.iterable+".items() %}{% set value_selected %}{{item}}{% endset %}"
            if self.value == 'value':
                # using double curls for
                template = "{% for item, value in "+ self.iterable+".items() %}{% set value_selected %}{{value}}{% endset %}"

            return template + for_body_template

        return "{% for item in "+ self.iterable +" %}{% set value_selected %}{{item}}{% endset %}}" + for_body_template

