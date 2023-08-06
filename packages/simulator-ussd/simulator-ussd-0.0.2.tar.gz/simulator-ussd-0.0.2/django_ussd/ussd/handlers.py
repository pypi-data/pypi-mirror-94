import datetime
from django.core.exceptions import ValidationError
from .core import UssdResponse, _handlers
from django.core.paginator import Paginator
from django.utils.translation import ugettext as _


class MissingAttribute(Exception):
    pass
    

class HandlerMeta(type):
    """Metaclass to register handlers upon creation"""
    def __init__(cls, name, bases, attrs):
        """
        Validates a handler class and registers it in a lookup table.
        """
        super(HandlerMeta, cls).__init__(name, bases, attrs)

        # Check for existence of required attributes, but only in
        # child classes of child classes of Handler.
        is_grandchild_class = (bases[0].__name__ != 'Handler')
        if '__required_attrs__' in attrs and is_grandchild_class:
            error_message = '%s required for handler %s'
            for attr_name in attrs['__required_attrs__']:
                if attr_name not in attrs:
                    raise MissingAttribute(error_message % (attr_name, name))

        # Register an instance of the handler
        handler_instance = cls()
        _handlers[name] = handler_instance


class Handler(object, metaclass=HandlerMeta):
    def handle(self, req):
        """Abstract method called by USSD framework; should be
        implemented in subclasses"""
        raise NotImplementedError

    def get_option(self, options, index):
        """
        gets option in terms of index provided or input text

        :param options: list or tuple whose values are MenuOption
        :param index:
                    :type  int or string
                    :description it can be index of menu option or input_text selected
        :return: return MenuOption object or raises ValueError or IndexError
        """
        if isinstance(index, int):
            return options[index]
        elif isinstance(index, str):
            for option in options:
                if option.input_value:
                    if option.input_value.strip() == index.strip():
                        return option
        else:
            raise ValueError("Please enter a valid number/choice")
        raise ValueError("index not found in options list")


class Input(Handler):
    """
    A handler that prompts the user for input, then stores it in the
    current session. 
    
    Required attributes:
   
    prompt        A string to display to the user 
    session_key   Key under which to store user input in session
    next_handler  Name of the handler to forward control to 
    """

    __required_attrs__ = ('prompt', 'next_handler', 'session_key', 'do_not_log')
                                           
    def handle(self, req):
        # Replace prompt with text if it is callable
        if hasattr(self, 'get_prompt'):
            self.prompt = self.get_prompt(req)
            if not isinstance(self.prompt, str):
                self.prompt = self.prompt.__str__()

        if not isinstance(self.prompt, str):
            self.prompt = self.prompt.__str__()

        if not req.input:
            ussd_screen = dict(
                name=self.__class__.__name__,
                start=datetime.datetime.now(),
                screen_text=self.prompt
            )
            req.session['steps'].append(ussd_screen)
            return UssdResponse(self.prompt)
        else:
            req.input = req.input.split('*')[-1]
            validated_input = req.input
            if hasattr(self, 'validate'):
                try:
                    validated_input = self.validate(req.input) or req.input
                except ValidationError as e:
                    return UssdResponse(e.messages.pop())

            req.session[self.session_key] = validated_input
            req.session['steps'][-1].update(
                end=datetime.datetime.now(),
                selection=req.input
            )
            return req.forward(self.next_handler)


class MenuOption(object):
    """
    Holds text for a menu option, and the name of the corresponding
    handler.
    """

    def __init__(self, text, handler, input_text=None, input_value=None):
        """
        MenuOptions are used to be displayed in menus and lists

        By default all options are arranged in numbers and those numbers are the inputs
        example:
                this MenuOptions:
                    MenuOption('One', 'One')
                    MenuOption('Two', 'Two')

                would be displayed as follows:
                    1. One
                    2. Two

                    and the options become 1 and 2

                To use you customize options you are suppose to give the input_txt parameter

                Example :
                    MenuOption('One', 'One')
                    MenuOption('Back', 'Back', '*')

                and it will be displayed as this
                    1. One
                    *. Back

                    and the options become 1 and *
        :param text: text to be displayed on screen
        :param handler: the handle to be selected when option is selected
        :param input_txt: input to display for option
        """
        self.text = text
        self.handler = handler
        self.input_text = input_text
        self.input_value = input_value or input_text


