import yaml
from setuptools import setup, find_packages
from io import open
from os import path

readme = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(readme, 'r') as f:
    readme_contents = f.read()

with open('build.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

name = config.get('project')
version = config.get('version')
description = config.get('description')
author = config.get('author')
author_email = config.get('author_email')
url = config.get('url')

install_requires = []    
  
setup(
    name=name,
    version=version,
    description=description,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    url=url,
    author=author,
    author_email=author_email,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='python development library',
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3',
    project_urls={
        'Bug Reports': url,
        'Tracker': url,
        'Source': url,
    },
)
