from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='pysoleno',
    version="0.0.8",
    author="Mariusz Wozniak",
    author_email="mariusz.wozniak@cern.ch",
    description="Solenoid field and inductance matrix calculator.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/mawoznia/PySoleno",
    keywords={'magnetic field', 'coil', 'solenoid', 'inductance'},
    install_requires=["numpy"],
    extras_require={"dev": ["pandas", "matplotlib",],},
    python_requires='>=3.6',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8"],

)
