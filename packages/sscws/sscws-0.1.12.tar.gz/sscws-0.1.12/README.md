
## Synopsis

This library provides a simple python interface to 
NASA's [Satellite Situation Center](https://sscweb.sci.gsfc.nasa.gov/)
(SSC).  This library implements the client side of the 
[SSC RESTful web services](https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/).
For more general details about the SSC web services, see
https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/.

## Code Example

This package contains example code calling most of the available web services.
To run the included example, do the following

    python -m sscws

---
There is also a [Jupyter notebook](https://jupyter.org/) 
[example](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsExample.html) 
demonstrating a simple 3D plot of orbit information.

## Motivation

This library hides the HTTP, JSON/XML, and CDF details of the SSC web 
services. A python developer only has to deal with python objects and 
methods (primarily the SpacePy data model object).

## Dependencies

At this time, the only dependency are:
1. [requests](https://pypi.org/project/requests/)
2. [numpy](https://pypi.ort/project/numpy/)
3. [matplotlib](https://pypi.org/project/matplotlib/).  This is not a critical dependency.  If it is not installed, the example will simple skip plotting some data.

The critical dependencies above will automatically be installed when this 
library is.

## Installation

To install this package

    $ pip install -U sscws


## API Reference

Refer to
[sscws package API reference](https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/py/sscws/index.html)

or use the standard python help mechanism.

    from sscws import SscWs
    help(SscWs)

## Tests

The tests directory contains 
[unittest](https://docs.python.org/3/library/unittest.html)
tests.

## Contributors

Bernie Harris.  
[e-mail](mailto:NASA-SPDF-Support@nasa.onmicrosoft.com) for support.

## License

This code is licensed under the 
[NASA Open Source Agreement](https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt) (NOSA).
