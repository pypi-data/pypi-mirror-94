from setuptools import setup

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
    name='ucla_geotech_tools-random_field',
    version='0.0.4',
    description='Random field generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yang Yang',
    author_email='dienyoung@outlook.com',
    license='MIT',
    classifiers=classifiers,
    py_modules = ['ucla_geotech_tools.random_field'],
    namespace_packages=['ucla_geotech_tools'],
)
