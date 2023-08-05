# indi-mr

This Python3 project provides functions for transferring the INDI protocol via MQTT and converting between the INDI protocol and redis storage. It includes tools to read/write instrument control data to redis and MQTT, and hence the INDI protocol, for use by your own Python INDI client applications.

INDI - Instrument Neutral Distributed Interface.

See https://en.wikipedia.org/wiki/Instrument_Neutral_Distributed_Interface

The package does not include indiserver or drivers, but is compatable with them.

Though INDI is generally used for astronomical instruments, it can work with any instrument if appropriate INDI drivers are available.


## Installation

You may need a number of required packages installing on your machine, depending on which functions you will be calling upon, these may include:

A redis server, assuming a debian system:

> apt-get install redis-server

indiserver with drivers:

> apt-get install indi-bin

If you are using the MQTT functions you will also need an MQTT server on your network:

> apt-get install mosquitto

You may need the Python3 version of pip to obtain further packages from Pypi.

> apt-get install python3-pip.

Then install indi-mr from pypi with:

> python3 -m pip install indi-mr

Or - if you just want to install it with your own user permissions only:

> python3 -m pip install --user indi-mr

Using a virtual environment may be preferred, if you need further information on pip and virtual environments, try:

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

You may also need to install the following packages: 

Python redis client, needed if the redis storage options are used.

> python3 -m pip install redis

Python MQTT client, needed if you are using the MQTT facility.

> python3 -m pip install paho-mqtt

These requirements are not automatically installed when you install indi-mr since you may be using MQTT or redis or both, the actual choice is left to you.

There is also a Python web client available, indiredis, which you may find useful which reads/writes to the redis storage created by the functions of this indi-mr project, and serves the instrument controls as a web service:

> python3 -m pip install indiredis


## Package indi_mr

The indi_mr package provides the following functions:


**indi_mr.inditoredis()**

Connects to a server port - typically port 7624 - (which could be provided by drivers connected through indiserver) and redis, providing redis key-value storage of the instrument parameters, and works with the pub/sub facilities of redis.


**indi_mr.driverstoredis()**

This function can take a list of drivers and will run them, without needing indiserver. Again it will provide redis key-value storage of the instrument parameters.


**indi_mr.inditomqtt()**

Receives/transmitts XML data between a server port - typically port 7624 provided by indiserver- and an MQTT server which ultimately sends data to the remote web/gui client.


**indi_mr.driverstomqtt()**

This function can take a list of drivers and will run them, without needing indiserver.

Receives/transmitts XML data between the drivers and an MQTT server which ultimately sends data to the remote web/gui client.


**indi_mr.mqtttoredis()**

Receives XML data from the MQTT server and converts to redis key-value storage, and reads data published to redis, and sends to the MQTT server.


**indi_mr.mqtttoport()**

Opens and listens on a server port - typically port 7624. If a client is connected to the port, the function forwards data from MQTT to the client, if data received from the client, passes it to MQTT. In this case the client could be an existing client that would normally connect to indiserver.


**indi_mr.tools**

The tools module contains a set of Python functions, which your own Python script may use if convenient. These read the indi devices and properties from redis, returning Python lists and dictionaries, and provides functions to transmit indi commands by publishing to redis.


## redis - why?

redis is used as:

A web-serving INDI client application typically has more than one process or thread running, redis makes common data visible to all such processes.

As well as simply storing values for other processes to read, redis has a pub/sub functionality. When data is received, indi-mr stores it, and publishes the XML data on the from_indi_channel, which could be used to alert a subscribing client application that a value has changed.

Redis key/value storage and publication is extremely easy, many web frameworks already use it.

## mqtt - why?

MQTT is an option providing distributed communications. In particular, scripts calling the driverstomqtt() function at different sites,
connected to distributed instruments, enables them to be controlled from a single client.

There is flexibility in where the MQTT server is sited, it could run on the client web/gui server, or on a different machine entirely. This makes it possible to choose the direction of the initial connection - which may be useful when passing through NAT firewalls.

As devices connect to the MQTT server, only the IP address of the MQTT server needs to be fixed, a remote device could, for instance, have a dynamic DHCP served address, and a remote GUI could also have a dynamic address, but since both initiate the call to the MQTT server, this does not matter.

It allows monitoring of the communications by a third device or service by simply subscribing to the topic used. This makes a possible instrument data broadcasting or logging service easy to implement.

It makes out-of-band communications easy, for example, if other none-INDI communications are needed between devices, then merely subscribing and publishing with another topic is possible.

A disadvantage may be a loss of throughput and response times. An extra layer of communications plus networking is involved, so this may not be suitable for all scenarios.

Though multiple clients connected to the MQTT network is possible, and useful if they are just gathering data, two clients attempting to simultaneously control one instrument would lead to chaos and confusion! A single controlling client would need to be enforced. 

## Security

Only open communications are defined in this package, security and authentication are not considered.

## Documentation

Detailed information is available at:

https://indi-mr.readthedocs.io

