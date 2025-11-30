import requests

url = "https://play.google.com/store/apps/details?id=com.cbe.mobilebanking"

try:
    r = requests.get(url)
    print("Play Store reachable:", r.status_code)
except Exception as e:
    print("Cannot access Play Store:", e)
