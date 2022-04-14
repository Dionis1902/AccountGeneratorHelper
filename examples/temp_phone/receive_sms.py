from account_generator_helper import ReceiveSms
from account_generator_helper.countries import Counties

phone = ReceiveSms()

country = phone.get_country(Counties.UKRAINE)
phone = country.get_number()
print('Phone number :', phone.number)  # Phone number : 380665327743

for message in phone.get_last_messages():
    print(message)  # <Message ...>
