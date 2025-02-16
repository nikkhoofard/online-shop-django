import kavenegar
from online_shop import settings
def send_verification_code(phone_number, code):
    api = kavenegar.KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {
        'sender': '1000596446',  # Your Kavenegar sender number
        'receptor': phone_number,
        'message': f'Your verification code is: {code}',
    }
    api.sms_send(params)