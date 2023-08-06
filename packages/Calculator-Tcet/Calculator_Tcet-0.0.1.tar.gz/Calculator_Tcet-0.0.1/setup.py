from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',


    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
setup(
    name = 'Calculator_Tcet',
    version = '0.0.1',
    description = 'Our file will give you basic functions of calculation like addition, multiplication, subtraction and division.',
    Long_description = open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url ='',
    author = 'Payal Kunwar',
    author_email ='XYZ@gmail.com',
    license ='MIT',
    classifiers = classifiers,
    keywords = ['add','sub','mul','div'],
    install_require = ['']
)