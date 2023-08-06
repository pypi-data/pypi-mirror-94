from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
from urllib.parse import urlencode
from django.conf import settings
import random
from . import app_settings
from django.views.generic import View
import requests
from .forms import DialForm, InputForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout


class UssdSimulatorView(View):
    def __init__(self, **kwargs):
        super(UssdSimulatorView, self).__init__(**kwargs)
        self.ussd_view_url = reverse(self.ussd_view_url_name)
        self.login_required = getattr(self, 'login_required', True)

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Store the original class on the view function.

        This allows us to discover information about the view when we do URL
        reverse lookups.  Used for breadcrumb generation.
        """
        view = super(UssdSimulatorView, cls).as_view(**initkwargs)
        view.cls = cls
        return view

    def post(self, request):
        # if its a login form process the authentification
        if request.POST.get('password', False):
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                return self.get(request)

        # if login is required make sure the user is logged in
        if self.login_required and not request.user.is_authenticated():
            return self.get(request)

        # Process ussd transactions
        if not request.session.get('phone_number', False):
            return self.initiate(request)
        return self.interact(request)

    def get(self, request):
        if self.login_required:
            # if user is not logged in redirect to login form
            if not request.user.is_authenticated():
                return render_to_response('login.html', context_instance=RequestContext(request))
        # each time you do a get the session is cleared
        authenticated_user = request.session.get('_auth_user_id')
        authentication_backend = request.session.get('_auth_user_backend')
        request.session.clear()
        request.session['_auth_user_id'] = authenticated_user
        request.session['_auth_user_backend'] = authentication_backend

        absolute_url = request.build_absolute_uri(reverse(self.ussd_view_url_name))
        return render_to_response(
            'initiate.html', {'form': DialForm(initial={'service_url': absolute_url}), },
            context_instance=RequestContext(request)
        )

    def initiate(self, request):
        """Request user's phone number. This would ordinarily be provided
        by the mobile operator; we need it to correctly simulate
        interaction ."""
        data = {}
        data.update(csrf(request))

        form = DialForm(request.POST)
        if form.is_valid():
            request.session['user_type'] = form.cleaned_data['user_type']
            request.session['phone_number'] = form.cleaned_data['phone_number']
            request.session['service_url'] = form.cleaned_data['service_url']
            request.session['language'] = form.cleaned_data['language']
            request.session['session_id'] = str(random.randint(0, 1000000))
            return self.post(request)
        return self.get(request)

    def interact(self, request):
        """Accept input from user and display menus from the application"""
        data = {}
        data.update(csrf(request))

        user_input = ''
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['input']

        # Always create a new unbound form (so that previous inputs don't
        # show up in current form fields)
        form = InputForm()
        try:
            # adding functionality to unable the simulator to create ussd request
            if getattr(self, 'request_handler', False):
                response = self.request_handler(
                    phoneNumber=request.session['phone_number'],
                    sessionId=request.session.get('session_id'),
                    input=user_input,
                    serviceCode="ussdSimulator",
                    language=request.session.get('language', 'en'),
                    ussd_url=request.session['service_url'],
                    request=request
                )

            else:
                # get the data used to create ussd request
                phoneNumber = getattr(self, 'phoneNumber', 'phoneNumber')
                sessionId = getattr(self, 'session_id', 'sessionId')
                input = getattr(self, 'input', 'text')
                language = getattr(self, 'language', 'language')
                extra_args = getattr(self, 'extra_args', {})

                data = {phoneNumber: request.session['phone_number'],
                        sessionId: request.session.get('session_id'),
                        input: user_input,
                        'serviceCode': '',
                        language: request.session.get('language', 'en')
                        }
                data.update(extra_args)

                if hasattr(self.ussd_view, 'get'):
                    response = requests.get(request.session['service_url'], params=data)
                else:
                    response = requests.post(request.session['service_url'], data=data)

            if response.status_code == 500:
                return HttpResponse(response)
            status, message = self.response_handler(response)

            # status should be a boolean
            data['status'] = status
            data['message'] = message
        except ValueError:
            data['message'] = '<Invalid response from app>'
        except urllib.error.HTTPError as h:
            data['response'] = h.read()
        data['form'] = form
        data['request_url'] = request.session['service_url']
        data['post_data'] = request.session.load()
        return render_to_response('interact.html', data,
                                  context_instance=RequestContext(request))

    def response_handler(self, response):
        """
        manipulates http response and returns message and status of session in response
        :param response:
        :return:
        """
        raise NotImplementedError("This method should be implemented")
