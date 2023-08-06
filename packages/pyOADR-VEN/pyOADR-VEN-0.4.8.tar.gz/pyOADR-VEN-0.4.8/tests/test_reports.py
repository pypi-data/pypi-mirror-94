import logging
import time
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from time_machine import travel
from pony import orm
from voluptuous import Invalid

from pyoadr_ven import database
from pyoadr_ven import OpenADRVenAgent
from pyoadr_ven.enums import ReportStatus
from tests.conftest import CA_PATH
from tests.conftest import CERT_PATH
from tests.factories import ReportFactory

_LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.pony

TELEMETRY_PARAMS = {
    "state": {
        "r_id": "evse state",
        "units": "NA",
        "min_frequency": 30,
        "max_frequency": 30,
        "report_type": "",
        "reading_type": "",
        "method_name": "state",
    },
    "amp": {
        "r_id": "evse charging current",
        "units": "A",
        "min_frequency": 30,
        "max_frequency": 30,
        "report_type": "",
        "reading_type": "",
        "method_name": "amp",
    },
    "wh": {
        "r_id": "evse energy used in session",
        "units": "Wh",
        "min_frequency": 30,
        "max_frequency": 30,
        "report_type": "",
        "reading_type": "",
        "method_name": "wh",
    },
}

REPORT_PARAMS = {
    "ccoop_telemetry_evse_status": {
        "report_name_metadata": "ccoop_telemetry_evse_status",
        "report_interval_secs_default": 30,
        "telemetry_parameters": TELEMETRY_PARAMS,
    }
}

MOCK_VTN_ADDRESS = "https://openadr-staging"
MOCK_VEN_ID = "ven01"
MOCK_VTN_ID = "vtn01"
LOCAL_VTN_ADDRESS = "http://localhost:3000"
LOCAL_VEN_ID = "1"
LOCAL_VTN_ID = "ccoopvtn01"


class TestReportParameters:
    def test_invalid_report_parameters_raise_exception(self):
        invalid_report_params = REPORT_PARAMS = {
            "ccoop_telemetry_evse_status": {
                "report_name_metadata": "ccoop_telemetry_evse_status",
                "report_interal_secs_default": 30,
                "telemetry_parameters": TELEMETRY_PARAMS,
            }
        }
        with pytest.raises(Invalid):
            agent = OpenADRVenAgent(
                ven_id=LOCAL_VEN_ID,
                vtn_id=LOCAL_VTN_ID,
                vtn_address=LOCAL_VTN_ADDRESS,
                security_level="standard",
                poll_interval_secs=5,
                log_xml=True,
                opt_timeout_secs=30,
                opt_default_decision="optIn",
                report_parameters=REPORT_PARAMS,
                client_pem_bundle=CERT_PATH,
                vtn_ca_cert=CA_PATH,
            )

    def test_blank_report_parameters_valid(self):

        agent = OpenADRVenAgent(
            ven_id=LOCAL_VEN_ID,
            vtn_id=LOCAL_VTN_ID,
            vtn_address=LOCAL_VTN_ADDRESS,
            security_level="standard",
            poll_interval_secs=5,
            log_xml=True,
            opt_timeout_secs=30,
            opt_default_decision="optIn",
            report_parameters={},
            client_pem_bundle=CERT_PATH,
            vtn_ca_cert=CA_PATH,
        )


