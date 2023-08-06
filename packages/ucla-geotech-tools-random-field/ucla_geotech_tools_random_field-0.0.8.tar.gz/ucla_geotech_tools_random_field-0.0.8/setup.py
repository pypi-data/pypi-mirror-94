from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

classifiers = [
               "Development Status :: 5 - Production/Stable",
               "Intended Audience :: Education",
               "Operating System :: OS Independent",
               "License :: OSI Approved :: MIT License",
               "Programming Language :: Python :: 3"
               ]

setup(
    name='ucla_geotech_tools_random_field',
    version='0.0.8',
    description='Randosm field generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yang Yang',
    author_email='dienyoung@outlook.com',
    license='MIT',
    classifiers=classifiers,
    packages = ['ucla_geotech_tools.random_field'],
    namespace_packages=['ucla_geotech_tools'],
)
