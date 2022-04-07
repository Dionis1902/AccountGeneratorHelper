from temp_mail import InboxKittenMail


mail = InboxKittenMail()
mail.set_mail('heavy-nobody-46')


@mail.letter_handler(sender_mail='den70007.ua@gmail.com')
def test(letter):
    print(letter)


mail.poling()
