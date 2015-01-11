import codecs
import os
from setuptools import setup, find_packages


install_requirements = [
    'django>=1.5',
]


test_requirements = [
    'py==1.4.25',
    'pyflakes==0.8.1',
    'pytest==2.6.0',
    'pytest-cache==1.0',
    'pytest-cov==1.7.0',
    'pytest-flakes==0.2',
    'pytest-pep8==1.0.6',
    'pytest-django==2.7.0',
    'cov-core==1.14.0',
    'coverage==3.7.1',
    'execnet==1.2.0',
    'pep8==1.5.7',
    'mock==1.0.1',
]


doc_requirements = [
    'sphinx',
    'sphinx_rtd_theme',
]


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-perseus',
    version='0.1.1',
    description='Builds a static version of your Django website',
    long_description=read('README.md'),
    author='Carlo Smouter',
    author_email='lockwooddev@gmail.com',
    url='https://github.com/lockwooddev/django-perseus',
    packages=find_packages(),
    install_requires=install_requirements,
    extras_require={
        'docs': doc_requirements,
        'tests': test_requirements,
    },
    include_package_data=True,
    license='MIT',
    keywords='django static html',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
