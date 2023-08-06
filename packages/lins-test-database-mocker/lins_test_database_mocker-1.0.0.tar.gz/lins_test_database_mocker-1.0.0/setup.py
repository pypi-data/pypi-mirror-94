import setuptools
from os import environ

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lins_test_database_mocker",
    version=environ.get('BUILD_VERSION', '0.0.1'),
    author='Diego Magalhães',
    author_email='diego.magalhaes@dbccompany.com.br',
    description='Lib para criação e população de databases para testes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/grupolinsferrao/pypck-lins-test-database-mocker',
    packages=setuptools.find_packages(),
    install_requires=['pymysql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
