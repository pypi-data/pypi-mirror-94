from setuptools import setup, find_packages

setup(
    name='hsmodels',
    version='0.1',
    packages=find_packages(include=['hsmodels', 'hsmodels.*', 'hsmodels.schemas.*', 'hsmodels.schemas.rdf.*'],
                           exclude=("tests",)),
    install_requires=[
        'rdflib',
        'pydantic',
        'email-validator'
    ],
    url='https://github.com/hydroshare/hsmodels',
    license='',
    author='Scott Black',
    author_email='scott.black@usu.edu',
    description='Pydantic models for HydroShare metadata'
)
