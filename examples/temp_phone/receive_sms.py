from account_generator_helper import ReceiveSms, Counties


phone = ReceiveSms()

country = phone.get_country(Counties.POLAND)
phone = country.get_number()
print('Phone number :', phone.number)  # Phone number : 380665327743

for message in phone.get_last_messages():
    print(message)  # (Message ...)
