import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = 'django-network-conditions',
    version = '1.1.1',
    packages = ['django_network_conditions'],
    url = 'http://pypi.python.org/pypi/django-network-conditions',
    license = 'LICENSE',
    description='Delay the response to simulate the real network conditions',
    long_description = long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    zip_safe=False,
    install_requires=["scipy"],
)