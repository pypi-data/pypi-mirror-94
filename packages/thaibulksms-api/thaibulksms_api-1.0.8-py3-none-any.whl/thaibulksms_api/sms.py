import requests
url = 'https://api-v2.thaibulksms.com/sms'
def send_sms(apiKey, apiSerect, phone, message, sendername='SMS.', scheduled_delivery='', force=''):
    r = requests.post(url, data={'msisdn': phone, 'message': message, 'sender': sendername}, auth=(apiKey, apiSerect))
    return r
