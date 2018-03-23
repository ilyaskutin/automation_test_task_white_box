import signal

from tornado import log, web, ioloop, httpserver
from tornado.options import define, options, parse_command_line

from api.urls import api_urls

# common settings
define('debug', default=False, help='Debug mode and autoreload')
define('http_host', default='127.0.0.1', help='Tornado listen address')
define('http_port', default=8888, help='Tornado listen port')


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(
            api_urls,
            **options.as_dict()
        )


def main():
    def handler(signum, frame):
        ioloop.IOLoop.instance().stop()
        log.app_log.info('Server stopped!')

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    parse_command_line()
    application = Application()
    server = httpserver.HTTPServer(application)

    log.app_log.info(
        'Starting server...{}:{}'.format(options.http_host, options.http_port))
    server.bind(options.http_port, address=options.http_host)
    server.start()
    log.app_log.info('Server started!')
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
