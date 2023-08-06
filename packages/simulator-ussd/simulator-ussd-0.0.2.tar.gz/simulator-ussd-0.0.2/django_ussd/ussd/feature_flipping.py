__author__ = 'Mwaaas'
__email__ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'


"""
This implements feature flipping in ussd screens handled by model
"""

from .models import *

def create_ussd_handler_flag(flag_name, ussd_handler):
    """
    Creation of flag is done by the following steps:
    ===================================================

    - This creates a another ussd_handler record with the name of the
    handler changed to {{flag_name:ussd_handler.name}}

    - If the ussd_handler has menu options
    create the same menu options for  the handler created in step one

    - create ussd_handler_flag record with ussd_handler as the
    provided in the parameter and the new feature as the ussd_handler created
    in step one

    :param flag_name: name of the flag (str)
    :param ussd_handler: screen to apply feature flipping (UssdHandler instance)
    :return:
    """
    # create a ussd handler with the flag_name appended
    new_feature_handler = UssdHandler.objects.create(
        name="{}:{}".format(flag_name, ussd_handler.name),
        title=ussd_handler.title,
        session_key=ussd_handler.session_key,
        list_items=ussd_handler.list_items,
        session_state=ussd_handler.session_state,
        next_handler=ussd_handler.next_handler,
        submission=ussd_handler.submission
    )

    menu_options = MenuOptions.objects.filter(ussd_handler=ussd_handler)
    for menus in menu_options:
        MenuOptions.objects.create(
            name=menus.name,
            next_handler=menus.next_handler,
            next_custom_handler=menus.next_custom_handler,
            ussd_handler=new_feature_handler,
            index=menus.index,
        )


