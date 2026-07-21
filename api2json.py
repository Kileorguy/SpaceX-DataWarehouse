import requests
import json

VERSION = "2.3.0/"
API_URL = "https://lldev.thespacedevs.com/"+VERSION

THROTTLE_ENDPOINT = "api-throttle"
# ENDPOINTS = ['launches','landings','spacecraft_flights', 'payload_flights','agencies', 'payloads','programs','locations', 'pads','spacecraft']
ENDPOINTS = ['payload_flights']
response = requests.get(f"{API_URL}{THROTTLE_ENDPOINT}")

if(response.raise_for_status()):
    print("Error :",response.raise_for_status())
else: 
    data = response.json()
    if(data['your_request_limit'] - data['current_use'] < len(ENDPOINTS)):
        print("You've reach your limit, please wait 1 hour")
    else: 
        for e in ENDPOINTS:
            print(e)
            response = requests.get(f"{API_URL}{e}/?limit=100")
            if(response.raise_for_status()):
                print("Error :", response.raise_for_status())
            else:
                data = response.json()
                with open(f"staging_data/raw/{e}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

print("Script Finished")
