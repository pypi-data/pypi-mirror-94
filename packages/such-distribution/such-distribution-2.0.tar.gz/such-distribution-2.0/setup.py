from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='such-distribution',
      version='2.0',
      description='statistical distributions',
      long_description=long_description,
      packages=['distributions'],
      zip_safe=False)
