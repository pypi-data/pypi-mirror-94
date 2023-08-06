import random
from smsc.smsc_api import *


def generate_pass_code():
    return random.randint(1000, 9999)


def send_message(phone, pass_code):
    smsc = SMSC()
    phone = phone.replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    smsc.send_sms(phone, 'Ваш проверочный код: {}'.format(pass_code), sender='sms')
    return True
