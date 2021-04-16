from setuptools import setup

setup(
    name='SmartSheet',
    version='1.0.0',
    packages=[''],
    url='',
    license='MIT',
    author='Ope Usman',
    author_email='mail.opeusman@gmail.com',
    description='Script to extract data from Smartsheet',
    python_requires='>=3',
    install_requires=[
        'smartsheet',
        'dict2xml'
    ]
)
