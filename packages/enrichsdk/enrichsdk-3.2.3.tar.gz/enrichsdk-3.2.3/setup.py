import re
import os
import sys
import py_compile
import ast 
from setuptools import setup, find_packages 

_version_re = re.compile(r'VERSION\s+=\s+(.*)')

thisdir = os.path.dirname(__file__)
readme = open(os.path.join(thisdir, 'README.rst')).read()

with open('enrichsdk/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))
    
setup(name='enrichsdk',
      version='3.2.3',
      description='Enrich Developer Kit',
      long_description=readme, 
      url='http://github.com/pingali/scribble-enrichsdk',
      author='Venkata Pingali',
      author_email='pingali@scribbledata.io',
      license='All rights reserved',
      scripts=[
      ],
      packages=find_packages(),
      include_package_data=True, 
      zip_safe=False,
      install_requires=[
          'docutils<0.16',
          'click>=7.1.2',
          'botocore==1.17.44',
          'boto3==1.14.14',
          'sphinx-click==2.3.0',
          'glob2==0.5',
          'requests>=2.21.0',
          'requests-oauthlib==0.8.0',
          'pytest>=4.6.0',
          'numpy>=1.14.2',
          'numpydoc>=0.7.0',
          'pandas>=0.22.0',
          'idna==2.8',
          'coverage==4.4.1',
          'flake8==3.4.1',
          'raven==6.6.0',
          'python-json-logger==0.1.8',
          'python-dateutil==2.8.1',
          's3fs>=0.5.1',
          'fsspec==0.8.0',
          'colored==1.3.5',
          'flask-multistatic==1.0',
          'humanize==0.5.1',
          'pytz==2020.1',
          'Flask==1.1.2',
          'Jinja2>=2.10.1',
          'pytest-cov',
          'Markdown>=3.2.30',
          'prompt-toolkit>=2.0.10',
          'pyarrow>=0.9.0',
          'cytoolz==0.9.0.1',
          'moto>=1.3.14',
          'prefect>=0.7.0',
          "distro>=1.4.0",
          "gcsfs",
          "jupyter-core>=4.6.1",
          "nbformat>=4.4.0",
          'tzlocal>=2.0.0',
          'texttable',
          'pykafka',
          'redis',
          'gitpython',
          'logstash_formatter',
          'pyhive',
          'pyfiglet',
          'sqlalchemy',
          'papermill>=2.2.2'
      ],
      entry_points = {
          'console_scripts': [
              'enrichpkg=enrichsdk.scripts.enrichpkg:main',
          ],
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
)
