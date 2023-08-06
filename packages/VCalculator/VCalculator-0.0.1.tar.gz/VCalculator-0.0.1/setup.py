from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='VCalculator',
    version='0.0.1',
    description='The python  file is a basic calculator which gives the values of addition, subtraction, multiplication and dvision of two numbers.',
    Long_description=open('README.txt').read() +
    '\n\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Vishal Thakur',
    author_email='vishalsanjivthakur@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['add', 'sub', 'mul', 'div'],
    packages=find_packages(),
    install_require=['']
)
