from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

long_description = (this_directory / 'README.md').read_text()
required = (this_directory / 'requirements.txt').read_text().splitlines()

setup(
    name='account_generator_helper',
    version='1.0.10',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
        'Topic :: Internet :: Proxy Servers',
    ],
    project_urls={
        'Source': 'https://github.com/Dionis1902/AccountGeneratorHelper/tree/main/account_generator_helper',
        'Examples': 'https://github.com/Dionis1902/AccountGeneratorHelper/tree/main/examples',
        'Tracker': 'https://github.com/Dionis1902/AccountGeneratorHelper/issues',
    },
    url='https://github.com/DioniS1902/AccountGeneratorHelper',
    license='MIT',
    author='Dionis1902',
    author_email='den70007.ua@gmail.com',
    description='This library is helpful when creating accounts, it has everything you need for this',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    keywords='python email captcha proxy pypi sms gmail temp-mail captcha-solving captcha-solver fake-data account-generator captcha-recognition fake-data-generator free-proxy recive-sms gmailnator gmailnator-api poxies',
    install_requires=required
)
