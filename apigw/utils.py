

def clean_url(value):

    urlvalue = value.replace("'", "%27")
    urlvalue = value.replace("&", "%26")
    return urlvalue


