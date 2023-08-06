Mopinion API - Python Client
==========================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://github.com/mopinion/mopinion-python-api/blob/master/LICENSE
    :alt: License-MIT

.. image:: https://readthedocs.org/projects/mopinion-python-api/badge/?version=latest
    :target: https://mopinion-python-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/mopinion/mopinion-python-api/workflows/Test%20Suite/badge.svg/
    :alt: GitHub Actions

.. image:: https://badge.fury.io/py/mopinion.svg/
    :target: https://badge.fury.io/py/mopinion/
    :alt: Badge PyPi


A client library for the `Mopinion Data API <https://developer.mopinion.com/api/>`_.

Our Mopinion Client provides functionality for authentication, authorization and requesting resources.
It comes with an easy, beautiful, and elegant way of interacting with our API.

`Read the docs <https://mopinion-python-api.readthedocs.io/en/latest/>`_ for further information.

Installation
-------------

Install using ``pip``...::

    pip install mopinion


Example
--------

.. code:: python

    >>> from mopinion import MopinionClient
    >>> client = MopinionClient(public_key=YOUR_PUBLIC_KEY, private_key=YOUR_PRIVATE_KEY)
    >>> assert client.is_available()
    >>> response = client.resource("account")
    >>> assert response.json()["_meta"]["code"] == 200
    >>> response = client.resource("deployments")
    >>> assert response.json()["_meta"]["code"] == 200


Documentation
---------------

You can find here at `Read the docs <https://mopinion-python-api.readthedocs.io/en/latest/>`_ the complete documentation.


About Mopinion
---------------

`Mopinion <https://mopinion.com/>`_ is a leading all-in-one user feedback platform that helps digital enterprises listen, understand,
and act across all digital touchpoints (web, mobile, and email). Join some of the most forward-thinking
digital teams from companies such as T-mobile, eBay, TSB Bank, Walmart, Hotels.com, Decathlon, Ahold,
Mediacorp Ltd, and many more.

Please visit the website for more information about the product: https://mopinion.com