class Menu(Handler):
    """
    A handler that asks the user to choose between actions.

    Required attributes:

    prompt        A string to display above the choices
    options       A list or tuple of MenuOptions

    Optional attributes:

    error_prompt  A string to display if an invalid choice is made
    """
    __required_attrs__ = ('prompt', 'options')
    error_prompt = _('Please enter a valid choice.\n')

    def get_error_prompt(self, req):
        lang = req.session.get('language', 'en')
        if lang == 'sw':
            return 'Tafadhali ingiza taarifa sahihi.\n'
        else:
            return self.error_prompt

    def handle(self, req):
        # Replace prompt with text if it is callable
        if hasattr(self, 'get_prompt'):
            self.prompt = self.get_prompt(req)

        if hasattr(self, 'get_options'):
            self.options = list(self.get_options(req))

        option_text = ''
        for i, o in enumerate(self.options):
            input_text = o.input_text or "%s."%(i+1,)
            if isinstance(o.text, str):
                option_text += '%s %s\n' % (input_text, o.text)
            else:
                option_text += '%s %s\n' % (input_text, o.text.__str__())

        if not req.input:
            ussd_screen = dict(
                name=self.__class__.__name__,
                start=datetime.datetime.now(),
                screen_text=self.prompt + option_text
            )
            req.session['steps'].append(ussd_screen)
            return UssdResponse(self.prompt + option_text)
        else:
            if req.input != '*':
                req.input = req.input.split('*')[-1]
            try:
                if req.input.isdigit():
                    option = self.get_option(self.options, int(req.input)-1)
                else:
                    option = self.get_option(self.options, req.input)
                req.session['steps'][-1].update(
                    end=datetime.datetime.now(),
                    selection=req.input
                )
                return req.forward(option.handler)
            except (ValueError, IndexError):
                prompt = self.prompt
                if hasattr(self, 'get_error_prompt'):
                    prompt = self.get_error_prompt(req)
                return UssdResponse(prompt + option_text)
                

class ListItem(object):
    """Holds an item in a List handler"""

    def __init__(self, text, value):
        self.text = text
        self.value = value

    def __eq__(self, other):
        return (self.text == other.text) and (self.value == other.value)

    def __str__(self):
        return "{0} {1}".format(self.text, self.value)


