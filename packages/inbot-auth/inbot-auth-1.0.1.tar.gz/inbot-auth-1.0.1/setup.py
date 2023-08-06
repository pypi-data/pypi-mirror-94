import os

from setuptools import setup, find_packages

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
with open(requirements_path) as requirements_file:
    requirements = requirements_file.readlines()

__version__ = '1.0.1'

setup(
    name='inbot-auth',
    version=__version__,
    description='Flask wrapper with pre-configured azure OIDC support',
    url='https://github.com/Inbot/inbotauth.git',
    maintainer='Aarni Alasaarela',
    maintainer_email='aarni.alasaarela@gmail.com',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    dependency_links=[],
    install_requires=[
        'inbot-common==0.5.9',
        'Flask>=1.0.2',
        'Flask-Session>=0.3.0',
        'Flask-SQLAlchemy>=2.4.0',
        'marshmallow>=2.21.0',
        'msal>=1.8.0',
        'requests>=2.24.0',
        'SQLAlchemy>=1.3.22',
        'urllib3>=1.25.11',
        'Werkzeug>=1.0.1'
    ],
    python_requires=">=3.6"
)
