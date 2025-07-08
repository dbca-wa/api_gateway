import json
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from django.core.cache import cache
from requests.auth import HTTPBasicAuth
from apigw import utils
import urllib.request
import urllib.parse


def aws_service_request(request, asq):
    print("AWS SERVICE REQUEST")
    paramGET = request.GET.get("paramGET", "{}")
    paramPOST = request.GET.get("paramPOST", "{}")
    cache_string = (
        "APIService" + asq.service_slug_url + "_query" + str(paramGET) + str(paramPOST)
    )

    apidata = cache.get(cache_string)
    if apidata is None or asq.cache_enabled is False:
        aws_access_key = asq.aws_access_key
        aws_secret_access_key = asq.aws_secret_access_key
        aws_token = asq.aws_token
        aws_host = asq.aws_host
        aws_region = asq.aws_region
        aws_service = asq.aws_service
        service_endpoint_url = asq.service_endpoint_url
        if aws_access_key is None:
            aws_access_key = ""
        if aws_secret_access_key is None:
            aws_secret_access_key = ""
        if aws_token is None:
            aws_token = ""
        if aws_host is None:
            aws_host = ""
        if aws_region is None:
            aws_region = ""
        if aws_service is None:
            aws_service = ""
        if service_endpoint_url is None:
            service_endpoint_url = ""

        paramGET_obj = json.loads(paramGET)
        paramPOST_obj = json.loads(paramPOST)
        encode_get_url = ""
        for g in paramGET_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + utils.clean_url(paramGET_obj[g])
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + utils.clean_url(paramGET_obj[g])

        for g in paramPOST_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + utils.clean_url(paramGET_obj[g])
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + utils.clean_url(paramGET_obj[g])

        auth = AWSRequestsAuth(
            aws_access_key=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
            aws_token=aws_token,
            aws_host=aws_host,
            aws_region=aws_region,
            aws_service=aws_service,
        )

        if service_endpoint_url[-1:] != "?" and len(encode_get_url) > 0:
            encode_get_url = "?" + encode_get_url
        r = requests.get(service_endpoint_url + encode_get_url, auth=auth)
        if asq.cache_enabled:
            cache.set(cache_string, r.text, asq.cache_limit)
        apidata = r.text
    else:
        pass

    return apidata


def http_request(request, asq, http_type):

    paramGET = request.GET.get("paramGET", "{}")
    paramPOST = request.GET.get("paramPOST", "{}")
    cache_string = (
        "APIService" + asq.service_slug_url + "_query" + str(paramGET) + str(paramPOST)
    )

    apidata = cache.get(cache_string)
    if apidata is None or asq.cache_enabled is False:
        service_endpoint_url = asq.service_endpoint_url
        basic_auth_enabled = asq.basic_auth_enabled
        basic_auth_username = asq.basic_auth_username
        basic_auth_password = asq.basic_auth_password

        if basic_auth_username is None:
            basic_auth_username = ""
        if basic_auth_password is None:
            basic_auth_password = ""
        if service_endpoint_url is None:
            service_endpoint_url = ""

        paramGET_obj = json.loads(paramGET)
        paramPOST_obj = json.loads(paramPOST)

        # print (paramGET_obj['boatNumber'])
        encode_get_url = ""
        for g in paramGET_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + paramGET_obj[g]
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + paramGET_obj[g]

        for g in paramPOST_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + paramGET_obj[g]
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + paramGET_obj[g]

        if service_endpoint_url[-1:] != "?" and len(encode_get_url) > 0:
            encode_get_url = "?" + encode_get_url
        if basic_auth_enabled is True:
            auth = auth = HTTPBasicAuth(basic_auth_username, basic_auth_password)
            if http_type == "post":
                r = requests.post(
                    service_endpoint_url + encode_get_url, auth=auth, data=paramPOST_obj
                )
            if http_type == "get":
                r = requests.get(service_endpoint_url + encode_get_url, auth=auth)

        else:
            if http_type == "post":
                r = requests.post(
                    service_endpoint_url + encode_get_url, data=paramPOST_obj
                )
            if http_type == "get":
                r = requests.get(service_endpoint_url + encode_get_url)

        if asq.cache_enabled:
            cache.set(cache_string, r.text, asq.cache_limit)
        apidata = r.text
    else:
        pass

    return apidata


def oauth_bearer(request, asq, http_type):

    paramGET = request.GET.get("paramGET", "{}")
    paramPOST = request.GET.get("paramPOST", "{}")
    urlappendGET = request.GET.get("urlappendGET", "")
    cache_string = (
        "APIService"
        + asq.service_slug_url
        + "_query"
        + str(paramGET)
        + str(paramPOST)
        + str(urlappendGET)
    )

    apidata = cache.get(cache_string)
    if apidata is None or asq.cache_enabled is False:
        service_endpoint_url = asq.service_endpoint_url
        oauth2_url = asq.oauth2_url
        oauth2_client_id = asq.oauth2_client_id
        oauth2_secret = asq.oauth2_secret
        oauth2_api_ocp_apim_subscription_key = asq.oauth2_api_ocp_apim_subscription_key

        if oauth2_url is None:
            oauth2_url = ""
        if oauth2_client_id is None:
            oauth2_client_id = ""
        if oauth2_secret is None:
            oauth2_secret = ""
        if service_endpoint_url is None:
            service_endpoint_url = ""

        paramGET_obj = json.loads(paramGET)
        paramPOST_obj = json.loads(paramPOST)

        # print (paramGET_obj['boatNumber'])
        encode_get_url = ""

        if urlappendGET:
            service_endpoint_url = service_endpoint_url + urlappendGET

        for g in paramGET_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + paramGET_obj[g]
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + paramGET_obj[g]

        for g in paramPOST_obj.keys():
            if encode_get_url == "":
                encode_get_url = encode_get_url + g + "=" + paramGET_obj[g]
            else:
                encode_get_url = encode_get_url + "&" + g + "=" + paramGET_obj[g]

        if service_endpoint_url[-1:] != "?" and len(encode_get_url) > 0:
            encode_get_url = "?" + encode_get_url

        body = {
            "client_id": oauth2_client_id,
            "client_secret": oauth2_secret,
            "grant_type": "client_credentials",
        }
        data = urllib.parse.urlencode(body).encode("utf-8")
        req = urllib.request.Request(oauth2_url, data)
        response = urllib.request.urlopen(req)
        jsonResponse = json.loads(response.read())
        aadToken = jsonResponse["access_token"]
        api_headers = {
            "User-agent": "Mozilla/5.0",
            "Ocp-Apim-Subscription-Key": oauth2_api_ocp_apim_subscription_key,
            "Authorization": "Bearer " + aadToken,
        }

        data = {}
        print("RQUIESTING ")
        print(service_endpoint_url + encode_get_url)
        r = requests.get(
            service_endpoint_url + encode_get_url, data=data, headers=api_headers
        )

        # req = urllib.request.Request(service_endpoint_url+encode_get_url, data, api_headers)
        # r = urllib.request.urlopen(req)

        # auth=auth=HTTPBasicAuth(basic_auth_username,basic_auth_password)
        # if http_type == 'post':
        #     r = requests.post(service_endpoint_url+encode_get_url, auth=auth, data=paramPOST_obj)
        # if http_type == 'get':
        #     r = requests.get(service_endpoint_url+encode_get_url, auth=auth)

        if asq.cache_enabled:
            cache.set(cache_string, r.text, asq.cache_limit)
        apidata = r.text
    else:
        pass

    return apidata
