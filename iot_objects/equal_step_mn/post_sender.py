import requests
import json
import sys

if __name__ == "__main__":
    samsung_ip = sys.argv[1]
    data       = json.loads(sys.argv[2])
    res = requests.post(url = 'http://'+samsung_ip+'/report', json = data, timeout = 60)
