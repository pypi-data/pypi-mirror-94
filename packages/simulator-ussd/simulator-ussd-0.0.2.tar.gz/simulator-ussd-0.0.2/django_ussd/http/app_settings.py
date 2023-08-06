__author__ = 'mwas'
__created_date__ = '3/20/15'
__email___ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'


import requests

# making a ussd request
def default_ussd_request(session_data, user_input):
    """
    given session data we make a ussd request and return a response
    :param session_data:
    :return: Response
    """
    data = {'phoneNumber': session_data['phone_number'],
            'sessionId': session_data.get('session_id'),
            'text': user_input,
            'serviceCode': ''}
    return requests.post(session_data['service_url'], data=data)



# parsing ussd request
def default_ussd_response_parser(response):
    """
    takes ussd response and parse the response
    returns an tuple containing state and messate
            state -> indicates whether the ussd session is in progress or its done
            message -> displays the ussd message
    :param response:
    :return: tuple with two objects
    """
    message = response.content
    status = response.headers.get('status')
    return status, message


USSD_DISPATCH_URL_NAME = 'ussd:dispatch'
USSD_SIMULATOR_REQUEST_HANDLER = default_ussd_request
USSD_SIMULATOR_RESPONSE_HANDLER = default_ussd_response_parser
USSD_CONTINUE_SYMBOL = 'CON'