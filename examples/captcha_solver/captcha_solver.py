from account_generator_helper import CaptchaSolver

# Get api key from https://optiic.dev/
captcha_solver = CaptchaSolver('11r6wjas2zTHLTgdWvEjaap1xq7m7111ufUNFas1fwCS')

print('Captcha 1 result :', captcha_solver.solve(open('images/captcha_1.png', 'rb')))  # 97823C

print('Captcha 2 result :', captcha_solver.solve(open('images/captcha_2.png', 'rb')))  # 8CCPXP

print('Captcha 3 result :', captcha_solver.solve(open('images/captcha_3.png', 'rb')))  # NRGFHG
