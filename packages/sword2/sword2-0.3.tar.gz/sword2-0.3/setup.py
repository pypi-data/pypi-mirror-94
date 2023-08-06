# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sword2']

package_data = \
{'': ['*']}

install_requires = \
['httplib2>=0.18.1,<0.19.0', 'lxml>=4.6.2,<5.0.0']

setup_kwargs = {
    'name': 'sword2',
    'version': '0.3',
    'description': 'SWORDv2 Python client',
    'long_description': "SWORD2 python client\n--------------------\n\nA python library and client to connect to and use SWORD v2 compliant servers.\n\nSWORD overview\n\nSWORD was originally a JISC-funded initiative to define and develop a standard mechanism for depositing into repositories and other systems. Why was it created? because there was no standard way of doing this. A standard deposit interface to repositories allows more services to be built which can offer functionality such as deposit from multiple locations, e.g. disparate repositories, desktop drag’n'drop tools or from within standard office applications. SWORD can also facilitate deposit to multiple repositories, increasingly important for depositors who wish to deposit to funder, institutional or subject repositories. Other possibilities include migration of content between repositories, transfer to preservation services and many more.\n\nSWORD is an Atom Publishing Profile\n\nRather than develop a new standard from scratch, SWORD chose to leverage the existing Atom Publishing Protocol (APP), “an application-level protocol for publishing and editing Web resources”. APP is based on the HTTP transfer of Atom-formatted representations yet SWORD has focussed on two key aspects of the protocol – the deposit of files, rather than Atom documents, and the extension mechanism for specifying additional deposit parameters. Also worth noting is that SWORD does not specify the implementation of all of the functionality of APP, rather it supports deposit only – implementations are free to support update and delete if they wish but this is out of the SWORD remit.\n\nPython Client library\n\nDependencies\n\nThe core dependency is httplib2, and uses this for all of its HTTP requests and response handling.\n\nThe python client tries to use any suitable ElementTree library implementation (lxml, xml.etree, cElementTree, ElementTree) and will fail without one.\n\nInstallation:\n\n```shell\n$ pip install .\n```\n\n(use of a virtualenv is recommended)\n\nSoftware links:\n\nUsage documentation: https://github.com/swordapp/python-client-sword2/wiki \n\nAPI documentation:   http://packages.python.org/sword2/\n\nRepository:          https://github.com/swordapp/python-client-sword2\n\nIssue-tracker:       https://github.com/swordapp/python-client-sword2/issues\n",
    'author': "Ben O'Steen",
    'author_email': 'beno@gmail.com',
    'maintainer': 'Cottage Labs',
    'maintainer_email': 'us@cottagelabs.com',
    'url': 'http://swordapp.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
