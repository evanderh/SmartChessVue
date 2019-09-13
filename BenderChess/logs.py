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
            record.requestID = flask.g.get('requestID', '-')[:6]
            record.status = flask.g.get('status', '-')
        else:
            record.ip = '-'
            record.method = '-'
            record.path = '-'
            record.requestID = '-'
            record.status = '-'

        return True
