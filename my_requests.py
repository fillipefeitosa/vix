import requests

resp = requests.get('http://192.168.1.6:8090/cuckoo/status')
resp_data = resp.json()
if resp.status_code != 200:
    raise ApiError('GET /cuckoo/tasks {}'.format(resp.status_code))

print('hostname: ', resp_data['hostname'])
print('total de tarefas: ', resp_data['tasks']['total'])
for cuckoo_status in resp_data:
    print(resp_data[cuckoo_status])
