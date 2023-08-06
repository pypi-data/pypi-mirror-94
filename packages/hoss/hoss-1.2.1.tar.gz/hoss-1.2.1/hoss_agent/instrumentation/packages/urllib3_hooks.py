import base64
import functools
import time
from uuid import uuid4

import wrapt
from urllib3.exceptions import NewConnectionError, TimeoutError

from hoss_agent.conf.constants import EVENT
from hoss_agent.context import execution_context
from hoss_agent.utils.buffer_proxy import BufferProxy
from hoss_agent.utils.compat import BytesIO
from hoss_agent.utils.logging import get_logger

logger = get_logger("hoss_agent.instrumentaion.packages.urllib3_hooks")


def install(module):
    wrapt.wrap_function_wrapper(
        module,
        "connectionpool.HTTPConnectionPool._make_request", _make_request,
    )
    wrapt.wrap_function_wrapper(
        module,
        "response.HTTPResponse.read", read,
    )

    wrapt.wrap_function_wrapper(
        module, "response.HTTPResponse.stream", _response_stream
    )

    wrapt.wrap_function_wrapper(
        module,
        "response.HTTPResponse.release_conn",
        _response_release_conn,
    )


# Instrument urllib3 connectionpool _make_request to capture connection error (both dns & connection timeout error)
# We're doing this at a higher level than httplib since the connection is httplib does't receive the full set of params
# (url, headers, etc...)
def _make_request(wrapped, instance, args, kwargs):
    request_received_at = int(round(time.time() * 1000))
    conn, method, url = args
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:
        _capture_error(conn, method, instance.scheme, instance.host, url, kwargs.get('body'),
                       kwargs.get('headers'), request_received_at, e)
        raise e


def _capture_error(connection, method, scheme, host, url, body, headers, request_received_at, error):
    try:
        client = execution_context.get_client()
        if isinstance(error, NewConnectionError):
            error = {
                "type": 'CONNECTION_ERROR',
                "context": {
                    "error": str(error)
                },
                "receivedAt": int(round(time.time() * 1000))
            }
        elif isinstance(error, TimeoutError):
            error = {
                "type": 'CONNECTION_TIMEOUT',
                "context": {
                    "error": str(error),
                    "timeout": connection.timeout * 1000
                },
                "receivedAt": int(round(time.time() * 1000))
            }
        else:
            error = {
                "type": 'CONNECTION_ERROR',
                "context": {
                    "error": str(error),
                },
                "receivedAt": int(round(time.time() * 1000))
            }
        req_body = BytesIO()
        if body is not None:
            if isinstance(body, bytes):
                req_body.write(body)
            elif isinstance(body, str):
                req_body.write(body.encode("utf-8"))
        event = {
            "eventId": uuid4(),
            "type": "OutboundHTTP",
            "request": {
                "method": method,
                "headers": dict(headers),
                "body": req_body,
                "url": "%s://%s%s" % (
                    scheme,
                    host,
                    url,
                ),
                "receivedAt": request_received_at
            },
            "error": error
        }
        client.queue(EVENT, event)
    except Exception as ex:
        logger.debug('Error capturing urllib.HTTPConnectionPool._make_request', ex)


def _response_release_conn(wrapped, instance, args, kwargs):
    rv = wrapped(*args, **kwargs)
    try:
        response = getattr(instance, "_original_response")
        hoss_context = getattr(response, "_hoss_context", None)
        if not hoss_context:
            return rv

        if 'queued' not in hoss_context['event']:
            hoss_context['event']['queued'] = True
            hoss_context['client'].queue(EVENT, hoss_context['event'])

    except Exception as ex:
        pass
    return rv


def _response_stream(wrapped, instance, args, kwargs):
    response = getattr(instance, "_original_response")
    hoss_context = getattr(response, "_hoss_context", None)

    if not hoss_context or 'response_proxy' in hoss_context:
        return wrapped(*args, **kwargs)

    stream = wrapped(*args, **kwargs)
    proxy = BufferProxy(stream, hoss_context['event']['response']['body'])

    hoss_context['response_proxy'] = True

    return proxy


# this hooks into urllib3.response
def read(wrapped, instance, args, kwargs):
    rv = wrapped(*args, **kwargs)
    try:
        hoss_context = getattr(instance._original_response, "_hoss_context", None)
        if not hoss_context:
            return rv
        if not hoss_context.get('response_proxy'):
            hoss_context['event']['response']['body'].write(rv)

        if instance.closed:
            logger.debug('Response is closed after read. Queue event')
            if 'queued' not in hoss_context['event']:
                hoss_context['event']['queued'] = True
                hoss_context['client'].queue(EVENT, hoss_context['event'])
    except Exception as ex:
        logger.debug('Error in monkey-patched urllib3.response.read: %s', ex)

    return rv

