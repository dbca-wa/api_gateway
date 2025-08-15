

def clean_url(value):
    value = value.replace("'", "%27")
    value = value.replace("&", "%26")
    value = value.replace("/", "%2F")
    value = value.replace(",", "%2C")    
    return value


