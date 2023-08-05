import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='stamdata3',
    version='v0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GPL',
    description='A Python class structure to work with data from stamdata3 XML files',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/StorFollo-IKT/stamdata3-py',
    author='Anders Birkenes',
    author_email='datagutten@datagutten.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
