import urllib.request
import requests
import multiprocessing as mp
import time
import sys

def timeout(t, cmd, *args, **kwds):
    pool = mp.Pool(processes=1)
    result = pool.apply_async(cmd, args=args, kwds=kwds)
    try:
        retval = result.get(timeout=t)
    except mp.TimeoutError as err:
        pool.terminate()
        pool.join()
        raise
    else:
        return retval

def open(url):
    try:
        #response = urllib2.urlopen(url)
        response = urllib.request.urlopen('http://python.org/')
        #a = 5/0
        return "True"
    except:
        return "False"
    #print(response)

if __name__ == "__main__":
    url = sys.argv[1]
    try:
        ret = timeout(5, open,  "http://"+url)
        print(ret)
    except mp.TimeoutError as err:
        print("False")
