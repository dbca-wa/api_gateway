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
import ipaddress
from apigw import common_iplookup
#from ledger.accounts.models import EmailUser


@csrf_exempt
#@require_http_methods(['POST'])
def proxy_request(request, *args, **kwargs):
    """Search people and groups"""
    slug = args[0]
    if request.user.is_authenticated:
         if models.APIService.objects.filter(service_slug_url=slug).count() > 0:
             groups = request.user.groups.all()
             api_service_query = models.APIService.objects.filter(service_slug_url=slug)
             client_ip = request.GET.get('client_ip', 'NoIp')
             paramGET = request.GET.get('paramGET', '{}')
             paramPOST = request.GET.get('paramPOST', '{}')
             error=''

             valid_client_ip = False
             try:
                 ipaddress.ip_address(client_ip)
                 valid_client_ip = True
             except:
                 pass
             if valid_client_ip is False:
                   return HttpResponse(json.dumps({'status': 503, 'message' : 'Invalid Client IP'}), content_type='application/json')

             asq = api_service_query[0]
             server_ip = common_iplookup.get_client_ip(request)
             allowed = common_iplookup.api_allow(server_ip,asq.id)

             throttle_limit_reached = False
             if asq.throttling_enabled is True:
                  throttle_time = datetime.datetime.now() - datetime.timedelta(seconds=asq.throttle_period)
                  request_count = models.APIServiceLog.objects.filter(api_service=asq,client_ip=client_ip, created__gt=throttle_time).count()
                  if request_count > asq.throttle_limit:
                         throttle_limit_reached = True
                         allowed = False
                         error = "Request Limit Reached ("+str(request_count)+")"


             models.APIServiceLog.objects.create(api_service=asq,
                                                 service_slug_url=asq.service_slug_url,
                                                 server_ip=server_ip,
                                                 client_ip=client_ip,
                                                 parameters_get=paramGET,
                                                 parameters_post=paramPOST,
                                                 error=error,
                                                 allowed=allowed

                                         )
             if throttle_limit_reached is True:
                  return HttpResponse(json.dumps({'status': 503, 'message' : error}), content_type='application/json')
             
             if allowed is True:
                  if asq.group in groups:
                       if asq.service_type == 1:
                            response = service_requests.aws_service_request(request,asq)
                            return HttpResponse(response, content_type='application/json', status=200)
                       elif asq.service_type == 2:
                            response = service_requests.http_request(request,asq,'get')
                            return HttpResponse(response, content_type='application/json', status=200)
                       elif asq.service_type == 3:
                            response = service_requests.http_request(request,asq,'post')
                            return HttpResponse(response, content_type='application/json', status=200)
                       else:
                            return HttpResponse(json.dumps({'status': 503, 'message' : 'Service does not have a service type'}), content_type='application/json')
                  else:
                      return HttpResponse(json.dumps({'status': 403, 'message' : 'Permission Denied'}), content_type='application/json')
                  return HttpResponse(json.dumps({}), content_type='application/json')
             else:
                  return HttpResponse(json.dumps({'status': 403, 'message' : 'Access Denied'}), content_type='application/json')    
         else:
             return HttpResponse(json.dumps({'status': 404, 'message': "Message Service API not found"}), content_type='application/json', status=404)
    else:
        return HttpResponse(json.dumps({'status': 403, 'message': "Forbidden Authentication"}), content_type='application/json', status=404)
