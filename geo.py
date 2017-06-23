from geoip import geolite2

def checkIndianIP(ip):
    try:
        match = geolite2.lookup(ip)
        if str(match.country).upper() == 'IN':
            return True
    except:
        pass
    return False
