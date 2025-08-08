

def clean_url(value):

    value = value.replace("'", "%27")
    value = value.replace("&", "%26")
    return value


