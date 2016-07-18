import json
import requests

result = json.loads('http://192.168.1.6:8090/cuckoo/status')
print('hostname: ', result['hostname'] )
