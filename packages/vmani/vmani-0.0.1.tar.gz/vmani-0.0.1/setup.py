from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'vmani',
    version = '0.0.1',
    description = 'Our package will give u a basic calculator function such as add, sub, mul, div for the two number.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'ManishKumar Vishwakarma',
    author_email = 'vmanish1313@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keyword = ('div','sub','add','sub'),
    packages = find_packages(),
    install_require = ['']
)