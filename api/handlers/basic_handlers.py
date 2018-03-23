import json
import sys

from tornado import log
from tornado.web import RequestHandler, HTTPError

if sys.version_info >= (3, 5):
    JSONDecodeError = json.decoder.JSONDecodeError
elif sys.version_info < (3, 5):
    JSONDecodeError = ValueError


class JSONHandler(RequestHandler):
    def prepare(self):
        self.remote_ip = self.request.headers.get('X-Real-IP') or self.request.remote_ip
        log.app_log.info('Access granted to %s for IP %s with token %s' % (
            self.__class__,
            self.remote_ip,
            self.request.headers.get('Auth-Token'))
        )

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.write({
            'error': self._reason
        })
        if not self._finished:
            self.finish()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Accept', 'application/json')

    def prepare(self):
        super().prepare()

        if self.request.method in ['POST']:
            self.prepare_post(self.request.body)

    def prepare_post(self, data):
        try:
            self.request_data = json.loads(data.decode())
            if not self.request_data:
                raise HTTPError(400, reason='Empty request')
            elif len(self.request_data) > 50:
                raise HTTPError(400, reason='Large request')

        except JSONDecodeError:
            raise HTTPError(400, reason='Invalid JSON format')

