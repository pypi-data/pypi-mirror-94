.. _usage:

=====
Usage
=====

To use pyoadr-ven in a project::

    import pyoadr_ven

This will import the OpenAdrVENAgent class.

Register VEN
------------
If you don't have a `ven_id`, you will need to register your VEN with the VTN.  To do this call the `register` function on an initialised agent:

.. code-block:: python

    from pyoadr_ven import OpenADRVenAgent
    agent = OpenADRVenAgent(
        vtn_address="http://openadr-vtn-server.local",
        client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
        vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
        # There are more parameters but you should consult the docs for these.
        # The above ones are the minimum necessary for registration.
    )
    response = agent.register(ven_name="name_of_ven")
    # > print(response)
    # {
    #     "vtn_id": "CC_VTN",
    #     "ven_id": "09384134-1340983314",
    #     "poll_interval_secs": 40,
    # }

These values should be stored somewhere safe (i.e. persistent) and passed along to the agent instance on future initialisations.


Pre-Registered VEN
------------------
If you already know the `ven_id`, initialize an `OpenAdrVENAgent` with it:

.. code-block:: python

    agent = OpenADRVenAgent(
        ven_id="ven_id",
        vtn_id="vtn_id",
        vtn_address="http://openadr-vtn-server.local",
        poll_interval_secs=15,
        log_xml=True,
        opt_timeout_secs=3,
        opt_default_decision="optIn",
        report_parameters={} # optional
        client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
        vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
    )

The first thing you are likely to want to do is get all of the existing events that are on the VTN.

.. code-block:: python

    agent.request_events()

This will return all of the events that are on the server and addsthem to the agent's database.
This should be done once.

Then, in a long running loop, periodically run:

.. code-block:: python

    agent.tick()


Reporting
---------
The VEN agent can be setup to report back to the VTN.
To enable this, initialise the agent with the parameter:

.. code-block:: python

    report_parameters={
        "reportSpecifierId": {
            "report_interval_secs_default": 15,
            "report_name": name,
            "telemetry_parameters": { ... },  # Should be JSON-safe
        }
    }

for example:

.. code-block:: python

    report_parameters = {
                "ccoop_telemetry_evse_status":{
                    "report_name_metadata":"ccoop_telemetry_evse_status",
                    "report_interval_secs_default":30,
                    "telemetry_parameters":{
                        "state":{
                            "r_id":"evse state",
                            "units":"NA",
                            "min_frequency":30,
                            "max_frequency":30,
                            "report_type":"",
                            "reading_type":"",
                            "method_name":"state",
                        },
                        "amp":{
                            "r_id":"evse charging current",
                            "units":"A",
                            "min_frequency":30,
                            "max_frequency":30,
                            "report_type":"",
                            "reading_type":"",
                            "method_name":"amp",
                        },
                        "wh":{
                            "r_id":"evse energy used in session",
                            "units":"Wh",
                            "min_frequency":30,
                            "max_frequency":30,
                            "report_type":"",
                            "reading_type":"",
                            "method_name":"wh",
                        },
                    },
                },
            }


Then, once the agent has been initialised, add new telemetry by running:

.. code-block:: python

    agent.add_telemetry_json(
            report_specifier_id="ccoop_telemetry_evse_status",
            values={"state": 1, "amp": 40, "wh": 50},
        )

This adds a TelemetryValue record to the VEN database.
The next time the report is sent, it sends this telemetry value record.
