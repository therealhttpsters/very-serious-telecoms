from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import ReceivedFax
from faxbox.settings import MAX_PAGES


@csrf_exempt
def handle_twilio_fax_sent(request):
    if request.method == 'POST':
        twiml = """
            <Response>
                <Receive action="/fax/received"/>
            </Response>
        """
        return HttpResponse(twiml)
    else:
        return HttpResponseBadRequest('Method not allowed')


@csrf_exempt
def handle_twilio_fax_receive(request):
    if request.method == 'POST':
        ReceivedFax.objects.create(
            payload={},
            media_url=request.POST.get('MediaUrl'),
            num_pages=int(request.POST.get('NumPages'), MAX_PAGES)
        )
        return HttpResponse('')
    else:
        return HttpResponseBadRequest('Method not allowed')