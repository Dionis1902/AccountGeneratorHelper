# <p align="center">AccountGeneratorHelper

<h3 align="center">Library to facilitate accounts generation.</h3>
<p align="center"><i>Unofficial API for temp email services.</i></p>
<p align="center"><i>Receive SMS from free services.</i></p>
<p align="center"><i>Generate fake person.</i></p>
<p align="center"><i>Generate passwords and etc.</i></p>

# Supported services
### Services for temporary mail
- [x] [Inbox Kitten](https://inboxkitten.com/)
- [x] [TempMail +](https://tempmail.plus/)
- [x] [GmailNator](https://www.gmailnator.com/) *(Temp gmail email)*
### Services for receiving SMS
- [x] [Receive Sms Free](https://receive-sms-free.cc/)
### Services for fake data
- [x] [TextReverse](https://www.textreverse.com/frontend/fakeAddressGenerator)

## Getting started
This library tested with Python 3.6-3.10 and Pypy 3. There are two ways to install the library:
- Installation using pip (a Python package manager):
```
$ pip install account-generator-helper
```
- Installation from source (requires git):
```
$ git clone https://github.com/DioniS1902/AccountGeneratorHelper.git
$ cd AccountGeneratorHelper
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/DioniS1902/AccountGeneratorHelper.git
```
It is generally recommended using the first option.

*While the library is production-ready, it is still under development, and it has regular updates, do not forget to update it regularly by calling*
```
$ pip install account-generator-helper --upgrade
```

# Usage
### Temp email services
```python
# Inbox Kitten
from account_generator_helper import InboxKitten


mail = InboxKitten()
print('Mail :', mail.set_email('test-mail'))  # Mail : test-mail@inboxkitten.com


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : <Letter ..>
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
from account_generator_helper import TempMailPlus
from account_generator_helper.temp_mail.tempmailplus import Domains


mail = TempMailPlus()
print('Mail :', mail.set_email('test-mail', Domains.MAILTO_PLUS))  # Mail : test-mail@mailto.plus


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : <Letter ...>
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
from account_generator_helper.temp_mail.gmailnator import Domains

mail = GmailNator()
print('Mail :', mail.set_email('test-mail', Domains.GMAILNATOR_COM))  # Mail : test-mail@gmailnator.com


for _letter in mail.get_inbox():
    print('Letter :', _letter)  # Letter : <Letter ..>
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
from account_generator_helper import ReceiveSms
from account_generator_helper.temp_phone.countries import Counties

phone = ReceiveSms()

country = phone.get_country(Counties.UKRAINE)
phone = country.get_number()  # return random number from site
print('Phone number :', phone.number)  # Phone number : 380...

for message in phone.get_last_messages():
    print(message)  # <Message ...>
```
### Generate data
```python
# Generate fake person
from account_generator_helper import Person

for _ in range(10):
    print(Person())  # <Person ...>
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