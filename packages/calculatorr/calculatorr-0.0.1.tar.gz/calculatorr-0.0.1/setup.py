from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
]

setup(
    name = 'calculatorr',
    version = '0.0.1',
    description = 'This Package will provide a basics Calculator function such as add_num, sub_num, mul_num, div_num',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Aakash Gupta',
    author_email = 's1032190135@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ('add','sub','mul','div'),
    packages = find_packages(),
    install_require = ['']
)