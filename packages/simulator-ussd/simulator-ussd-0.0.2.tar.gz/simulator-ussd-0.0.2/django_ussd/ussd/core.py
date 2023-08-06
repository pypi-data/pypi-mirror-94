from structlog import get_logger

from django.contrib.sessions.backends.db import SessionStore as DjangoSessionStore
from django.http import HttpResponse
from copy import copy
from urllib.parse import unquote
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import UssdRouterHandler, MenuOptions, ListItems, UssdHandler, PluginHandler, HttpRequest
from ..ussd_template.template_engine import UssdTemplate
from datetime import datetime
import json
from collections import OrderedDict
from jinja2 import Environment
from annoying.functions import get_object_or_None
from waffle import *

logger = get_logger(__name__)

_handlers = {}

import os

class UssdRequest(object):
    """Represents a USSD request"""
    def __init__(self, phone_number, session_id, input_, session=None, language=None, **kwargs):
        self.phone_number  = phone_number
        self.session_id    = session_id
        self.input = unquote(input_)
        self.session       = session
        self.language = language
        self.extra_params = kwargs or {}

    def forward(self, handler_name):
        """
        Forwards a copy of the current request to a new
        handler. Clears any input, as it is assumed this was meant for
        the previous handler. If you need to pass info between
        handlers, do it through the USSD session.
        """
        new_request = copy(self)
        new_request.input = ''
        return new_request, handler_name


class UssdResponse(object):
    """Represents a USSD response"""
    def __init__(self, text, level=2, status=True, session=None, **kwargs):
        self.text = text
        self.level = level
        self.status = status
        self.session = session
        self.kwargs = kwargs

    def dumps(self):
        return self.text

    def __str__(self):
        return self.dumps()

class UssdAppViewMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        """
        Store the original class on the view function.

        This allows us to discover information about the view when we do URL
        reverse lookups.  Used for breadcrumb generation.
        """
        view = super(APIView, cls).as_view(**initkwargs)
        view.cls = cls
        # Note: session based authentication is explicitly CSRF validated,and
        # all other authentication is CSRF exempt.
        return csrf_exempt(view)


