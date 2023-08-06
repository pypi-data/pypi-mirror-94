import json
import unittest

from uuid import uuid4

import urllib3
from urllib3.exceptions import ConnectionError, TimeoutError, NewConnectionError

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

# Similar to test_requests (todo: share code somehow). The only difference is we
# use urllib3 http client here

@patch('hoss_agent.transport.base.Transport.queue')
@patch('hoss_agent.transport.base.Transport.start_thread')
@patch('hoss_agent.Client.start_threads')
class TestUrllib3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hoss_agent.init({
            "API_KEY": "API_KEY"
        })

    def test_basic_get(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/get?id=" + request_id
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        self.assertEqual(response.status, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'GET')
        self.assertEqual(event['request']['url'], url)
        self.assertEqual(event['request']['body'].getvalue(), b'')

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_post_with_body(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/post?id=" + request_id

        http = urllib3.PoolManager()
        response = http.request('POST',
                                url,
                                body=json.dumps({'key': 'value'}).encode('utf-8'),
                                headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['request']['method'], 'POST')
        self.assertEqual(event['request']['url'], url)
        self.assertEqual(event['request']['body'].getvalue(), b'{"key": "value"}')

        self.assertEqual(event['response']['statusCode'], 200)
        self.assertEqual(event['response']['headers'], dict(response.headers))

    def test_post_with_bytes_body(self, start_threads, transport_start_threads, queue):
        request_id = str(uuid4())
        url = "https://postman-echo.com/post?id=" + request_id

        http = urllib3.PoolManager()
        response = http.request('POST',
                                url,
                                body=b'test',
                                headers={'Content-Type': 'application/json'})
        queue.assert_called_once_with(EVENT, ANY, False)

        event = queue.call_args_list[0][0][1]

        self.assertEqual(event['request']['body'].getvalue(), b'test')


    def test_chunked(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/stream/1"
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        self.assertEqual(response.status, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertEqual(body['args']['n'], '1')
        self.assertTrue(body['url'].endswith("postman-echo.com/stream/1"))

    def test_gzip(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/gzip"
        http = urllib3.PoolManager()
        response = http.request('GET', url)

        self.assertEqual(response.status, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertTrue(body['gzipped'])

    def test_deflate(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/deflate"
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        self.assertEqual(response.status, 200)
        queue.assert_called_once_with(EVENT, ANY, False)

        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertEqual(event['response']['statusCode'], 200)
        body = json.loads(event['response']['body'].getvalue().decode())
        self.assertTrue(body['deflated'])

    def test_timeout(self, start_threads, transport_start_threads, queue):
        url = "https://postman-echo.com/delay/2"
        http = urllib3.PoolManager()
        try:
            http.request('GET', url, timeout=1, retries=False)
        except TimeoutError:
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
            http = urllib3.PoolManager()
            http.request('GET', url, retries=False)
        except NewConnectionError as ex:
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
            http = urllib3.PoolManager()
            http.request('POST', url, retries=False,
                         body=json.dumps({'key': 'value'}).encode('utf-8'),
                         headers={'Content-Type': 'application/json'})
        except NewConnectionError as ex:
            pass

        queue.assert_called_once_with(EVENT, ANY, False)
        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertFalse('response' in event)
        self.assertEqual(event['error']['type'], 'CONNECTION_ERROR')
        self.assertEqual(event['request']['body'].getvalue(), b'{"key": "value"}')

    def test_file(self, start_threads, transport_start_threads, queue):
        url = "https://fasdftasdfa-echo.com/delay/2"
        try:
            http = urllib3.PoolManager()
            http.request('GET', url, retries=False)
        except NewConnectionError as ex:
            pass

        queue.assert_called_once_with(EVENT, ANY, False)
        event_type = queue.call_args_list[0][0][0]
        event = queue.call_args_list[0][0][1]
        self.assertEqual(event_type, EVENT)

        self.assertFalse('response' in event)
        self.assertEqual(event['error']['type'], 'CONNECTION_ERROR')

    def test_file(self, start_threads, transport_start_threads, queue):
        url = "http://httpbin.org/post"
        http = urllib3.PoolManager()
        with open('tests/instrumentations/test.txt', 'rb') as fp:
            file_data = fp.read()
            http.request('POST', url, fields={
                'filefield': ('test.txt', file_data , 'text/plain'),
            })
        event = queue.call_args_list[0][0][1]
        self.assertTrue(event['request']['headers']['Content-Type'].startswith('multipart/form-data; boundary='))
        body = event['request']['body'].getvalue()
        # content of test.txt
        self.assertTrue('foobar' in body.decode())