class TestReportCreationRegistration:
    @pytest.mark.local
    def test_inactive_report_created_on_register_report(self, mocked_agent):

        mocked_agent.send_oadr_register_report()

        assert orm.select(r for r in database.Report).count() == 1

        test_report = orm.select(r for r in database.Report).first()
        assert test_report
        assert test_report.specifier_id == "ccoop_telemetry_evse_status"
        assert test_report.status == ReportStatus.INACTIVE.value

    @pytest.mark.local
    def test_handle_oadr_registered_report_works(self, caplog):
        """
        To run this test you need to ensure the following:
            #. Start your VTN server
                * note the url it comes up on - if it isn't localhost:3000,
                    change the LOCAL_VTN_ADDRESS variable

            #. Go to the Admin page of the VTN and create a certificate authority called ``default``
                * save the CA certificate in the tests folder as 'ca.crt'
            #. Still in the VTN Admin page, create a certificate
                * save the certificate and private key in the tests folder as 'client.pem'

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


            #. Now, using the main VTN interface (not the Django admin), create a VEN
                on the VTN - you will need to create a Customer and Site to do this.
                * set the LOCAL_VEN_ID variable to the ven_id you used
                * Note the LOCAL_VTN_ID used (see base.py in the VTN repo)

            #. Using the Django admin, create a DRProgram on the VTN
                * Add your VEN/site to this program

        Each time you run the test, it is better to have a clean VTN database.
        Open a django shell and remove all of the Reports and Telemetry objects.

        """
        caplog.set_level(logging.INFO)
        agent = OpenADRVenAgent(
            ven_id=LOCAL_VEN_ID,
            vtn_id=LOCAL_VTN_ID,
            vtn_address=LOCAL_VTN_ADDRESS,
            security_level="standard",
            poll_interval_secs=5,
            log_xml=True,
            opt_timeout_secs=30,
            opt_default_decision="optIn",
            report_parameters=REPORT_PARAMS,
            client_pem_bundle=CERT_PATH,
            vtn_ca_cert=CA_PATH,
        )
        agent.send_oadr_register_report()
        agent.tick()
        # agent.reports_registered = True
        assert orm.select(r for r in database.Report).count() == 1
        test_report = orm.select(r for r in database.Report).first()
        agent.process_report(test_report.id)
        assert test_report.status == ReportStatus.ACTIVE.value
        agent.add_telemetry_json(
            report_specifier_id=test_report.specifier_id,
            values={"state": 1, "amp": 40, "wh": 50},
        )
        tel = agent.get_new_telemetry_for_report(
            report_specifier_id=test_report.specifier_id
        )
        assert len(tel) == 1
        # while True:
        #     time.sleep(6)
        #     agent.tick()


class TestReportStatusHelpers:
    def test_inactive_report_in_active_or_pending(self, mocked_agent):
        report = ReportFactory(status=ReportStatus.INACTIVE.value)
        assert report.status == ReportStatus.INACTIVE.value
        assert report.is_active_or_pending
        assert report in mocked_agent.active_or_pending_reports

    def test_active_report_in_active_or_pending(self, mocked_agent):
        report = ReportFactory(status=ReportStatus.ACTIVE.value)
        assert report.status == ReportStatus.ACTIVE.value
        assert report.is_active_or_pending
        assert report in mocked_agent.active_or_pending_reports

    def test_completed_report_not_in_active_or_pending(self, mocked_agent):
        report = ReportFactory(status=ReportStatus.COMPLETED.value)
        assert report.status == ReportStatus.COMPLETED.value
        assert report.is_active_or_pending is False
        assert report not in mocked_agent.active_or_pending_reports

    def test_canceled_report_not_in_active_or_pending(self, mocked_agent):
        report = ReportFactory(status=ReportStatus.CANCELED.value)
        assert report.status == ReportStatus.CANCELED.value
        assert report.is_active_or_pending is False
        assert report not in mocked_agent.active_or_pending_reports


class TestWithTimeMovingOn:
    @pytest.mark.local
    def test_active_report_becomes_complete(self, mocked_agent):
        initial_datetime = datetime(year=2019, month=1, day=1, hour=10, minute=0)
        with travel(initial_datetime) as traveller:
            report = ReportFactory(
                start_time=initial_datetime,
                end_time=datetime.utcnow() + timedelta(hours=1),
                created=initial_datetime,
                status=ReportStatus.ACTIVE.value,
            )
            mocked_agent.process_report(report.id)
            assert report.status == ReportStatus.ACTIVE.value
            traveller.tick(delta=timedelta(hours=2))
            mocked_agent.process_report(report.id)
            assert report.status == ReportStatus.COMPLETED.value
