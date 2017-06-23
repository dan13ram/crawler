import config

def checkNullParams(log):
    if ((log['url'] not in config.NULLPARAM_URLS) and (log['url_params'] == None or len(log['url_params']) == 0)):
        return True
    return False
