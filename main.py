import sys
import progressbar
import db
import config
import geo
import frequency
import user_agent
import aws
import azure
import dns
import null_param
import tor
import time

current_time = lambda: int(round(time.time() * 1000))

def myprint(ip, a, b):
    if ip == "something":
        print a, b

def parseLog(log):
    ip = log['remote_ip']
    ip_score = db.getIp(log)
    if ip_score == None or ip_score['last_time'] < (current_time() - config.EXPIRE_SCORE_TIME):
        ip_score = {
            'ip' : ip,
            'score': 1,
            'last_time': log['time'],
            'frequency': [0 for i in xrange(10)],
            'captcha_count': 0,
            'is_google_ip': False
        }

    if ip_score['is_google_ip']:
        return False
    score = ip_score['score']
    ip_score['last_time'] = log['time']

    myprint(ip, "IP", ip)
    myprint(ip, "INIT", score)
    if not geo.checkIndianIP(ip):
        score = score * config.GEO / 1000
        myprint(ip, "CHANGE", "GEO")
        myprint(ip, "AFTER", score)
    if aws.checkAWS(ip):
        score = score * config.AWS / 1000
        myprint(ip, "CHANGE", "AWS")
        myprint(ip, "AFTER", score)
    if azure.checkAzure(ip):
        score = score * config.AZURE / 1000
        myprint(ip, "CHANGE", "AZURE")
        myprint(ip, "AFTER", score)
    if tor.checkTor(ip):
        score = score * config.TOR / 1000
        myprint(ip, "CHANGE", "TOR")
        myprint(ip, "AFTER", score)
    if null_param.checkNullParams(log):
        score = score * config.NULLPARAM / 1000
        myprint(ip, "CHANGE", "NULLPARAM")
        myprint(ip, "AFTER", score)
    if user_agent.checkBadBot(log['user_agent']):
        score = score * config.USERAGENT / 1000
        myprint(ip, "CHANGE", "USERAGENT")
        myprint(ip, "AFTER", score)
    factor, new_ip_score = frequency.checkFrequency(log)
    score = score * factor
    if new_ip_score is not None and 'frequency' in new_ip_score:
        ip_score['frequency'] = new_ip_score['frequency']

    myprint(ip, "CHANGE", "FREQUENCY")
    myprint(ip, "AFTER", score)
    if user_agent.checkGoogleBot(log['user_agent']):
        if dns.checkGoogleBot(ip):
            ip_score['is_google_ip'] = True
        else:
            score = score * config.BADGOOGLEBOT / 1000
            myprint(ip, "CHANGE", "BADGOOGLEBOT")
            myprint(ip, "AFTER", score)

    ip_score['score'] = score

    is_bot = False
    if score <= config.FLAG_BOT_SCORE / 1000:
        ip_score['captcha_count'] = ip_score['captcha_count'] + 1
        is_bot = True

    db.updateIp(ip_score)
    return is_bot

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE:', sys.argv[0], 'NUM_LOGS'
        sys.exit(1)
    total = int(sys.argv[1])
    found_logs = db.logs.find().limit(total)
    bar = progressbar.ProgressBar(maxval=total, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    count = 0
    for log in found_logs:
        log['remote_ip'] = [x.strip() for x in log['remote_ip'].split(',')][-1]
        parseLog(log)
        count = count + 1
        bar.update(count)
    bar.finish()
    print 'DONE'
