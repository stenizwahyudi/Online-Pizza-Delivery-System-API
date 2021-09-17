# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Turing Pizza API",
    author_email="turingpizza@turingpizza.com",
    url="",
    keywords=["Swagger", "Turing Pizza API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    The APIs for Turing Pizza project, which includes the access to pizza sizes, pizza toppings, pizza specials, pizzas, stores and orders information through various of endpoints and methods. &lt;br&gt;&lt;/br&gt;You can find out more about Turing Pizza API at [GitHub](https://github.ccs.neu.edu/cs5500f19/TuringPizza)
    """
)
