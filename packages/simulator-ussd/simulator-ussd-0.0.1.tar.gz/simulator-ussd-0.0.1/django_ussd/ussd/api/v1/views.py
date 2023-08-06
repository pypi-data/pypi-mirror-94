from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from ...core import get_ussd_workflow, UssdAppModelView
from structlog import get_logger
from .serializers import *
from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse

# todo this api nees a testcase
class UssdJourney(APIView):
    def get(self, req):
        query_params = req.query_params
        logger = get_logger(__name__).bind(
            action='ussd_journey'
        )
        logger.info('request', data=query_params)
        try:
            ussd_handler = query_params['ussd_handler']
            logger.info('ussd_handler',
                        ussd_handler=ussd_handler)

            ussd_journey = get_ussd_workflow(
                query_params['ussd_handler']
            )
            status_code = status.HTTP_200_OK
            logger.info('response',
                        data=ussd_journey,
                        status=status_code
                        )
            return Response(data=ussd_journey,
                            status=status_code)
        except KeyError:
            msg = "invalid ussd handler"
            status_code = status.HTTP_400_BAD_REQUEST
            logger.info('error_response', data=msg,
                        status=status_code
                        )
            return Response(data=msg,
                            status=status_code)


class TypeOfUssd(APIView):

    def get(self, req):
        ussd_handler = req.query_params.get('ussd_handler')

        if ussd_handler:
            ussd_handler = get_object_or_None(UssdHandler,
                                              name=ussd_handler)
            if ussd_handler:
                type_of_ussd = UssdAppModelView().type_of_ussd_handler(ussd_handler)

                return Response(status=status.HTTP_200_OK, data=type_of_ussd)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class UssdHandlerView(viewsets.ModelViewSet):

    queryset = UssdHandler.objects.all()
    serializer_class = UssdHandlerSerializer


class MenuHandlerView(viewsets.ModelViewSet):
    queryset = MenuOptions.objects.all()
    serializer_class = MenuHandlerSerializer


class ApiRoot(APIView):
    def get(self, req):
        return Response(
                {
                    "ussd_journey": reverse('ussd_journey'),
                    "type_of_ussd": reverse('type_of_ussd'),
                }
        )
