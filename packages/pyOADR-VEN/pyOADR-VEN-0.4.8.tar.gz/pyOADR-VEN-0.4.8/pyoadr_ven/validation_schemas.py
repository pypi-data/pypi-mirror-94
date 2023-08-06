from voluptuous import Schema

internal_schema = Schema(
    {
        "report_name_metadata": str,
        "report_interval_secs_default": int,
        "telemetry_parameters": dict,
    },
    required=True,
)
REPORT_PARAMETER_SCHEMA = Schema({str: internal_schema})
