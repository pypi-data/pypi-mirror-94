from django.conf.urls import patterns, include, url
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'ussd_handler', views.UssdHandlerView)
router.register(r'menu_handler', views.MenuHandlerView)

urlpatterns = patterns(
    '',
    url(r'ussd_journey', views.UssdJourney.as_view(),
        name='ussd_journey'),
    url(r'type_of_ussd', views.TypeOfUssd.as_view(),
        name='type_of_ussd'),
    url('', include(router.urls)),
    url('root/', views.ApiRoot.as_view())
)
