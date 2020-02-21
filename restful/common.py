import logging
from datetime import datetime, date
import json
import ast

import werkzeug.wrappers

_logger = logging.getLogger(__name__)


def default(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()


def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {"count": len(data), "data": data}
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )


def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    # return json.dumps({})
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {
                "type": typ,
                "message": str(message)
                if str(message)
                else "wrong arguments (missing validation)",
            },
            default=datetime.datetime.isoformat,
        ),
    )


def extract_arguments(payloads, offset=0, limit=0, order=None):
    """Parse additional data  sent along request."""
    fields, domain, payload = [], [], {}
    date_from = False
    date_to = False
    employee_id = False

    if payloads.get("domain", None):
        domain = ast.literal_eval(payloads.get("domain"))
    if payloads.get("fields"):
        fields += payloads.get("fields")
    if payloads.get("offset"):
        offset = int(payloads.get("offset"))
    if payloads.get("limit"):
        limit = int(payloads.get("limit"))
    if payloads.get("order"):
        order = payloads.get("order")
    if payloads.get("date_from"):
        date_from = datetime.strptime(payloads.get("date_from"), '%Y/%m/%dT%H:%M:%S-06:00')
        payloads["date_from"] = date_from
    if payloads.get("date_to"):
        date_to = datetime.strptime(payloads.get("date_to"), "%Y/%m/%dT%H:%M:%S-06:00")
        payloads["date_to"] = date_to
    if payloads.get("employee_id"):
        employee_id = int(payloads.get("employee_id"))
        payloads["employee_id"] = employee_id
    return [domain, fields, offset, limit, order, date_from, date_to, employee_id]