class UssdAppView(APIView):
    """
    Its a view for ussd handlers
    takes requests and convert it to ussd_request and then process the ussd
    takes ussd_requests and finish by converting ussd_response to http response
    """

    def dispatch(self, request, *args, **kwargs):
        """
          `.dispatch() ' is pretty much the same as rest framework dispatch but with extra hooks
          to enable ussd handlers functionality
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        # make sure all attributes required by ussd are provided
        self.ussd_initials()

        # initialize ussd requirements
        #self.initial_handler = self.initial_handler
        self.initial_input = getattr(self, 'initial_input', None)
        self.initial_level = getattr(self, 'initial_level', 1)

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            ussd_request = handler(request, *args, **kwargs)

            if isinstance(ussd_request, HttpResponse):
                return ussd_request

            if not isinstance(ussd_request, UssdRequest) and not isinstance(ussd_request, Exception):
                raise TypeError("{0} should return an instance of {1}".
                    format(request.method.lower(), UssdRequest.__name__))

            if isinstance(ussd_request, UssdRequest):
                session = SessionStore(session_key=ussd_request.session_id)
                ussd_request.session = session
                ussd_response = self.ussd_dispatcher(ussd_request)
                response = self.ussd_response_handler(ussd_response)
            else:
                response = ussd_request
        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def ussd_dispatcher(self, ussd_request):
        """
        Takes an incoming HTTP request, converts it into a USSD
        request, and invokes _run_handlers on it. Converts the
        resulting USSD response into a HttpResponse and returns it.
        """
        self.logger = get_logger(__name__)

        self.logger = self.logger.bind(phone_number=ussd_request.phone_number,
                             session_id=ussd_request.session_id,
                                       extra_params=ussd_request.extra_params
                                       )

        self.logger.debug('gateway_request', text=ussd_request.input)
        # Clear input and initialize session if we are starting up
        if '_ussd_state' not in ussd_request.session:
            ussd_request.input = ''
            ussd_request.session['_ussd_state'] = {'next_handler': self.initial_handler}
            ussd_request.session['steps'] = []
            ussd_request.session['posted'] = False
            ussd_request.session['session_id'] = ussd_request.session_id
            ussd_request.session['phone_number'] = ussd_request.phone_number
            ussd_request.session['start_of_screen'] = True
            ussd_request.session['language'] = ussd_request.language
            ussd_request.session.update(ussd_request.extra_params)

            # this indicates its the first time we are handling the session
            ussd_request.session["start_of_session"] = True

        # Invoke handlers
        ussd_response = self.run_handlers(ussd_request)

        # we have already handled the first session
        ussd_request.session["start_of_session"] = False

        # Save session
        ussd_request.session.save()

        self.logger.debug('gateway_response', text=ussd_response.dumps())

        # Construct HTTP response
        # use response handle if one if provided in th"e settings
        return ussd_response

    def ussd_initials(self):
        from .handlers import MissingAttribute

        if not hasattr(self, 'initial_handler'):
            raise MissingAttribute("Missing initial_handler  attribute in {}".format(self.__class__))

        # if not issubclass(self.ussd_response_handler, UssdResponseHandlerBaseClass):
        #     raise Exception("ussd response handler should be a subclass of {}".format(UssdResponseHandlerBaseClass.__name__))

    def run_handlers(self, ussd_request):
        """
        Implements the core of the dispatch process. Takes a ussd
        request. Invokes USSD handlers and returns a final ussd response.
        """
        # Handle the request
        handler = ussd_request.session['_ussd_state']['next_handler']
        result = _handlers[handler].handle(ussd_request)

        # Handle any forwarded Requests; loop until a Response is
        # eventually returned.
        while not isinstance(result, UssdResponse):
            new_ussd_request, handler = result
            result = _handlers[handler].handle(new_ussd_request)

        ussd_response = result

        # Whichever handler responded should handle the next request
        ussd_request.session['_ussd_state']['next_handler'] = handler

        # Attach session to outgoing response
        ussd_response.session = ussd_request.session

        return ussd_response

    def ussd_response_handler(self, ussd_response):
        return HttpResponse(str(ussd_response))

    def simulator_handler(self, req):
        return UssdRequest(req.GET['phoneNumber'],
                       req.GET['sessionId'],
                       req.GET['text'],
                       req.GET.get('LANGUAGE', 'en'),
                       )


class TypesOfUssdScreens(object):
    input_screen='input_screen'
    menu_screen='menu_screen'
    list_screen='list_screen'
    menu_list_screen = 'menu_list_screen'
    quit = 'quit_screen'
    router = 'router_screen'


class UssdAppModelView(UssdAppView):
    """
    A view implementing ussd screens using model method should inherit this class

    Ussd view used to handle ussd screens from models

    A class overriding this class should have the following requirements:
            1. ussd_router
                This is a UssdRouter record. Its used to route ussd request
                to Ussd handler depending on the status provided in
                menu lookup

            2. lookup_url
                Its used for menu lookup

    The class should also implement get or post method that returns
    UssdRequest

    # Workflow
    - Gets lookup_url and make the request to get menu lookup
      the lookup results should have status parameter

    - With status in menu lookup find the fist ussd handler in ussd_router
      that is given as an attribute

    - Once we have the first ussd handler navigate to the next screens
      depending with what has been defined

    # check the type of ussd handlers (ussd screens) in UssdHandler model doc-string

    """

    def do_menu_lookup(self, ussd_request):
        """
        it does menu lookup if it han't been done already

        :return dict result of menu lookup
        """
        logger = get_logger(__name__).bind(
            phone_number=ussd_request.phone_number,
            session_id=ussd_request.session_id
        )
        logger.info('menu_lookup')
        if not ussd_request.session.get('menu_lookup', False):
            url = '{0}{1}'.format(self.lookup_url, ussd_request.phone_number)
            logger.info('menu_lookup_request', url=url)
            response_ = requests.get(url, headers={'Content-Type': 'application/json'})

            results = json.loads(response_.content.decode(), object_pairs_hook=OrderedDict)

            logger.info('menu_lookup_response', data=results, status_code=response_.status_code)

            ussd_request.session['menu_lookup'] = True
            ussd_request.session.update(results)
            ussd_request.session.save()
            logger.info('menu_lookup_initial_handler', initial_handler=self.initial_handler)

        logger.info('menu_lookup_already_done')

    def run_handlers(self, ussd_request):

        # initialize ussd variables
        self.ussd_request = ussd_request
        next_handler = self.get_next_hanldler()

        # check if next handler is custom handler
        if "custom:" in next_handler:
            self.ussd_request.session['start_of_screen'] = True
            self.set_next_handler(next_handler.split(":")[1])
            return self.run__custom_handlers()

        self.ussd_handler = UssdHandler.objects.get(name=next_handler)

        # populate interaction
        ussd_response = self.respond_to_input()

        if self.ussd_request.session['start_of_screen']:
            self._record_new_screen(ussd_response)
        else:
            # update the previous screen in steps
            self._update_previous_screen()

            # then add this new screen to steps
            self._record_new_screen(ussd_response)

        return ussd_response

    def run__custom_handlers(self):
        """
        Implements the core of the dispatch process. Takes a ussd
        request. Invokes USSD handlers and returns a final ussd response.
        """
        # Handle the request
        handler = self.get_next_hanldler()
        result = _handlers[handler].handle(self.ussd_request)

        # Handle any forwarded Requests; loop until a Response is
        # eventually returned.
        while not isinstance(result, UssdResponse):
            self.ussd_request, handler = result

            # if handler is a model ussd to be handled by model ussd logistics
            if "model:" in handler:
                self.set_next_handler(handler.split(":")[1])
                return self.run_handlers(self.ussd_request)

            result = _handlers[handler].handle(self.ussd_request)

        ussd_response = result

        # Whichever handler responded should handle the next request
        self.set_next_handler("custom:{}".format(handler))

        # Attach session to outgoing response
        ussd_response.session = self.ussd_request.session

        return ussd_response

    def set_next_handler(self, next_handler_name):
        self.ussd_request.session['_ussd_state']['next_handler'] = next_handler_name

    def get_next_hanldler(self):
        return self.ussd_request.session['_ussd_state']['next_handler']

    def set_next_model_handler(self, next_handler_name):
        self.ussd_request.session['_ussd_state']['next_model_handler'] = \
            "model:{}".format(next_handler_name)

    def get_next_model_handler(self):
        return self.ussd_request.session['_ussd_state']['next_model_handler']

    def respond_to_input(self):
        # if its the first time we are handling the session
        if self.ussd_request.session['start_of_session']:
            return self.create_ussd_response(self.ussd_handler)

        menu_options = MenuOptions.objects.filter(ussd_handler=self.ussd_handler)

        type_of_screen = self.type_of_ussd_handler(self.ussd_handler)

        # if its a quit screen or router screen render the ussd
        if type_of_screen in (TypesOfUssdScreens.quit, TypesOfUssdScreens.router):
            return self.create_ussd_response(self.ussd_handler)
        elif type_of_screen == TypesOfUssdScreens.input_screen:
            self.ussd_request.session[self.ussd_handler.session_key] = self.ussd_request.input
            if self.ussd_handler.next_handler:
                return self.create_ussd_response(self.ussd_handler.next_handler)
            return self.create_ussd_response(self.ussd_handler.plugin)
        # if its menu screen
        elif type_of_screen == TypesOfUssdScreens.menu_screen:
            option_selected = self.get_selected_menu(
                menu_options,
                self.ussd_request.input
            )
            # if input was valid
            # create ussd response for next handler
            if option_selected:
                return self.create_ussd_response(option_selected)
            # Return invalid message with the same menus
            return self.create_ussd_response(self.ussd_handler)

        # if its list screen
        elif type_of_screen == TypesOfUssdScreens.list_screen:
            validated_input = self.get_selected_list(self.ussd_handler.list_items,
                                                     self.ussd_request.input)
            if validated_input:
                # save selected input in session
                self.ussd_request.session[self.ussd_handler.session_key] = validated_input.value

                if self.ussd_handler.next_handler:
                    return self.create_ussd_response(self.ussd_handler.next_handler)
                return self.create_ussd_response(self.ussd_handler.plugin)

            # Return invalid message with the same menus
            return self.create_ussd_response(self.ussd_handler)

        # if its a list/menu screen
        elif type_of_screen == TypesOfUssdScreens.menu_list_screen:
            # check if one of the list item was selected
            list_item_selected = self.get_selected_list(
                self.ussd_handler.list_items,
                self.ussd_request.input)

            if list_item_selected:
                # save selected input in session
                self.ussd_request.session[self.ussd_handler.session_key] \
                    = list_item_selected.value

                if self.ussd_handler.next_handler:
                    return self.create_ussd_response(
                        self.ussd_handler.next_handler)
                else:
                    return self.create_ussd_response(self.ussd_handler.plugin)

            # check if one of the menu was selected
            menu_item_selected = self.get_selected_menu(menu_options,
                                                        self.ussd_request.input
                                                        )

            if menu_item_selected:
                return self.create_ussd_response(menu_item_selected)

            # Return invalid message with the same menus
            return self.create_ussd_response(self.ussd_handler)

        # if its a plugin handler
        elif self.ussd_handler.plugin:
            return self.create_ussd_response(self.ussd_handler.plugin)

    def get_selected_list(self, list_items, ussd_input):
        items = self.__list_items(list_items)
        try:
            if ussd_input.isdigit():
                return items[int(ussd_input) - 1]
        except IndexError:
            pass
        return False

    def get_selected_menu(self, menuoptions, ussd_input):
        for options in menuoptions:
            if options.in_put_value.strip() == ussd_input.strip():
                if options.next_handler:
                    return options.next_handler
                return options.plugin
        return False

    def __plugin_create_ussd_response(self, ussd_handler):
            self.ussd_request.input = ''
            self.set_next_handler(ussd_handler.plugin)
            self.set_next_model_handler(ussd_handler.next_handler)
            return self.run__custom_handlers()

    def _get_text(self, obj, language):
        text = ''
        text_and_translations = obj.text.filter(language=language)
        if text_and_translations:
            return text_and_translations[0].text

        # it translation was not found
        default_text = obj.text.all()
        if default_text:
            return default_text[0].text
        return text

    def get_text(self, obj):
        return self._get_text(obj, self.ussd_request.language)

    def get_raw_text(self, ussd_handler):
        raw_text = {}
        all_text = ussd_handler.text.all()
        menu_options = MenuOptions.objects.filter(ussd_handler=ussd_handler)
        for text in all_text:
            content = {text.language: text.text}

            for menu in menu_options:
                content[text.language] += "{0}{1}\n".format(
                    menu.in_put,
                    self._get_text(menu, text.language)
                )
            raw_text.update(
                content
            )
        #import pdb; pdb.set_trace()
        return raw_text

    def create_ussd_response(self, ussd_handler):
        # ussd_handler can't be none object
        if not ussd_handler:
            raise TypeError("ussd handler should not be none")

        # is handler is a string its a custom ussd handler
        if isinstance(ussd_handler, PluginHandler):
            return self.__plugin_create_ussd_response(ussd_handler)

        # if the handler has submission then submit the ussd session
        if ussd_handler.http_request:
            self.__make_http_request(ussd_handler)

        # set next handler to the current handler
        self.set_next_handler(ussd_handler.name)

        # create title to be used
        title = UssdTemplate(self.get_text(ussd_handler),
                             self.get_session_items()).render()

        screen_name = ussd_handler.name
        # check if it has menu options
        menu_options = MenuOptions.objects.filter(ussd_handler=ussd_handler).order_by('index')

        if not title:
            if ussd_handler.plugin:
                return self.__plugin_create_ussd_response(ussd_handler.plugin)

            # router screen
            elif not title:
                return self.__forward_request(ussd_handler)

        # if its quit screen return title only
        if not ussd_handler.session_state:
            return UssdResponse(title, status=False, screen_name=screen_name)

        # if its input
        elif (not ussd_handler.list_items) and (len(menu_options) == 0):
            return UssdResponse(title, screen_name=screen_name)

        # if its menu screen
        elif not ussd_handler.list_items:
            response_text = "{0}{1}".format(title,
                                            self._create_ussd_response_for_menu_screen(menu_options))

            return UssdResponse(response_text, screen_name=screen_name)

        # if its list screen
        elif ussd_handler.list_items and (len(menu_options) == 0):
            response_text = "{0}{1}".format(title,
                                            self._create_ussd_response_for_list_screen(
                                                ussd_handler.list_items)
                                            )

            return UssdResponse(response_text, screen_name=screen_name)

        # if its a list/menu screen
        elif ussd_handler.list_items:
            response_text = "{0}{1}".format(
                title,
                self._create_ussd_response_for_list_menu_screen(
                    menu_options, ussd_handler.list_items
                )
            )

            return UssdResponse(response_text, screen_name=screen_name)

    def _create_ussd_response_for_menu_screen(self, menu_option, start_index=1):

        option_text = ''

        for i, o in enumerate(menu_option, start_index):
            option_text += "{0}{1}\n".format(o.in_put, self.get_text(o))

        option_text = UssdTemplate(option_text,
                                   self.get_session_items()
                                   ).render()
        return option_text

    def __list_items(self, list_item):
        items = UssdTemplate(self.get_text(list_item), self.get_session_items(), list_item.iterable). \
            render()
        return items

    def _create_ussd_response_for_list_screen(self, list_item, start_index=1):
        items = self.__list_items(list_item)

        list_text = ''
        for i, o in enumerate(items, start_index):
            input_text = "{}.".format(i)
            list_text += "{0} {1}".format(input_text, o.text)

        return list_text

    def _create_ussd_response_for_list_menu_screen(self, menu_options, list_item):

        # list should be displayed first then the menus
        list_text = self._create_ussd_response_for_list_screen(list_item)

        # the menus index should start after the list text
        menu_text = self._create_ussd_response_for_menu_screen(menu_options,
                                                               len(self.__list_items(list_item)) + 1)

        return "{0}{1}".format(list_text, menu_text)

    def get_session_items(self):
        return dict(iter(self.ussd_request.session.items()))

    def _record_new_screen(self, ussd_response):
        ussd_screen = dict(
            name=ussd_response.kwargs.get('screen_name'),
            screen_text=ussd_response.text,
            start=datetime.now(),
            duration=None
        )
        self.ussd_request.session['steps'].append(ussd_screen)

        self.ussd_request.session['start_of_screen'] = False

    def _update_previous_screen(self):
        end_time = datetime.now()
        self.ussd_request.session['steps'][-1].update(
            end=end_time,
            selection=self.ussd_request.input,
            duration=(self.ussd_request.session['steps'][-1]['start'] - end_time).microseconds / 1000
        )
        self.ussd_request.session['start_of_screen'] = True

    def __render_text(self, text):
        return UssdTemplate(text, self.get_session_items()).render()

    def __forward_request(self, ussd_handler):
        routing_mechanisms = UssdRouterHandler.objects.filter(ussd_handler=ussd_handler)
        env = Environment()
        for router in routing_mechanisms:
            expr = env.compile_expression(router.expression)
            if expr(self.get_session_items()):
                return self.create_ussd_response(router.next_handler)

    def __make_http_request(self, ussd_handler):

        http_request_obj = ussd_handler.http_request

        url = UssdTemplate(http_request_obj.url,
                           self.get_session_items()).render()
        request_name = http_request_obj.name
        headers = http_request_obj.headers or {}
        params = http_request_obj.params or {}
        method = http_request_obj.method
        headers.update({'Content-Type': 'application/json'})

        data = UssdTemplate(str(params),
                            self.get_session_items()).render()

        self.logger.info("ussd_handler_http_request", request_name=request_name,
                         data=data, headers=headers, http_method=method,
                         url=url
                         )

        if http_request_obj.method == HttpRequest.get:
            resp = requests.get(url, params=data, headers=headers, timeout=10)
        else:
            resp = requests.post(url, data=data, headers=headers,
                                 timeout=10
                                 )
        self.logger.info("ussd_handler_http_response", request_name=request_name,
                         status_code=resp.status_code, response_body=resp.content
                         )
        try:
            data = json.loads(resp.content.decode(), object_pairs_hook=OrderedDict)
        except json.JSONDecodeError:
            data = {}
            self.logger.info("ussd_handler_error", request_name=request_name,
                             status_code=resp.status_code, response_body=resp.content
                             )

        # the response is expected to be json or empty string
        self.ussd_request.session[request_name] = {"status_code": resp.status_code}
        self.ussd_request.session[request_name].update(data)
        self.ussd_request.session.save()

    def type_of_ussd_handler(self, ussd_handler):
        # check if it has menu options
        menu_options = MenuOptions.objects.filter(ussd_handler=ussd_handler).order_by('index')

        if not ussd_handler.text.all():
            return TypesOfUssdScreens.router
        # quit screen
        elif not ussd_handler.session_state:
            return TypesOfUssdScreens.quit
        # menu screen
        elif menu_options:
            if ussd_handler.list_items:
                return TypesOfUssdScreens.menu_list_screen
            return TypesOfUssdScreens.menu_screen
        # list screen
        elif ussd_handler.list_items:
            return TypesOfUssdScreens.list_screen
        # input screen
        return TypesOfUssdScreens.input_screen



    def ussd_initials(self):
        from .handlers import MissingAttribute

        required_attr = ('initial_handler',)

        for attrb in required_attr:
            if not hasattr(self, attrb):
                raise MissingAttribute("Missing {0} attribure in {}".format(attrb,
                                                                            self.__class__
                                                                            ))

class SessionStore(DjangoSessionStore):
    """
    HACK! HACK! HACK!

    Django's built-in session store silently replaces user-provided
    session keys with autogenerated ones to prevent session fixation
    attacks. While this is a security best practice, it leaves us with
    no way to interact with cookie-less USSD gateways that do not
    offer a pass-through HTTP variable, since we have no way to send
    them our own autogenerated session key.

    This subclass is a hack that allows us to work with user-provided
    session keys. One side effect of this is that multiple session
    model objects may be created, though only one will save the actual
    updates.
    """

    def __init__(self, session_key):
        """
        Call parent init method, then save the gateway-provided
        session key.
        """
        super(SessionStore, self).__init__(session_key)
        self.user_session_key = session_key

    def save(self, *args, **kwargs):
        """
        Restore the gateway-provided session key, then call parent
        save method.
        """
        self._session_key = self.user_session_key
        super(SessionStore, self).save(*args, **kwargs)


def get_ussd_workflow(ussd_handler, language='en'):
    """
    given ussd handler it returns a all the ussd screens that follow the one provide
    :param ussd_handler:
    :return:
    """

    # get ussd handler instance
    ussd_handler = get_object_or_None(UssdHandler, name=ussd_handler)
    if not ussd_handler:
        return {"edges": {}, 'nodes': {}}

    edge, nodes = __get_ussd_workflow(ussd_handler, {}, {})
    return {"edges": edge, "nodes": nodes}


def __get_ussd_workflow(ussd_handler, workflow={}, screen_nodes={}):
    #import pdb; pdb.set_trace()
    screen_nodes.update(
        {ussd_handler.name: {"text": UssdAppModelView().get_raw_text(ussd_handler)}}
    )
    type_of_ussd = UssdAppModelView().type_of_ussd_handler(ussd_handler)
    # to avoid cyclic
    if ussd_handler.name in workflow.keys():
        return workflow, screen_nodes

    if type_of_ussd == TypesOfUssdScreens.quit:
        return {}, screen_nodes

    elif type_of_ussd in (TypesOfUssdScreens.menu_screen, TypesOfUssdScreens.menu_list_screen):
        menu_options = MenuOptions.objects.filter(ussd_handler=ussd_handler)
        for menu_option in menu_options:
            if not workflow.get(ussd_handler.name):
                workflow[ussd_handler.name] = {}
            workflow[ussd_handler.name].update(
                {menu_option.next_handler.name: {'input': menu_option.in_put_value}}
            )
            __get_ussd_workflow(menu_option.next_handler, workflow=workflow, screen_nodes=screen_nodes)
        if type_of_ussd == TypesOfUssdScreens.menu_list_screen:
            workflow[ussd_handler.name].update(
                {ussd_handler.next_handler.name: {'input': ussd_handler.session_key}}
            )
            __get_ussd_workflow(ussd_handler.next_handler, workflow=workflow, screen_nodes=screen_nodes)
    elif type_of_ussd in (TypesOfUssdScreens.input_screen,
                          TypesOfUssdScreens.list_screen,
                          TypesOfUssdScreens.menu_list_screen):
        if not workflow.get(ussd_handler.name):
            workflow[ussd_handler.name] = {}
        workflow[ussd_handler.name].update(
            {ussd_handler.next_handler.name: {'input': ussd_handler.session_key}}
        )
        __get_ussd_workflow(ussd_handler.next_handler, workflow=workflow, screen_nodes=screen_nodes)
    elif type_of_ussd == TypesOfUssdScreens.router:
        routers = UssdRouterHandler.objects.filter(ussd_handler=ussd_handler)
        for router in routers:
            if not workflow.get(ussd_handler.name):
                workflow[ussd_handler.name] = {}
            workflow[ussd_handler.name].update(
                {router.next_handler.name: {"input": router.expression}}
            )
            __get_ussd_workflow(router.next_handler, workflow=workflow, screen_nodes=screen_nodes)
    return workflow, screen_nodes
