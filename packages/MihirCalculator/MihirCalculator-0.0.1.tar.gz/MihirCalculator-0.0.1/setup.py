from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'MihirCalculator',
    version = '0.0.1',
    description = 'Our package will be doing a function of a simple calculator like addition,subtraction,multiplication and division.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Mihir Gharat',
    author_email = 'gharatmihirmohan@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ('add','sub','mul','div'),
    packages = find_packages(),
    install_require = ['']
)