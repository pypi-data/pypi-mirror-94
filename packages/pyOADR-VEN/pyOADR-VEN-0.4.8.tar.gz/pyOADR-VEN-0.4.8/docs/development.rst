Development
===========

The development of this VEN client is still in progress, and contributions are welcome

Here's how to set up `pyoadr_ven` for local development.

1. Fork the `pyoadr_ven` repo on Gitlab.
2. Clone your fork locally

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pyoadr_ven
    $ cd pyoadr_ven/
    $ pip install -r requirements_dev.txt

4. This project uses pre-commit to enforce black and flake8 on the codebase.
   Install pre-commit with::

    $ pip install pre-commit
    $ pre-commit install

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. To check you're passing the tests, just run pytest:

    $ pytest

7. Commit your changes and push your branch to Gitlab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the Gitlab website.



Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.

Test Driven Development
-----------------------
There are a number of tests written.

Tests should be written in a way where they don't need to contact an external VTN to run.
The ``test_responses.py`` tests use mocking and the ``responses`` package.

To run the test suite run:

.. code-block:: bash

    pytest

The tests are named in such a way to attempt to explain the specifications being tested.
To run the tests in a way they output a nice "rspec" style spec, run:

.. code-block:: bash

    pytest --spec

When writing tests, please use a similar style.


Testing with a local VTN server
-------------------------------

#. Start your VTN server
    * note the url it comes up on - if it isn't localhost:3000, change the LOCAL_VTN_ADDRESS
        variable (best set in a .env file)

#. Using the Django admin, create a certificate authority called ``default``
    * save the CA certificate somewhere
#. Create a certificate
    * save the certificate and private key somewhere as a PEM bundle

.. code-block:: bash

    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqFiHgHccwrsrs
    ...
    lTwad+cbPVyQMzCsxEl7e7A=
    -----END PRIVATE KEY-----
    -----BEGIN CERTIFICATE-----
    MIIESzCCAzOgAwIBAgIRAOY4YtDbjUM4gek4QkBib6cwDQYJKoZIhvcNAQELBQAw
    ...
    -----END CERTIFICATE-----


#. Create a VEN on the VTN - using the main VTN interface (not the Django admin). You will
    need to create a Customer and Site to do this.
    * Note the VEN ID
    * Note the VTN ID used

#. Using the Django admin system, create a DRProgram on the VTN
    * Add your VEN/site to this program

#. Start a python or ipython shell
    * Import the pyoadr library
    * create an agent with the appropriate parameters

.. code-block:: python

    from pyoadr_ven import OpenADRVenAgent
    agent = OpenADRVenAgent(
            ven_id=AS_NOTED_ABOVE,
            vtn_id=AS_NOTED_ABOVE,
            vtn_address=AS_NOTED_ABOVE,
            client_pem_bundle=LOCATION_OF_SAVED_PEM_BUNDLE,
            vtn_ca_cert=LOCATION_OF_SAVED_CA_CERT
        )


Follow the instructions as on the Usage page.


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Gitlab CI will then deploy to PyPI if tests pass.
