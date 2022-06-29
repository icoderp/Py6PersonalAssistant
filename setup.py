from setuptools import setup, find_namespace_packages

setup(
    name='Personal Assistant',
    version='0.0.1',
    description='Consol scripts',
    url='https://github.com/icoderp/Py6PersonalAssistant',
    author= 'Ihor Voitiuk, Anastasiia Ivanytska, Arsen Badia',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prompt_toolkit'],
    entry_points={'console_scripts': ['start-assistant = Py6PersonalAssistant.main:main']}
)

