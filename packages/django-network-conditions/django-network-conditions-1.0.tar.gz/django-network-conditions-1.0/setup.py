import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name = 'django-network-conditions',
    version = '1.0',
    packages = ['django_network_conditions'],
    url = 'http://pypi.python.org/pypi/django-network-conditions',
    license = 'LICENSE',
    description = description,

    requires = [

    ],

)