from distutils.core import setup
from mjango import __version__
from setuptools import find_packages

setup(
    name='mjango',
    version=__version__,
    license='MIT',
    description='database sdk for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    url='https://github.com/revtel/mjango',
    keywords=['revteltech', 'sdk'],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'pymongo',
        'dnspython'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
