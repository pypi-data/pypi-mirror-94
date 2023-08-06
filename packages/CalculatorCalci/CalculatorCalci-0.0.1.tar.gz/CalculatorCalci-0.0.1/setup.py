from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'CalculatorCalci',
    version = '0.0.1',
    description = 'Our package will give u a basic calculator function such as add, sub, multiply and divide.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Shreyas Jadhav',
    author_email = 'jshreyas12@gmail.com',
    classifiers = classifiers,
    keywords = ('add','sub','mul','div'),
    packages = find_packages(),
    install_require = ['']
)