class List(Handler):
    """
    A handler that asks the user to choose an item from a
    list. Provides pagination.

    Required attributes:

    prompt          A string to display above the items
    session_key     Key under which to save chosen item's value
    items_per_page  Number of items to show per page
    next_handler    Handler to forward to after selection


    Optional attributes:

    error_prompt    String to display if an invalid choice is made
    items           A list or tuple of ListItems
    get_items       Method returning a list or tuple of ListItems. 
                    Is an alternative to items.
    options         A list or tuple of MenuOptions to display 
                    after the items.
    """

    __required_attrs__ = ('prompt', 'session_key', 'items_per_page', 
                          'next_handler')
    error_prompt = _('Please enter a valid choice.\n')

    def handle(self, req):

        # Replace prompt with text if it is callable
        if hasattr(self, 'get_prompt'):
            self.prompt = self.get_prompt(req)

        prompt = self.prompt

        # Call item getter if one exists
        if hasattr(self, 'get_items'):
            self.items = list(self.get_items(req))

        if hasattr(self, 'get_options'):
            self.options = list(self.get_options(req))

        # Adjust prompt if item list is empty
        if len(self.items) == 0:
            prompt = 'No items found.\n'
            if hasattr(self, 'empty_prompt'):
                prompt = self.empty_prompt

        paginator = Paginator(self.items, self.items_per_page)
        if not req.input:
            # Set page number for future requests
            req.session['_ussd_state']['page'] = 1
            page = paginator.page(1)
            # Render first page of items
            response = prompt + self._render(page)
            ussd_screen = dict(
                name=self.__class__.__name__,
                start=datetime.datetime.now(),
                screen_text=response
            )
            req.session['steps'].append(ussd_screen)
            return UssdResponse(response)
        else:
            if req.input != '*':
                req.input = req.input.split('*')[-1]
            page = paginator.page(req.session['_ussd_state']['page'])
            try:
                # Handle customized menu option input
                if not req.input.isdigit():
                    if hasattr(self, 'options'):
                        option = self.get_option(self.options, req.input)
                        req.session['steps'][-1].update(
                            end=datetime.datetime.now(),
                            selection=req.input
                        )
                        return req.forward(option.handler)
                    else:
                        raise IndexError('No such option')

                # Handle valid input
                selection = int(req.input)
                if page.start_index() <= selection <= page.end_index():
                    # Handle straightforward selection
                    item_value = self.items[selection-1].value
                    req.session[self.session_key] = item_value
                    req.session['steps'][-1].update(
                        end=datetime.datetime.now(),
                        selection=req.input
                    )
                    return req.forward(self.next_handler)
                else:
                    # Handle extras
                    more_index = page.end_index() + 1
                    if page.has_next() and selection == more_index:
                        new_page_number = page.next_page_number()
                        req.session['_ussd_state']['page'] = new_page_number
                        new_page = paginator.page(new_page_number)
                        return UssdResponse(prompt + self._render(new_page))
                    elif hasattr(self, 'options'):
                        opt_start_index = page.end_index() + 1
                        if page.has_next():
                            # Skip 'More'
                            opt_start_index += 1
                        opt_end_index = opt_start_index + len(self.options) - 1
                        if opt_start_index <= selection <= opt_end_index:
                            option = self.options[selection - opt_start_index]
                            req.session['steps'][-1].update(
                                end=datetime.datetime.now(),
                                selection=req.input
                            )
                            return req.forward(option.handler)
                        else:
                            raise IndexError('No such option')
                    else:
                        # Input was out of range
                        raise IndexError('No such item')
            except (ValueError, IndexError):
                # Re-display and ask for valid input
                prompt = _('Please enter a valid choice.\n')
                if hasattr(self, 'error_prompt'):
                    prompt = self.error_prompt
                return UssdResponse(prompt + self._render(page))

    def _render(self, page):
        """
        Takes a Django page object. Renders the items on the page,
        adding navigation options.
        """
        lines = []
        for (i, o) in enumerate(page.object_list, page.start_index()):
            if isinstance(o.text, str):
                lines.append("{0}. {1}".format(i, o.text))
            else:
                lines.append("{0}. {1}".format(i, o.text.__str__()))

        templates = []

        # options should start after the end of items
        start = page.end_index() + 1
        if page.has_next():
            templates.append('%d. %s'%(start, _('More')))
            start += 1
        if hasattr(self, 'options'):
            for i, o in enumerate(self.options, start):
                input_text = o.input_text or "%s."%(i,)
                if isinstance(o.text, str):
                    templates.append('%s %s\n'%(input_text, o.text))
                else:
                    templates.append('%s %s\n'%(input_text, o.text.__str__()))
        lines.extend(templates)

        return '\n'.join(lines)


class Quit(Handler):
    """Handler that displays a message and terminates the session."""

    __required_attrs__ = 'message'

    timestamp = datetime.datetime.now()

    def handle(self, req):
        if hasattr(self, 'get_message'):
            self.message = self.get_message(req)
            if not isinstance(self.message, str):  # force translation of proxy object
                self.message = self.message.__str__()

        if not isinstance(self.message, str):  # force translation of proxy object
            self.message = self.message.__str__()
        ussd_screen = dict(
            name=self.__class__.__name__,
            start=self.timestamp,
            end=self.timestamp,
            selection="",
            screen_text=self.message
        )
        req.session['steps'].append(ussd_screen)
        return UssdResponse(self.message, status=False)
