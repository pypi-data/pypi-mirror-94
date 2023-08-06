from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education ',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'Dhiraj',
    version = '0.0.1',
    description = 'package will give you a basic calculator function such as addition, substraction, multiplication and division.',
    Lang_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Dhiraj Jha',
    autor_email = 'dhirajjha735@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ('add', 'sub', 'mul', 'div'),
    packages = find_packages(),
    install_require = ['']
)