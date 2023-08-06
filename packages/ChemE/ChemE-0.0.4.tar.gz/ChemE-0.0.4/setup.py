from setuptools import setup
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name='ChemE',
    version='0.0.4',
    description='Various functions and data for Chemical Engineering Students',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ConciseVerbosity18/ChemE_CV',
    author='ol-<(',
    license="MIT",
    install_requires=['numpy','scipy','pandas','matplotlib'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    include_package_data=True,
    package_data={'':['Data_files/*.txt']},
    packages=['ChemE']
    
)
