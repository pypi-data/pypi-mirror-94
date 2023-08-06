from setuptools import setup

setup(
    name='cryptobazen',
    version='0.1.0',
    description='Wrappers for several exchanges, mainly used for jupyter',
    url='https://bitbucket.org/salurebi/salure_helpers/',
    author='Cryptobazen',
    author_email='info@cryptobazen.com',
    license='N.A.',
    packages=['cryptobazen'],
    package_data={'cryptobazen': []},
    install_requires=[
        'requests>=2,<3'
    ],
    zip_safe=False
)
