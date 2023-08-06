from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='buycoins_client', 
    version='0.1', 
    description='Buycoins API Python client', 
    url='https://github.com/ChukwuEmekaAjah/buycoins_python', 
    author='Chukwuemeka Ajah', 
    author_email='talk2ajah@gmail.com', 
    license='MIT', 
    packages=['buycoins_client'], 
    install_requires=['requests'], 
    zip_safe=True, 
    long_description=long_description, 
    long_description_content_type='text/markdown'
)