from account_generator_helper import TextCaptchaSolver


captcha_solver = TextCaptchaSolver()

print('Captcha 1 result :', captcha_solver.solve(open('images/captcha_1.png', 'rb')))  # 97823C

print('Captcha 2 result :', captcha_solver.solve(open('images/captcha_2.png', 'rb')))  # 8CCPXP

print('Captcha 3 result :', captcha_solver.solve(open('images/captcha_3.png', 'rb')))  # NRGFHG
