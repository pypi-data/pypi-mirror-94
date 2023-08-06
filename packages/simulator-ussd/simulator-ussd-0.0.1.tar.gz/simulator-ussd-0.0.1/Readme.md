
# Usage

Install
---
    $ pip install -e git+git@bitbucket.org:wezatele/django-ussd.git@0.X.x#egg=django-ussd

Usage
--------------
# Settings up UssdView
- add django_ussd in installed apps for the purpose of static files:
        django_ussd
        
- adding your first ussd view. Note the http method should return UssdRequest instead of the 
convention HttpResponse:

 
    from django_ussd.ussd.core import UssdAppView, UssdRequest
    
    class TzUssdView(UssdAppView):
        initial_handler = 'Welcome'
        initial_level = '1'
        initial_input = '30'

    def post(self, req):
        return UssdRequest(req.POST['phoneNumber'],
                           req.POST['sessionId'],
                           req.POST['text'],)

    # this is an example of a handler
    class Welcome(Menu):

        prompt = 'Choose from:\n\n'
        error_prompt = 'Please enter a valid choice.\n'

        def get_options(self, req):
            yield MenuOption('Apples', 'MenuScreen')
            yield MenuOption('Oranges', 'MenuScreen')
            yield MenuOption('Melons', 'MenuScreen')
            yield MenuOption('Back', 'MenuScreen')
            
- By default ussd response is converted to http response by this method:


    def ussd_response_handler(self, ussd_response):
        return HttpResponse(str(ussd_response))

- To  define your custom response handler override the method. eg:


    class KenyaUssdView(UssdAppView):
        initial_handler = 'Welcome'
        initial_level = '1'
        initial_input = '30'
    
        def post(self, req):
            return UssdRequest(req.POST['phoneNumber'],
                               req.POST['sessionId'],
                               req.POST['text'],)
    
        def ussd_response_handler(self, ussd_response):
            CONTINUE = 'CON'
            STOP = 'END'
            response = HttpResponse(str(ussd_response))
            freeflow_params = {CONTINUE: 'FC', STOP: 'FB'}
            response['Freeflow'] = freeflow_params[ussd_response.status]
    
            return response

        
- add url to point at your ussd view:


    url(r'^tz/ussd', TzUssdView.as_vew(), name='tz_ussd_view'),
    url(r'^ke/ussd', KenyaUssdView.as_view(), name='ke_ussd_view'),
    
    # NB: the name should be a Must if you want to have ussd simulator
    
     
# Setting up ussd Simulator

- an exmple of a simulator for KenyaUssdView written above


    class KenyaUssdSimulator(UssdSimulatorView):
        ussd_view = KenyaUssdView
        ussd_view_url_name = 'ke_ussd_view'
    
        def response_handler(self, response):
            response_status = response.headers['Freeflow']
            response_message = response.content
            if response_status == 'CON':
                status = False
            else:
                status = True
            return status, response_message
            
            
- add url pointing to the ussd simulator
  
  
  
    url(r'^ke/ussd/simulator', KenyaUssdSimulator.as_view()),
                       
    
- As for now default django session is used ( which is the database ) and it requires serializer 
settings. So add the following serializer  to your settings


      SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
  
For more usage info, checkout the `example` app.


# command to dump sample data
docker run web  python manage.py  dumpdata ussd --format yaml --output ke_ussd.yaml