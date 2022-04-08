from temp_all import ReceiveSms
from temp_all.temp_phone.countries import Counties

phone = ReceiveSms()

country = phone.get_country(Counties.UKRAINE)
phone = country.get_number()
print('Phone number :', phone.number)

for message in phone.get_last_messages():
    print(message)
