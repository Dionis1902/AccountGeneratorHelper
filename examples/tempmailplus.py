from temp_mail import TempMailPlus
from temp_mail.tempmailplus import Domains


mail = TempMailPlus()
print('Mail :', mail.set_mail('test-mail', Domains.MAILTO_PLUS))

for _letter in mail.get_inbox():
    print('Letter :', _letter)
    print('Letter content :', _letter.letter)


@mail.letter_handler()
def new_mail(letter):
    print('New mail :', letter)


@mail.letter_handler(sender_mail='den70007.ua@gmail.com')
def test_from(letter):
    print('Test from :', letter)


@mail.letter_handler(re_subject='.* test .*')
def test_re_subject(letter):
    print('Test re subject :', letter)


@mail.letter_handler(sender_mail='den70007.ua@gmail.com', subject='Test letter')
def test_handler(letter):
    print('Test handler :', letter)


mail.poling()
