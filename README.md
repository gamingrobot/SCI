SCI
===

Server Control Interface

SCI is a tool for managing one or more server/daemon instances across server boxes.

### Main features:
* Cross platform - SCI is Python based, and runs on a variety of systems.
* Plugin system - A set of submodules that adds functionality to SCI.
* Service integration - Install any server as a service.
* Restart system - Remotely restart SCI, which reloads configs and all plugins.

### Major modules:
* Manager - Controls the loading of plugins and main config and adds an interface for plugins interacting with each other.
* Logger - Controls logging to console, file, and log listeners.
* Servers - Interfaces for starting, stopping, updating, and sending commands to servers/services.
* Plugins - Submodules that add overall functionality to SCI.
* Interfaces - Plugins that handle the incoming connections to SCI.


## Dependencies
* [Python 2.7](http://www.python.org/download/)
* [Twisted 12.3.0](https://twistedmatrix.com/trac/wiki/Downloads)
* [zope.interface 4.0.3](https://pypi.python.org/pypi/zope.interface#download)

## Install
* Clone this repo into a directory on your server
* Install dependencies

## Running
`python main.py sci_configname.xml`

