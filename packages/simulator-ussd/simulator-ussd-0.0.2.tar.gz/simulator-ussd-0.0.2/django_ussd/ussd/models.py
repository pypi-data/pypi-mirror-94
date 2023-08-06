"""
The idea of model is to use database to save screens in the db so that
product owner can be able to change ussd screens via django admin

The lookup should be exposed to the product owner

Types of screen that the product owner:
    1. Menu (contains only options)
        - Contains the title of the screen
        - Options to be displayed
        -


"""

from django.db import models
from jsonfield import JSONField
from django.core.exceptions import ValidationError
from python_field.fields import PythonCodeField

class ListItems(models.Model):
    """
    This will be used by ussd handlers to display items

    It requires:
        - text : text to be used to display the items
        - value: what to save once the user selects the item
    """
    text = models.ManyToManyField('Translation')

    # to be used to fetch iterable object in menu lookup
    iterable = models.CharField(max_length=100)

    # value to be used to represent what the user is shown
    value = models.CharField(max_length=50)

    def __unicode__(self):
        return "Text: {0} iterable: {1}".format(self.text, self.iterable)

    class Meta:
        verbose_name = "ListItems"
        verbose_name_plural = "ListItems"

class MenuOptions(models.Model):
    """
    This are the menu options that will be displayed to the user:
        1. name -> this is the text that is going to be displayed
        2. ussd_handler -> this used to call the
    """
    text = models.ManyToManyField('Translation', related_name='menu_text')
    next_handler = models.ForeignKey('UssdHandler', related_name='menuoptions_next_handler',
                                     blank=True, null=True
                                     )
    plugin = models.OneToOneField("PluginHandler", blank=True, null=True)

    ussd_handler = models.ForeignKey('UssdHandler')

    # menu options would be sorted by this field
    index = models.IntegerField()

    in_put = models.CharField(verbose_name="input_to_display", max_length=50, blank=True, null=True)

    in_put_value = models.CharField(verbose_name="input_to_be_selected", max_length=50, blank=True, null=True)

    def __str__(self):
        return "Name: {0} \nNext_handler: {1}  \nScreen: {2}".format(self.text, str(self.next_handler), str(self.ussd_handler))

    class Meta:
        verbose_name = "MenuOptions"
        verbose_name_plural = "MenuOptions"
        unique_together = ("index", "ussd_handler", "in_put")


    def clean(self):
        super(MenuOptions, self).clean()

        if self.next_handler is None and self.plugin is None:
            raise ValidationError({'next_handler': 'next_handler or next_custom_handler '
                                                   'should be defined'})

        if self.in_put_value is None or self.in_put_value == '':
            self.in_put_value = self.in_put or self.index
        if self.in_put is None or self.in_put == '':
            self.in_put = "{}. ".format(self.index)

    def save(self, *args, **kwargs):
        self.clean()
        super(MenuOptions, self).save(*args, **kwargs)


class HttpRequest(models.Model):
    post, get = 'post', 'get'
    http_methods = (
        (post, post),
        (get, get),
    )

    url = models.CharField(max_length=100)
    params = JSONField(default={}, blank=True, null=True)
    method = models.CharField(max_length=100,
                              choices=http_methods)
    headers = JSONField(default={}, blank=True, null=True)

    name = models.CharField(max_length=100)


