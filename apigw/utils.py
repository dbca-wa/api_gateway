

def clean_url(value):

    urlvalue = value.replace("'", "%27")
    urlvalue = urlvalue.replace("&", "%26")
    return urlvalue


