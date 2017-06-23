import config
import db

def checkFrequency(log):
    ip_score = db.getIp(log)
    return_factor = 1
    try:
        if ip_score != None:
            current_interval = int((log['time'] - ip_score['last_time'])/1000)
            if current_interval < config.FREQUENCY_INTERVALS:
                ip_score['frequency'][current_interval] = ip_score['frequency'][current_interval] + 1
                total = sum(ip_score['frequency'])
                if total > config.FREQUENCY_REQUESTS:
                    mean = total / config.FREQUENCY_INTERVALS
                    factor = abs(ip_score['frequency'][current_interval] - mean) / total
                    return_factor = 1 - factor ** 2
    except:
        pass
    return return_factor, ip_score
