from pymongo import MongoClient

client = MongoClient("10.33.133.248:27101")
logs = client.crawler.logs
user_agents = client.crawler.user_agents
ip_scores = client.crawler.ip_scores

def getIp(log):
    return ip_scores.find_one({'ip': log['remote_ip']})

def updateIp(ip_score):
    ip_scores.update_one({'ip': ip_score['ip']}, {'$set': ip_score}, upsert=True) 
