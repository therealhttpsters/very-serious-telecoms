from django.urls import path
from core.views import handle_twilio_fax_receive, handle_twilio_fax_sent

app_name = 'core'

urlpatterns = [
    path('sent', handle_twilio_fax_sent),
    path('received', handle_twilio_fax_receive)
]
