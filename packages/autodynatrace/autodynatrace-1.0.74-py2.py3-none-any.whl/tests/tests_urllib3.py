import autodynatrace
import time
import requests


@autodynatrace.trace
def send_request():
    requests.api.get("https://api.spacexdata.com/v3/launches/latest")


while True:
    print("Testing requests")
    send_request()
    time.sleep(2)
