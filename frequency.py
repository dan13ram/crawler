import config
import db

def checkFrequency(log):
    ip_score = db.getIp(log)
    try:
        if ip_score != None:
            print 'its there'
            current_interval = int((ip_score['last_time'] - log['time'])/1000)
            print current_interval
            if current_interval < config.FREQUENCY_INTERVALS:
                ip_score['frequency'][current_interval] = ip_score['frequency'][current_interval] + 1
                total = sum(ip_score['frequency'])
                db.updateIp(ip_score)
                if total > config.FREQUENCY_REQUESTS:
                    mean = total / config.FREQUENCY_INTERVALS
                    factor = abs(ip_score['frequency'][current_interval] - mean) / total
                    return 1 - factor ** 2
    except:
        pass
    return 1
