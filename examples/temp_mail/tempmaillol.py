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