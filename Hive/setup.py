from setuptools import setup

setup(
    name='Apiary Hive',
    version='0.1.0',
    author='Sam Betts, Bradley Jones, John Davidge, Jack Peter Fletcher',
    author_email='bradleyjones92@googlemail.com',
    packages=['hive.common', 'hive', 'hive.honeycomb', 'hive.control'],
    url='http://bradleyjones.github.io/apiary',
    license='LICENSE.txt',
    description='Middleware for the Apiery Project',
    long_description=open('README.md').read(),
    install_requires=[
        "configobj",
        "pika",
    ],
    entry_points={
        'console_scripts':
        ['apiary_honeycomb = hive.honeycomb.honeycomb:main',
         'apiary_control = hive.control.control:main',
         'apiary_intelligence = hive.control.intelligence:main',
         ]
    },
)
