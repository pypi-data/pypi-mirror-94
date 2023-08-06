from setuptools import setup , find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]

setup(
    name = 'Avk-Calculator',
    version = '0.0.1',
    description = 'Our package will give us a basic calculator function such as add, subtract, multiply and divide.',
    Long_description = open('README.txt').read() +'\n\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Apeksha Kamath',
    author_email = 'abc@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ['div' , 'sub' , 'mul' ,'add'],
    packages = find_packages(),
    install_require = ['']
)