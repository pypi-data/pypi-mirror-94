# indiredis

This Python3 package provides an INDI web client for general Instrument control.

INDI - Instrument Neutral Distributed Interface.

See https://en.wikipedia.org/wiki/Instrument_Neutral_Distributed_Interface

The package does not include indiserver or drivers, but is compatable with them.

Though INDI is generally used for astronomical instruments, it can work with any instrument if appropriate INDI drivers are available.

The package can be imported, or run directly with the python -m option.

The package is associated with the package indi-mr, which provides functions communicating between INDI instrument drivers and a redis database, indi-mr functions can be used which run drivers directly, or input can be taken from a server port such as that provided by indiserver, or via MQTT. Once indi-mr is used to populate redis, then a client can be created which reads and writes to redis (using functions from the indi_mr.tools module), and hence control the attached instruments.

This indiredis provides the function make_wsgi_app() which is such a client. It produces a WSGI application, which if served with a WSGI compliant web server provides an INDI web client. If you import indiredis and indi-mr, you have the choice of communicating to instruments with any of the tools provided by indi-mr, and serving the application with a web server of your choice.

If you run indiredis with the python -m option, then a script is run which imports the waitress web server, and indi-mr.inditoredis, which communicates to indiserver,
and provides an INDI web client.

 For example:

Your host should have a redis server running, typically with instruments connected by appropriate drivers and indiserver. For example, in one terminal, run:

> indiserver -v indi_simulator_telescope indi_simulator_ccd

Usage of this client is then:

> python3 -m indiredis /path/to/blobfolder


The directory /path/to/blobfolder should be a path to a directory of your choice, where BLOB's (Binary Large Objects), such as images will be stored, it will be created if it does not exist. Then connecting with a browser to http://localhost:8000 should enable you to view and control the connected instruments.

For further usage information, including setting ports and hosts, try:

> python3 -m indiredis --help


## Installation

Server dependencies: A redis server (For debian systems; apt-get install redis-server), and indiserver with drivers (apt-get install indi-bin).

For debian systems you may need apt-get install python3-pip, and then use whichever variation of the pip command required by your environment, one example being:

> python3 -m pip install indiredis

Or - if you just want to install it with your own user permissions only:

> python3 -m pip install --user indiredis

Using a virtual environment may be preferred, if you need further information on pip and virtual environments, try:

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

The above pip command should automatically pull in the following packages:

indi-mr - converts between the XML data received via the indiserver port and redis storage

skipole - framework used to build the web pages.

waitress - Python web server.

redis - Python redis client.

## Security

Only open communications are defined in this package, security and authentication are not considered.

The web service provided here does not apply any authentication.

## Documentation

Detailed information is available at:

https://indiredis.readthedocs.io


