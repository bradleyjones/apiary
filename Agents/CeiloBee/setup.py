import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='ApiaryCelioBee',
    version='0.0.1',
    author='Sam Betts, Bradley Jones, John Davidge, Jack Peter Fletcher',
    author_email='jackfletcher2010@googlemail.com',
    packages=find_packages(),
    url='http://bradleyjones.github.io/apiary',
    license='../../LICENSE.txt',
    description='Celiometer Agent for the Apiary Project',
    long_description=open('README.md').read(),
    install_requires=[
        "configobj >= 4.7.2",
        "pika >= 0.9.13",
        "jsonschema >= 2.2.0",
        "pymongo >= 2.6.3",
    ],
    entry_points={
        'console_scripts':
        ['apiary-celiobee = celiobee:main',
         ]
    }
)
