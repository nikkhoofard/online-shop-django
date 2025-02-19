from ippanel import Client
from online_shop import settings
import requests
import json
"""
def send_verification_code(phone_number, code):
    api = kavenegar.KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {
        'sender': '1000596446',  # Your Kavenegar sender number
        'receptor': phone_number,
        'message': f'Your verification code is: {code}',
    }
    api.sms_send(params)
"""




def send_verification_code(phone_number, code):
    API_KEY = 'OWUzYzEzMjEtZjgxNS00MzRlLThhYTEtMzFjMzA4N2ExMmY1NTY1NGExODVhNDhkZGQ5NzllYjg0NGM3MzgwOGUxMjE='
 
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
 
    payload = json.dumps({
        "code": "0s4osu9wi3ekzsv",
        "sender": "+9810004223",
        "recipient": phone_number ,
        "variable": {
          "code": code
                      }
          })
    headers = { 
        'accept': '*/*',
        'apikey': settings.API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
