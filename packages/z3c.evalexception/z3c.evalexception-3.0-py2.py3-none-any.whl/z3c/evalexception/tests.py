from io import BytesIO
import unittest

import mock

import z3c.evalexception

try:
    from StringIO import StringIO  # PY2
except ImportError:
    from io import StringIO


class WsgiMiddlewareTestCase(unittest.TestCase):

    app_factory = staticmethod(z3c.evalexception.test_application_factory)
    middleware_factory = None

    def setUp(self):
        global_conf = {}
        self.app = self.app_factory(global_conf)
        self.middleware = self.middleware_factory(self.app, global_conf)
        self.environ = {
            # http://wsgi.readthedocs.org/en/latest/definitions.html
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'PATH_INFO': '',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8080',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'HTTP_HOST': 'localhost:8080',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': BytesIO(),
            'wsgi.errors': StringIO(),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

    def request(self, **kwargs):
        environ = dict(self.environ)
        environ.update(kwargs)
        start_response = mock.Mock()
        body_iter = self.middleware(environ, start_response)
        return b''.join(body_iter)


class TestZopeEvalException(WsgiMiddlewareTestCase):

    middleware_factory = staticmethod(z3c.evalexception.zope_eval_exception)

    def test(self):
        body = self.request()
        self.assertIn(b'<title>Server Error</title>', body)
        self.assertIn(b'RuntimeError: The test application is raising this.',
                      body)


class TestPostMortemDebug(WsgiMiddlewareTestCase):

    middleware_factory = staticmethod(z3c.evalexception.post_mortem_debug)

    @mock.patch('pdb.post_mortem')
    def test(self, mock_post_mortem):
        with self.assertRaises(RuntimeError):
            self.request()
        self.assertEqual(mock_post_mortem.call_count, 1)


def DelayedCrashApplication(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    yield "Test Application"
    raise RuntimeError('The test application is raising this.')


class TestDelayedPostMortemDebug(TestPostMortemDebug):

    def app_factory(self, global_conf):
        return DelayedCrashApplication


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
