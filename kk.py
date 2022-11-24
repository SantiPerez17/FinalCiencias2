import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    ,
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
call = requests.get('http://localhost:8080/ors/v2/directions/driving-car?&start=-60.5799053,-33.8950982&end=-60.5799053,-33.8950982', headers=headers,verify=False)

print(call.status_code, call.reason)
print(call.text)