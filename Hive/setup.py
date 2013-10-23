import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='ApiaryHive',
    version='0.0.1',
    author='Sam Betts, Bradley Jones, John Davidge, Jack Peter Fletcher',
    author_email='jones.bradley@me.com',
    packages=find_packages(),
    url='http://bradleyjones.github.io/apiary',
    license='LICENSE.txt',
    description='Middleware for the Apiery Project',
    long_description=open('README.md').read(),
    install_requires=[
        "configobj >= 4.7.2",
        "pika >= 0.9.13",
        "jsonschema",
    ],
    entry_points={
        'console_scripts':
        ['apiary-honeycomb = hive.honeycomb.honeycomb:main',
         'apiary-control = hive.control.control:main',
         'apiary-intelligence = hive.control.intelligence:main',
         ]
    },
    package_data={
        '': ['schemas/*.js'],
    },
)
