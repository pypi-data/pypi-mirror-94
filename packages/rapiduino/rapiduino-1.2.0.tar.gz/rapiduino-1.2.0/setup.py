# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rapiduino',
 'rapiduino.boards',
 'rapiduino.communication',
 'rapiduino.components',
 'rapiduino.globals']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'rapiduino',
    'version': '1.2.0',
    'description': 'Rapidly develop code to control an Arduino using Python',
    'long_description': '[![Build and Test](https://github.com/samwedge/rapiduino/workflows/Build%20and%20Test/badge.svg)](https://github.com/samwedge/rapiduino/actions?query=workflow%3A%22Build+and+Test%22)\n[![Coverage Status](https://coveralls.io/repos/github/samwedge/rapiduino/badge.svg?branch=master)](https://coveralls.io/github/samwedge/rapiduino?branch=master)\n![Python Supported Versions](https://img.shields.io/pypi/pyversions/rapiduino)\n[![GitHub - License](https://img.shields.io/github/license/samwedge/rapiduino)](https://github.com/samwedge/rapiduino/blob/master/LICENSE)\n[![Latest Version](https://img.shields.io/pypi/v/rapiduino)](https://pypi.org/project/rapiduino/)\n\n# Rapiduino\n\nRapiduino is a Python library to allow Python code to control an Arduino.\nThe Python code runs on a computer connected to an Arduino through a serial connection.\n\nA sketch is provided to upload to the Arduino.\nThe Rapiduino library can be used to connect to the Arduino and send it familiar commands such as digitalWrite and pinMode.\nBy sending these commands from Python and not writing them directly on the Arduino, you gain the power of Python\'s wonderful syntax and libraries. \n\n## Why use Rapiduino?\n\n* Rapidly develop using everyone\'s favourite language 😉\n* Easily integrate an Arduino with Python\'s libraries to provide a real-time clock, web access, data visualisation, number crunching etc...\n* Allow hot-swappable parts. Change pin mode, pin state etc. whenever you like from your Python code!\n* Easily obtain data from your Arduino without setting up any custom communication\n* Probably many other benefits that will become realised as time goes on...\n\n\n## Are there any downsides?\n\nOf course. Don\'t use this library if:\n* You are not able to run a computer alongside an Arduino (not even a Raspberry Pi) because of issues such as size, battery, operating conditions etc.\n* You need timing accuracy that Rapiduino does not yet support; For example, for an ultrasonic sensor where the connection\n  lag could cause inaccuracy (although there are workarounds for this for specific components)\n* Probably many others personal to your project...\n\n\n## Status\n\nRapiduino is in active development.\nIt is ready to be used in simple projects, but there may be some breaking changes and restructuring until it settles down\n\n\n## Installation\n\n    pip install rapiduino\n\n\n## Usage\n\nTo use with an ArduinoUno, simply import the class and globals as follows. Importing globals give you access to the same\nINPUT, OUTPUT, HIGH, LOW, A0, A1 etc. as when developing an Arduino sketch\n\n    from rapiduino.globals.arduino_uno import *\n    from rapiduino.globals.common import *\n    from rapiduino.boards.arduino import Arduino\n\nSet up the class and serial connection with the following. The port to be passed in can be identified using the Arduino software\n\n    arduino = Arduino.uno(\'port_identifier\')\n    \nThen start using it! Here is a blinking LED example:\n    \n    import time\n    while True:\n        arduino.digital_write(13, HIGH)\n        time.sleep(1)\n        arduino.digital_write(13, LOW)\n        time.sleep(1)\n        \nYou can also use classes for components (such as LEDs) which make using the Arduino easier and less error-prone.\nThe components are "registered" to the Arduino along with a pin-mapping which tells the Arduino object which pins are connected\nto the component. Let\'s look at an example with an LED:\n\n    from rapiduino.components.led import LED\n    led = LED(arduino, 13)\n    \nThis creates an LED object and registers it to the arduino against pin 13. When binding, the code automatically\ntakes care of checking compatibility, raising an error if there is a problem. For example, if you are trying to connect \na component that requires a PWM pin to a non-PWM pin, you will get a helpful message.\n\nYou can re-write the blink example as:\n\n    while True:\n        led.toggle()\n        time.sleep(1)\n\nThe benefit of this is that you can use methods with familiar names such as:\n\n    led.turn_on()\n    led.turn_off()\n    led.toggle()\n    \nYou don\'t need to think of pin states or pin modes when interacting with your components, and you don\'t need to keep\ntrack of which pin is connected to which component - rapiduino will do that for you.\n\n\n## Contribution\n\nYes please! Code and/or suggestions are very welcome! Feel free to raise an issue or raise a pull request from a fork.\n\n\n## Developing\n\nRapiduino uses [poetry](https://python-poetry.org/docs/) to handle the installation.\n\nTo install Rapiuino for development:\n\n`poetry install`\n\nTo run tests:\n\n`make test` will run all testing, linting, type checking and coverage reporting\n\n`make fix` will auto-fix any issues found by `isort` and `black`\n\n\n## Licence\n\n[Rapiduino is released under the Apache-2.0 licence](https://github.com/samwedge/rapiduino/blob/master/LICENSE).\n\nIf you contribute code to this repository, you agree that your code will also be released under this licence.',
    'author': 'Sam Wedge',
    'author_email': 'sam.wedge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
