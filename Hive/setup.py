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
    description='Middleware for the Apiary Project',
    long_description=open('README.md').read(),
    install_requires=[
        "configobj >= 4.7.2",
        "pika >= 0.9.13",
        "jsonschema >= 2.2.0",
        "apns >= 1.1.2",
        "pymongo >= 2.6.3",
    ],
    entry_points={
        'console_scripts':
        ['apiary-honeycomb = hive.honeycomb:main',
         'apiary-agentmanager = hive.agentmanager:main',
         'apiary-agentmonitor = hive.agentmonitor:main',
         'apiary-timemachine = hive.timemachine:main',
         'apiary-sting = hive.sting:main',
         'apiary-pheromone = hive.pheromone:main',
         ]
    },
    package_data={
        '': ['schemas/*.js'],
    },
    eager_resources=[
        'hive/sting/apns/certs/ApiaryCert.pem',
        'hive/sting/apns/certs/ApiaryKey.pem',
    ],
)
