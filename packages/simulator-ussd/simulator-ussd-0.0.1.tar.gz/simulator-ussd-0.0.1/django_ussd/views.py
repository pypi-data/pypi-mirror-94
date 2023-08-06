from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .ussd.core import UssdAppModelView, UssdRequest, UssdResponse
from .ussd.handlers import Handler
from .http.views import UssdSimulatorView
import json

class AirtelKeUssdViewV1(UssdAppModelView):
    initial_handler = "Ke_initial_screen"

    def post(self, req):
        return UssdRequest(phone_number=req.POST['phoneNumber'].strip('+'),
                                   session_id=req.POST['sessionId'],
                                   input_=req.POST['text'],
                                   service_code=req.POST['serviceCode']
                                )

    def ussd_response_handler(self, ussd_response):
        if ussd_response.status:
            return HttpResponse('CON' + ' '+str(ussd_response))
        return HttpResponse('STOP' + ' ' + str(ussd_response))


class AirtelKeUssdSimulatorV1(UssdSimulatorView):
    ussd_view = AirtelKeUssdViewV1
    ussd_view_url_name = 'airtel_ke_dispatch_v1'

    def parse_response(self, raw_str):
        response_status, response_message = raw_str.split(' ', 1)
        return response_status, response_message

    def response_handler(self, response):
        response_status, response_message = self.parse_response(response.content.decode())
        if response_status == 'CON':
            status = True
        else:
            status = False

        return status, response_message

@csrf_exempt
def mock_json_1_api(req, msisdn):
    status = 200
    res = {
        'UID': "19412h12h2h1414hji4h4h",
        'GUID': "89214h21h41xuhruf1y4u4",
        'maximum_loan_amount' :"20000",
        'maximum_loan_duration': "30",
        'message': ""
    }

    if msisdn == '200':
        res["loan_increments"] = [500, 750]
        res["repayment_amounts"] = {"14": {"750": 878, "500": 585}, "7": {"750": 852, "500": 568}}
        res["durations_for_amount"] = {"750": {"14": 878, "7": 852}, "500": {"14": 585, "7": 568}}
        res["duration_increments"] = [7, 14]
        status = 200
    elif msisdn == '404': #needs to optin
        status = 404
    elif msisdn == '423': #user with a loan
        status = 423
        res['message'] = "Have an outstanding loan"
    elif msisdn == '42':
        raise TimeoutError()
    else:
        status = 403
    return HttpResponse(json.dumps(res), status=status)

@csrf_exempt
def mock_json_2_api(req):
    response = HttpResponse()
    response.status_code = 204

    return response

class PinValidation(Handler):

    def handle(self, req):
        self.next_handler = req.session['_ussd_state']['next_model_handler']

        # get pin
        pin = req.session.get('pin')

        validate = RegexValidator(regex=r'^[0-9]{1,4}$', message='Not a valid PIN. Please enter your Airtel Money PIN')

        try:
            validate(pin)
        except ValidationError as e:
            return UssdResponse(e.messages.pop())

        return req.forward(self.next_handler)