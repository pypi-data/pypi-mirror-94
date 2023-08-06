import json
import unittest

import requests
from uuid import uuid4

from requests import ReadTimeout, ConnectionError

import hoss_agent
try:
    from unittest.mock import MagicMock, patch, ANY
except ImportError:
    from mock import MagicMock, patch, ANY

from hoss_agent.conf.constants import EVENT

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


# test httplib instrumentation by calling higher level http client method and verify that we can capture the
# call correctly
@patch('hoss_agent.transport.base.Transport.queue')
@patch('hoss_agent.transport.base.Transport.start_thread')
@patch('hoss_agent.Client.start_threads')
class TestRequests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hoss_agent.init({
            "API_KEY": "API_KEY"
        })

    def test_basic_get(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/get?id=" + request_id
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'GET')
        self.assertEqual(event['request']['url'], url)
        self.assertEqual(event['request']['body'].getvalue(), b'')

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(request_id, response.json()['args']['id'])
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_post_with_body(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/post?id=" + request_id
        response = requests.post(url, data=json.dumps({'key': 'value'}))
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'POST')
        self.assertEqual(event['request']['url'], url)
        self.assertEqual(event['request']['body'].getvalue(), b'{"key": "value"}')

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(request_id, response.json()['args']['id'])
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_post_with_bytes_body(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/post?id=" + request_id
        response = requests.post(url, data=b'test')
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)
        self.assertEqual(event['request']['body'].getvalue(), b'test')

    def test_chunked(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/stream/1"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertEqual(body['args']['n'], '1')

    def test_gzip(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/gzip"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertTrue(body['gzipped'])

    def test_deflate(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/deflate"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertTrue(body['deflated'])

    def test_timeout(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/delay/2"
        try:
            requests.get(url, timeout=1)
        except ReadTimeout as ex:
            pass

        queue.assert_called_once_with(EVENT, ANY, False)
        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertFalse('response' in event)
        self.assertEqual(event['error']['type'], 'CONNECTION_TIMEOUT')
        self.assertEqual(event['error']['context']["timeout"], 1000)

    def test_connection_error(self, start_threads, transport_start_threads, queue):
        url = "https://fasdftasdfa-echo.com/delay/2"
        try:
            response = requests.get(url, timeout=1)
        except ConnectionError as ex:
            pass

        queue.assert_called_once_with(EVENT, ANY, False)
        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertFalse('response' in event)
        self.assertEqual(event['error']['type'], 'CONNECTION_ERROR')

    def test_connection_error_post(self, start_threads, transport_start_threads, queue):
        url = "https://fasdftasdfa-echo.com/delay/2"
        try:
            response = requests.post(url, data=json.dumps({'key': 'value'}))
        except ConnectionError as ex:
            pass

        queue.assert_called_once_with(EVENT, ANY, False)
        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertFalse('response' in event)
        self.assertEqual(event['error']['type'], 'CONNECTION_ERROR')
        self.assertEqual(event['request']['body'].getvalue(), b'{"key": "value"}')

    def test_file(self, start_threads, transport_start_threads, queue):
        url = "http://httpbin.org/post"
        with open('tests/instrumentations/test.txt', 'rb') as fp:
            files = {'upload_file': fp}
            values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
            r = requests.post(url, files=files, data=values)
        event = queue.call_args_list[0][0][1]
        self.assertTrue(event['request']['headers']['Content-Type'].startswith('multipart/form-data; boundary='))
        body = event['request']['body'].getvalue()
        # content of test.txt
        self.assertTrue('foobar' in body.decode())

