import requests
from account_generator_helper import ReCaptchaSolver


headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}


captcha_solver = ReCaptchaSolver()
response = captcha_solver.solve('6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-', 'https://www.google.com/recaptcha/api2/demo')

print('Captcha response :', response)  # Captcha response : 03AGdBq25OBEnZZsZCsW_sm293AnUb79X....

captcha_solver.close()
r = requests.post('https://www.google.com/recaptcha/api2/demo', data='g-recaptcha-response=' + response, headers=headers)

if 'recaptcha-success' in r.text:
    print('Success captcha solved!')
else:
    print('Oh no, captcha is not valid!')
