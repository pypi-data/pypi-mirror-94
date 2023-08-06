from setuptools import setup,find_packages

classifiers =[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved ',
    'Programming Language :: Python :: 3'
]

setup(
    name ='Satyam',
    version='0.0.1',
    description='''This pacakage conatins a basic functionality of a 
                    calculator , containing functions such as addition , subraction , multiplication and division.
                    It  will return the value calculated by the respective function. ''',
    Long_description =open('README.txt').read() + '\n\n\n' +open('CHANGELOG.txt').read(),
    url='',
    author='Satyam Shukla',
    author_email ='coolsatyamshukla@rediffmail.com',
    license ='MIT',
    classifiers= classifiers,
    keywords =('div','sub','add','mul'),
    packages =find_packages(),
    install_require =['']
)