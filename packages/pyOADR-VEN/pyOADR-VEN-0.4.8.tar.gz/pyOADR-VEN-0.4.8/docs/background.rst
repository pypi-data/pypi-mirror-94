Background
==========

OpenADR (Automated Demand Response) is a standard for alerting and responding to the need to adjust electric power consumption in response to fluctuations in grid demand.

OpenADR communications are conducted between Virtual Top Nodes (VTNs) and Virtual End Nodes (VENs).
In this implementation, a this agent is a VEN, implementing EiEvent and EiReport services in conformance with a subset of the OpenADR 2.0b specification.

The VEN receives VTN requests via the web service.

The VTN can 'call an event', indicating that a load-shed event should occur.
The VEN responds with an 'optIn' acknowledgment.

Events:
    The VEN agent maintains a persistent record of DR events.
    These events are stored in a sqlite database

Reporting:
    The VEN agent configuration defines telemetry values (data points) to be reported to the VTN.
    The VEN agent maintains a persistent record of reportable/reported telemetry values over time.

Supported requests/responses in the OpenADR VTN interface:
    VTN:
        oadrDistributeEvent (needed for event cancellation)
        oadrResponse
        oadrRegisteredReport
        oadrCreateReport
        oadrUpdatedReport
        oadrCancelReport
        oadrCreatedPartyRegistration
    VEN:
        oadrPoll
        oadrRequestEvent
        oadrCreatedEvent
        oadrResponse
        oadrRegisterReport
        oadrCreatedReport
        oadrUpdateReport
        oadrCanceledReport
        oadrCreatePartyRegistration
        oadrQueryRegistration


Event workflow (see OpenADR Profile Specification section 8.1)...

Event poll / creation:
    (VEN) oadrPoll
    (VTN) oadrDistributeEvent (all events are included; one oadrEvent element per event)
    (VEN) oadrCreatedEvent with optIn/optOut (if events had oadrResponseRequired)

        If "always", an oadrCreatedEvent must be sent for each event.
        If "never", it was a "broadcast" event -- never create an event in response.
        Otherwise, respond if event state (eventID, modificationNumber) has changed.

    (VTN) oadrResponse

Event change:
    (VEN) oadrCreatedEvent (sent if the optIn/optOut status has changed)
    (VTN) oadrResponse

Sample oadrDistributeEvent use case from the OpenADR Program Guide:

    Event:
        Notification: Day before event
        Start Time: midnight
        Duration: 24 hours
        Randomization: None
        Ramp Up: None
        Recovery: None
        Number of signals: 2
        Signal Name: simple

            Signal Type: level
            Units: LevN/A
            Number of intervals: equal TOU Tier change in 24 hours (2 - 6)
            Interval Duration(s): TOU tier active time frame (i.e. 6 hours)
            Typical Interval Value(s): 0 - 4 mapped to TOU Tiers (0 - Cheapest Tier)
            Signal Target: None

        Signal Name: ELECTRICITY_PRICE

            Signal Type: price
            Units: USD per Kwh
            Number of intervals: equal TOU Tier changes in 24 hours (2 - 6)
            Interval Duration(s): TOU tier active time frame (i.e. 6 hours)
            Typical Interval Value(s): $0.10 to $1.00 (current tier rate)
            Signal Target: None

        Event Targets: venID_1234
        Priority: 1
        VEN Response Required: always
        VEN Expected Response: optIn
    Reports:
        None

Report workflow (see OpenADR Profile Specification section 8.3)...

Report registration interaction:
    (VEN) oadrRegisterReport (METADATA report)
        VEN sends its reporting capabilities to VTN.
        Each report, identified by a reportSpecifierID, is described as elements and attributes.
    (VTN) oadrRegisteredReport (with optional oadrReportRequests)
        VTN acknowledges that capabilities have been registered.
        VTN optionally requests one or more reports by reportSpecifierID.
        Even if reports were previously requested, they should be requested again at this point.
    (VEN) oadrCreatedReport (if report requested)
        VEN acknowledges that it has received the report request and is generating the report.
        If any reports were pending delivery, they are included in the payload.
    (VTN) oadrResponse
        Why??

Report creation interaction:
    (VTN) oadrCreateReport
        See above - this is like the "request" portion of oadrRegisteredReport
    (VEN) oadrCreatedReport
        See above.

Report update interaction - this is the actual report:
    (VEN) oadrUpdateReport (report with reportRequestID and reportSpecifierID)
        Send a report update containing actual data values
    (VTN) oadrUpdatedReport (optional oadrCancelReport)
        Acknowledge report receipt, and optionally cancel the report

Report cancellation:
    (VTN) oadrCancelReport (reportRequestID)
        This can be sent to cancel a report that is in progress.
        It should also be sent if the VEN keeps sending oadrUpdateReport after an oadrUpdatedReport cancellation.
        If reportToFollow = True, the VEN is expected to send one final additional report.
    (VEN) oadrCanceledReport
        Acknowledge the cancellation.
        If any reports were pending delivery, they are included in the payload.

Key elements in the METADATA payload:
    reportSpecifierID: Report identifier, used by subsequent oadrCreateReport requests
    rid: Data point identifier

        This VEN reports only two data points: baselinePower, actualPower

    Duration: the amount of time that data can be collected
    SamplingRate.oadrMinPeriod: maximum sampling frequency
    SamplingRate.oadrMaxPeriod: minimum sampling frequency
    SamplingRate.onChange: whether or not data is sampled as it changes

For an oadrCreateReport example from the OpenADR Program Guide, see test/xml/sample_oadrCreateReport.xml.
