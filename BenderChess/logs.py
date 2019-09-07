import flask
from logging import Filter


class RequestFilter(Filter):
    """Add request info to log record"""

    def filter(self, record):
        if flask.has_request_context():
            record.ip = flask.request.environ.get('HTTP_X_REAL_IP',
                                                  flask.request.remote_addr)
            record.method = flask.request.method
            record.path = flask.request.path
        else:
            record.ip = '-'
            record.method = '-'
            record.path = '-'

        return True
