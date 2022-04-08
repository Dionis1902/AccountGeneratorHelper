from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='account_generator_helper',
    version='1.0.1',
    packages=['account_generator_helper', 'account_generator_helper.fake_data', 'account_generator_helper.temp_mail',
              'account_generator_helper.temp_mail.mail', 'account_generator_helper.temp_mail.gmailnator',
              'account_generator_helper.temp_mail.inboxkitten', 'account_generator_helper.temp_mail.tempmailplus',
              'account_generator_helper.temp_phone', 'account_generator_helper.temp_phone.receive',
              'account_generator_helper.temp_phone.receive_sms'],
    url='https://github.com/DioniS1902/account_generator_helper',
    license='',
    author='Dionis1902',
    author_email='den70007.ua@gmail.com',
    description='This library is helpful when creating accounts, it has everything you need for this',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=required
)
