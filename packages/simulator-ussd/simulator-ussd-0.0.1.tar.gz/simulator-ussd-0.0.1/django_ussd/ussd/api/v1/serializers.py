__author__ = 'Mwaaas'
__email__ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'

from rest_framework import serializers
from ...models import *

common_fields = ('name', 'text', 'http_request')


class Text(serializers.ModelSerializer):
    class Meta:
        model = Translation


class ListItemSerializer(serializers.ModelSerializer):
    text = Text(many=True)

    class Meta:
        model = ListItems


class UssdHandlerSerializer(serializers.ModelSerializer):
    list_items = ListItemSerializer(required=False)
    text = Text(many=True,)

    class Meta:
        model = UssdHandler

    def create(self, validated_data):
        text_data = validated_data.pop('text')

        ussd_handler = UssdHandler.objects.create(
            **validated_data
        )

        for data in text_data:
            ussd_handler.text.add(
                Translation.objects.create(**data)
            )

        return ussd_handler

class MenuHandlerSerializer(serializers.ModelSerializer):
    #next_handler = serializers.Field(source='next_handler.name')
    text = Text(many=True)

    class Meta:
        model = MenuOptions

    def create(self, validated_data):

        text_data = validated_data.pop('text')

        menu_obj = MenuOptions.objects.create(
            **validated_data
        )

        for data in text_data:
            menu_obj.text.add(
                Translation.objects.create(**data)
            )

        return menu_obj
