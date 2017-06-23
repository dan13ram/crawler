import socket
from multiprocessing.pool import ThreadPool
from multiprocessing import TimeoutError


def checkGoogleBot(ip):
    try:
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(socket.gethostbyaddr, args=(ip,))
        dns_list = async_result.get(timeout=1)
        return dns_list[0].endswith('googlebot.com')
    except TimeoutError:
        return False
