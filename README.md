<p align="center">
    <img src="https://img.shields.io/github/license/DioniS1902/AccountGeneratorHelper" />
    <img src="https://pepy.tech/badge/account-generator-helper/month" />
    <img src="https://img.shields.io/github/stars/DioniS1902/AccountGeneratorHelper" />
    <img src="https://img.shields.io/pypi/v/account-generator-helper" />
    <img src="https://img.shields.io/pypi/pyversions/account-generator-helper" />
</p>

# <p align="center">AccountGeneratorHelper

<h3 align="center">Library to facilitate accounts generation.</h3>
<p align="center"><i>Unofficial API for temp email services.</i></p>
<p align="center"><i>Receive SMS from free services.</i></p>
<p align="center"><i>Parsing and testing proxies.</i></p>
<p align="center"><i>Free solving regular text captcha.</i></p>
<p align="center"><i>Generate fake person.</i></p>
<p align="center"><i>Generate passwords and etc.</i></p>

## Contents
* [Supported services](#supported-services)
* [Getting started](#getting-started)
* [Usage](#usage)
    * [Temp email services](#temp-email-services)
    * [Receive SMS](#receive-sms)
    * [Generate data](#generate-data)
    * [Proxy parser](#proxy-parser)
    * [Captcha solving](#captcha-solving)
* [Coming soon](#coming-soon)
* [Say thank you me](#say-thank-you-me)

## Supported services
### Services for temporary mail
- ✅ [Inbox Kitten](https://inboxkitten.com/)
- ✅ [TempMail +](https://tempmail.plus/)
- ✅ [TempMail.lol](https://tempmail.lol/)
- ✅ [TempMail](https://temp-mail.org/uk/)
- ✅ [GmailNator](https://www.gmailnator.com/) *(Temp gmail email)*
### Services for receiving SMS
- ✅ [Receive Sms Free](https://receive-sms-free.cc/)
### Services for fake data
- ✅ [Randomuser](https://randomuser.me)
### Services for proxy list
- ✅ [Proxy List](https://www.proxy-list.download/)
- ✅ [SSL Proxies](https://www.sslproxies.org/)
- ✅ [Socks Proxy](https://www.socks-proxy.net/)
- ✅ [Free Proxy List](https://free-proxy-list.net/)
- ✅ [ProxyScrape](https://proxyscrape.com/free-proxy-list)
- ✅ [HideMy.name](https://hidemy.name/)
- ✅ [Advanced](https://advanced.name/freeproxy)
- ✅ [OpenProxy](https://openproxy.space/list)
- ✅ [GeoNode](https://geonode.com/free-proxy-list/)
- ✅ [OpenProxy](https://openproxy.space/list)
### Services for solving captcha
- ✅ [Optiic](https://optiic.dev/)

## Getting started
This library tested with Python 3.6+ and Pypy 3. There are two ways to install the library:
- Installation using pip (a Python package manager):
```
$ pip install account-generator-helper
```
- Installation from source (requires git):
```
$ git clone https://github.com/Dionis1902/AccountGeneratorHelper.git
$ cd AccountGeneratorHelper
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/Dionis1902/AccountGeneratorHelper.git
```
It is generally recommended using the first option.

*While the library is production-ready, it is still under development, and it has regular updates, do not forget to update it regularly by calling*
```
$ pip install account-generator-helper --upgrade
```

## Usage
### Temp email services
```python
# Inbox Kitten
from account_generator_helper import InboxKitten


mail = InboxKitten()
print('Mail :', mail.set_email('test-mail'))  # Mail : test-mail@inboxkitten.com


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : (Letter ..)
    print('Letter content :', _letter.letter)  # Letter content : ...


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
```

```python
# TempMail +
from account_generator_helper import TempMailPlus, TempMailPlusDomains


mail = TempMailPlus()
print('Mail :', mail.set_email('test-mail', TempMailPlusDomains.MAILTO_PLUS))  # Mail : test-mail@mailto.plus


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : (Letter ...)
    print('Letter content :', _letter.letter)  # Letter content : ...


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
```

```python
# GmailNator
from account_generator_helper import GmailNator


mail = GmailNator()
print('Mail :', mail.set_email('jo.n.a.thanm.icha.eltmp@gmail.com'))  # Mail : jo.n.a.thanm.icha.eltmp@gmail.com


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : (Letter ..)
    print('Letter content :', _letter.letter)  # Letter content : ...


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
```

```python
# TempMailLol
from account_generator_helper import TempMailLol


mail = TempMailLol()
print('Mail :', mail.get_email())  # Mail : 73f17426835@delusionstress.in


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : (Letter ..)
    print('Letter content :', _letter.letter)  # Letter content : ...


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
```

```python
# Temp Mail
from account_generator_helper import TempMail


mail = TempMail()
print('Mail :', mail.get_email())  # Mail : lolerip541@gpipes.com


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : (Letter ..)
    print('Letter content :', _letter.letter)  # Letter content : ...


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(from_email='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
```


### Receive SMS
```python
# Receive Sms Free
from account_generator_helper import ReceiveSms, Counties


phone = ReceiveSms()

country = phone.get_country(Counties.POLAND)
phone = country.get_number()
print('Phone number :', phone.number)  # Phone number : 380665327743

for message in phone.get_last_messages():
    print(message)  # (Message ...)
```

### Generate data
```python
# Generate fake person
from account_generator_helper import generate_person, generate_persons


print(generate_person())  # Person(gender='female', nam...)
print(generate_persons(10))  # [Person(gender='female', nam...), Person(gender='female', nam...), ...]
```

```python
# Utilities
from account_generator_helper import get_password

# Generate password
print(get_password())  # i)7\\yc4EsvTQJG'

print(get_password(numbers=False))  # a<}>?;xZr!Ne{^^H

print(get_password(special_symbols=False))  # vX12FgcJ7PYwA3tn

print(get_password(upper_case=False))  # ](}kh()|9~t(":4$

print(get_password(upper_case=False, numbers=False, special_symbols=False))  # mppimpgxchlznwmm
```

### Proxy parser

```python
# Proxy parsing
from account_generator_helper import Proxies


proxies = Proxies()

proxies.parse_proxies()

print(proxies)  # (Proxies proxies_count=11572)

print(proxies.pop())  # (Proxy proxy_type=HTTP address=203.23.106.209 port=80 country=Counties.CYPRUS)

print(proxies.pop().strfproxy())  # http://203.32.121.187:80
```

### Captcha solving
```python
# Solving regular text captcha
from account_generator_helper import CaptchaSolver

# Get api key from https://optiic.dev/
captcha_solver = CaptchaSolver('11r6wjas2zTHLTgdWvEjaap1xq7m7111ufUNFas1fwCS')

print('Captcha 1 result :', captcha_solver.solve(open('images/captcha_1.png', 'rb')))  # 97823C

print('Captcha 2 result :', captcha_solver.solve(open('images/captcha_2.png', 'rb')))  # 8CCPXP

print('Captcha 3 result :', captcha_solver.solve(open('images/captcha_3.png', 'rb')))  # NRGFHG
```

## Coming soon
- reCAPTCHA solver
- hCaptcha solver
- FunCaptcha solver
- Better text captcha solver
- Add more emails and receiving SMS services
- Better fake person generator, with more data (credit card, bio, photo etc)
- Simple account generator (Steam, Outlook etc)

## Say thank you me
<p align="center">
    <a href="https://www.buymeacoffee.com/Dionis1902"><img src="https://i.imgur.com/zE8Y8Dp.png"></a>
</p>

<p align="center">USDT (ERC20) : 0xB8314551f0633aee73f93Ff4389629B367e59189</p>
<p align="center">USDT (TRC20) : TYJmX4R22NmSMBu7HWbwuwRr7TW9jN5az9</p>
<p align="center">BTC : bc1q3jgp25rc8qtzx0fwd9ltpy45yv05hphu7pvwla</p>
<p align="center">ETH : 0xB8314551f0633aee73f93Ff4389629B367e59189</p>
<p align="center">BNB (Smart Chain) : 0xB8314551f0633aee73f93Ff4389629B367e59189</p>

