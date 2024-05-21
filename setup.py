#this is setup.py file which will contain all details of project here futhure used this file to create python package as pypi
# so importing all the important library which is used in this files

from setuptools import setup,find_packages
from typing import List


def get_requirements(filepath:str)->list[str]:
    #now reading the filepath 
    requirement = []
    with open(filepath,'r') as file:
        text = file.read()
        rows = text.split('\n')
        for line in rows:
            if "-e ." in line:
                continue
            else:
                requirement.append(line.strip())

    return requirement












#creating an object of setup class !!
setup(
    name = 'ML_INSURANCE_CLAIM_PREDICTION',
    version='0.0.0.1',
    long_description=open('Readme.md','r').read(),
    author='Raees Azam Shaikh',
    author_email='shaikhraishazam@gmail.com',
    url = 'https://github.com/raish123/ML_INSURANCE_CLAIM_PREDICTION',
    #creating an object of find_packages class
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt'),
    python_requires='>=3.6'
    

)