class UssdHandler(models.Model):
    """
    This stores all the screens to be stored.

    There are three types of screen:
        1. Input screen
                Its a screen with just a text and an input field

                To create this type of screen:
                        - Title -> Its the text to be displayed
                        - Menu options should be null
                        - List items should be null
                        - Should state the session_key ( this is where the user input should be stored)
                        - Session state should be True ( since the session is still in progress)
                        - next_handler -> this is the next screen to be displayed after user enters the input

        2. Menu screen
            Its a screen with a title and menus from which user can select

            To create this type of screen:
                - Title -> title to be displayed to the user
                - Menu options ->  should not be null
                - Session state -> should be True since the session is still in progress

            next_handler -> is not required since the next screen is determined by the menu options
            list items  -> is not required since you are only displaying menus

        3. List screen
            Its a screen with a title and items for user to select it can also have menus

            To create this type of screen:
                - Title -> title to be displayed to the user
                - List items -> items to be listed to the user
                - Menu option -> options for user to select from
                - session_key -> to store the item the user has selected
                - next handler -> to display the next screen if the user selects one of the items
                - session_state -> should be True, since the session is still continuing
        4. Quit screen
            Its a screen with a text only and it terminates the session

            To create this type of screen :
                - Title -> title to be displayed to the user
                - session_state -> should be False to terminate the session

        5. Router screens
            It routes ussd request to other ussd handler

            To create this type of screen
                - all fields should be null apart from the name
                - create UssdRouterHandler object that reference to this handler

    """
    name = models.CharField(max_length=100, unique=True)
    text = models.ManyToManyField('Translation', blank=True, related_name='screen_text')
    session_key = models.CharField(max_length=50, null=True, blank=True)

    # name of the field that contains the items
    list_items = models.OneToOneField(ListItems, null=True, blank=True)

    session_state = models.BooleanField(default=True)

    next_handler = models.ForeignKey('self', null=True, blank=True)

    plugin = models.OneToOneField("PluginHandler", blank=True, null=True)

    http_request = models.ForeignKey(HttpRequest,
                                   related_name='http_request',
                                   null=True,
                                   blank=True
                                   )

    def __str__(self):
        return self.name

    # def clean(self):
    #     super(UssdHandler, self).clean()
    #
    #     menu_options = MenuOptions.objects.filter(ussd_handler=self)
    #     # if its input screen either next_handler or next_custom_handler is defined
    #     if (self.list_items is None) and (len(menu_options) == 0) and self.session_state and self.text.all():
    #         if (self.next_handler is None) and (self.plugin is None):
    #             raise ValidationError("Input screen {} should have atleast next_handler or "
    #                                    "next_custom_handler".format(self.name))
    #
    #     # it its a list item then next_handler or custom handler is defined
    #     elif (self.list_items is not None) and self.session_state and self.text.all():
    #         if (self.next_handler is None) and (self.plugin is None):
    #             raise ValidationError("List screen should have atleast next_handler or "
    #                                    "next_custom_handler")

class UssdRouterHandler(models.Model):
    """
    Its used to forward ussd request to ussd handler depending on the expression
    """
    ussd_handler = models.ForeignKey("UssdHandler", related_name="ussd_screen")
    next_handler = models.ForeignKey("UssdHandler")
    expression = models.CharField(max_length=500)
    index = models.IntegerField()

    def __unicode__(self):
        return "Router: {0} screen: {1} status: {2}".format(self.ussd_router, self.ussd_handler, self.status)

    class Meta:
        ordering = ['index']

class UssdHandlerFlag(models.Model):
    name = models.CharField(max_length=100)
    ussd_handler = models.ForeignKey(UssdHandler)
    new_feature = models.ForeignKey(UssdHandler, related_name='ussd_handler_flag_new_features')


class PluginHandler(models.Model):
    """
    This is used to redirect ussd traffic from model handlers to
    class handlers (plugin handler)

    You define a plugin (a class handler that ussd traffic is going to
    be routed to)

    """
    # this is used by ussd handler model to redirect
    #  traffic to class Ussdhandlers
    plugin = models.CharField(max_length=255)
    # this is to be used by plugin to redirect traffic back to models
    next_handler = models.ForeignKey("UssdHandler")


class Widget(models.Model):
    logic = PythonCodeField()
    description = models.TextField(blank=True, null=True)


class Translation(models.Model):
    language = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return "({0}){1}".format(self.language, self.text)

# todo: functionality to validate user input and respond with error message
# todo: functionality for language translation
# todo:  add a way to save session steps

