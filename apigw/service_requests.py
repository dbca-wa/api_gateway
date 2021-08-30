import json
import os
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

def aws_service_request(request,asq):
     print ("AWS SERVICE REQUEST")
     aws_access_key =asq.aws_access_key
     aws_secret_access_key = asq.aws_secret_access_key
     aws_token = asq.aws_token
     aws_host = asq.aws_host
     aws_region = asq.aws_region
     aws_service = asq.aws_service
     service_endpoint_url = asq.service_endpoint_url
     if aws_access_key is None:
         aws_access_key = ''
     if aws_secret_access_key is None:
         aws_secret_access_key = ''
     if aws_token is None:
         aws_token= ''
     if aws_host is None:
         aws_host = ''
     if aws_region is None:
         aws_region =''
     if aws_service is None:
         aws_service = ''
     if service_endpoint_url is None:
         service_endpoint_url = ''

     paramGET = request.GET.get('paramGET', '{}')
     paramGET_obj= json.loads(paramGET)

     paramPOST = request.GET.get('paramPOST', '{}')
     paramPOST_obj= json.loads(paramPOST)


     #print (paramGET_obj['boatNumber'])
     encode_get_url = ""
     for g in paramGET_obj.keys():
         if encode_get_url == "":
             encode_get_url = encode_get_url +g+"="+paramGET_obj[g]
         else:
             encode_get_url = encode_get_url +"&"+g+"="+paramGET_obj[g]

     for g in paramPOST_obj.keys():
         if encode_get_url == "":
             encode_get_url = encode_get_url +g+"="+paramGET_obj[g]
         else:
             encode_get_url = encode_get_url +"&"+g+"="+paramGET_obj[g]
     auth = AWSRequestsAuth(aws_access_key=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_token=aws_token,
                            aws_host=aws_host,
                            aws_region=aws_region,
                            aws_service=aws_service
                            )
     
     if service_endpoint_url[-1:] != '?' and len(encode_get_url) >0:
           encode_get_url = "?"+encode_get_url
     r = requests.get(service_endpoint_url+encode_get_url, auth=auth)
     return r.text


