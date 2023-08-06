from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]

setup(
    name = 'YK-Calculator',
    version = '0.0.1',
    description = 'Our package will give you a basic calculator function such as addition,subtraction, multiplication and division. It will provide you a basic undersanding of how a calculator works.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOC.txt').read(),
    url = '',
    author = 'Yumna Khan',
    author_email = 'yumnakhan2611@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ('div','sub','mul','add'),
    packages = find_packages(),
    install_require = ['']
)