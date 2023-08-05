import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sscws",
    version="0.1.12",
    description="NASA's Satellite Situation Center Web Service Client Library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://sscweb.sci.gsfc.nasa.gov/WebServices/REST",
    author="Bernie Harris",
    author_email="NASA-SPDF-Support@nasa.onmicrosoft.com",
    license="NOSA",
    packages=["sscws"],
#    packages=find_packages(exclude=["tests"]),
#    packages=find_packages(),
    include_package_data=True,
#    install_requires=["python-dateutil>=2.8.0", "requests>=2.20", "spacepy>=0.1.6"],
#    install_requires=["python-dateutil>=2.8.0", "requests>=2.20", "numpy>=1.19.2", "matplotlib>=3.3.2"],
    install_requires=["python-dateutil>=2.8.0", "requests>=2.20", "numpy>=1.19.4"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
#        "License :: OSI Approved :: NASA Open Source Agreement",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
#    entry_points={
#        "console_scripts": [
#            "sscws=sscws.__main__:example",
#        ]
#    },
)
