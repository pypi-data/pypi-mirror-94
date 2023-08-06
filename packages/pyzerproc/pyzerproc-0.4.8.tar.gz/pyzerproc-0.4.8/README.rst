=========
pyzerproc
=========


.. image:: https://img.shields.io/pypi/v/pyzerproc.svg
        :target: https://pypi.python.org/pypi/pyzerproc

.. image:: https://github.com/emlove/pyzerproc/workflows/tests/badge.svg
        :target: https://github.com/emlove/pyzerproc/actions

.. image:: https://coveralls.io/repos/emlove/pyzerproc/badge.svg
        :target: https://coveralls.io/r/emlove/pyzerproc


Async library to control Zerproc Bluetooth LED smart string lights

* Free software: Apache Software License 2.0


Features
--------

* Discover nearby devices
* Turn lights on and off
* Set light color
* Get light status


Command line usage
------------------
pyzerproc ships with a command line tool that exposes the features of the library.

.. code-block:: console

    $ pyzerproc discover
    INFO:pyzerproc.discovery:Starting scan for local devices
    INFO:pyzerproc.discovery:Discovered AA:BB:CC:00:11:22: LEDBlue-CC001122
    INFO:pyzerproc.discovery:Discovered AA:BB:CC:33:44:55: LEDBlue-CC334455
    INFO:pyzerproc.discovery:Scan complete
    AA:BB:CC:00:11:22
    AA:BB:CC:33:44:55

    $ pyzerproc turn-on AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Turning on AA:BB:CC:00:11:22

    $ pyzerproc turn-off AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Turning off AA:BB:CC:00:11:22

    $ pyzerproc set-color AA:BB:CC:00:11:22 ff0000
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Changing color of AA:BB:CC:00:11:22 to #ff0000

    $ pyzerproc set-color AA:BB:CC:00:11:22 00ff00
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Changing color of AA:BB:CC:00:11:22 to #00ff00

    $ pyzerproc is-on AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Got state of AA:BB:CC:00:11:22: <LightState is_on='True' color='(255, 0, 0)'>
    True

    $ pyzerproc get-color AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Connecting to AA:BB:CC:00:11:22
    INFO:pyzerproc.light:Got state of AA:BB:CC:00:11:22: <LightState is_on='True' color='(255, 0, 0)'>
    ff0000


Usage
-----

Discover nearby devices

.. code-block:: python

    import asyncio
    import pyzerproc


    async def main():
        lights = await pyzerproc.discover(timeout=30)

        for light in lights:
            print("Address: {} Name: {}".format(light.address, light.name))

    asyncio.get_event_loop().run_until_complete(main())


Turn a light on and off

.. code-block:: python

    import asyncio
    import pyzerproc


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pyzerproc.Light(address)

        try:
            await light.connect()
            await light.turn_on()

            await asyncio.sleep(5)

            await light.turn_off()
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(main())


Change the light color

.. code-block:: python

    import asyncio
    import pyzerproc


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pyzerproc.Light(address)

        try:
            await light.connect()

            while True:
                await light.set_color(255, 0, 0) # Red
                await asyncio.sleep(1)
                await light.set_color(0, 255, 0) # Green
                await asyncio.sleep(1)
        finally:
            await light.disconnect()

    asyncio.get_event_loop().run_until_complete(main())


Get the light state

.. code-block:: python

    import asyncio
    import pyzerproc


    async def main():
        address = "AA:BB:CC:00:11:22"

        light = pyzerproc.Light(address)

        try:
            await light.connect()

            state = await light.get_state()

            if state.is_on:
                print(state.color)
            else:
                print("Off")
        finally:
            await light.disconnect()


Changelog
---------
0.4.8 (2021-02-12)
~~~~~~~~~~~~~~~~~~
- Dependency cleanup `(#1) <https://github.com/emlove/pyzerproc/pull/1>`_ `(#3) <https://github.com/emlove/pyzerproc/issues/3>`_ `@fabaff <https://github.com/fabaff>`_

0.4.7 (2020-12-20)
~~~~~~~~~~~~~~~~~~
- Include a default timeout on all remote calls

0.4.5 (2020-12-20)
~~~~~~~~~~~~~~~~~~
- Wrap all exceptions from upstream code

0.4.4 (2020-12-19)
~~~~~~~~~~~~~~~~~~
- Timeout for is_connected and reduce extra calls

0.4.3 (2020-12-17)
~~~~~~~~~~~~~~~~~~
- Fix bleak dependency called in setup.py

0.4.1 (2020-12-17)
~~~~~~~~~~~~~~~~~~
- Wrap exceptions from is_connected

0.4.0 (2020-12-17)
~~~~~~~~~~~~~~~~~~
- Refactor from pygatt to bleak for async interface

0.3.0 (2020-12-03)
~~~~~~~~~~~~~~~~~~
- Remove thread-based auto_reconnect

0.2.5 (2020-06-24)
~~~~~~~~~~~~~~~~~~
- Set full brightness to 0xFF to match vendor app

0.2.4 (2020-05-09)
~~~~~~~~~~~~~~~~~~
- Improve RGB edge cases

0.2.3 (2020-05-09)
~~~~~~~~~~~~~~~~~~
- Rethrow exceptions on device subscribe

0.2.2 (2020-05-09)
~~~~~~~~~~~~~~~~~~
- Fix imports

0.2.1 (2020-05-09)
~~~~~~~~~~~~~~~~~~
- Wrap upstream exceptions

0.2.0 (2020-05-09)
~~~~~~~~~~~~~~~~~~
- Expose exception objects
- Expose light address and name on discovery

0.1.1 (2020-05-08)
~~~~~~~~~~~~~~~~~~
- Expose auto reconnect

0.1.0 (2020-05-07)
~~~~~~~~~~~~~~~~~~
- Discover nearby devices

0.0.2 (2020-05-05)
~~~~~~~~~~~~~~~~~~
- Get the current light state

0.0.1 (2020-05-04)
~~~~~~~~~~~~~~~~~~
- Initial release


Credits
-------

- Thanks to `Uri Shaked`_ for an incredible guide to `Reverse Engineering a Bluetooth Lightbulb`_.

- This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`Uri Shaked`: https://medium.com/@urish
.. _`Reverse Engineering a Bluetooth Lightbulb`: https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
