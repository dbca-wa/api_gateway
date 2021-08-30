import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from apigw import models
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from apigw import models
from apigw import service_requests
import base64
import datetime
#from ledger.accounts.models import EmailUser


@csrf_exempt
#@require_http_methods(['POST'])
def proxy_request(request, *args, **kwargs):
    """Search people and groups"""
    slug = args[0]
    if request.user.is_authenticated:
         if models.APIService.objects.filter(service_slug_url=slug).count() > 0:
             api_service_query = models.APIService.objects.filter(service_slug_url=slug)
             asq = api_service_query[0]
             if asq.service_type == 1:
                 response = service_requests.aws_service_request(request,asq)
                 return HttpResponse(response, content_type='application/json', status=200)
             else:
                 return HttpResponse(json.dumps({'status': 503, 'message' : 'Service does not have a service type'}), content_type='application/json')
             return HttpResponse(json.dumps({}), content_type='application/json')
         else:
             return HttpResponse(json.dumps({'status': 404, 'message': "Message Service API not found"}), content_type='application/json', status=404)
    else:
        return HttpResponse(json.dumps({'status': 403, 'message': "Forbidden Authentication"}), content_type='application/json', status=404)
