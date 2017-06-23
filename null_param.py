import config

def checkNullParams(log):
    if ((log['url'] not in config.NULLPARAM_URLS) and ('url_params' not in log or log['url_params'] == None or len(log['url_params']) == 0)):
        return True
    return False
