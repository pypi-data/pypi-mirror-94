from setuptools import setup, find_packages

classifiers = [
    'License :: OSI Approved :: MIT License'
]

setup(
    name ='Gautam_Calculator',
    version = '0.0.1',
    description = 'A package offering basic calculator functions such as addition, subtraction, multiplication, division and exponentiation.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Gautam Chaurasia',
    author_email = 'gautamchaurasia501@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ['div', 'sub', 'mul', 'add', 'exp'],
    packages = find_packages(),
    install_require = ['']
)