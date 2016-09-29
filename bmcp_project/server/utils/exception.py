from exceptions import Exception
from server.utils import log


class BmcpException(Exception):
    message = "An unkonwn message exception occurred."

    def __init__(self, message=None, **kwargs):
        if not message:
            try:
                message = self.message % kwargs
            except Exception as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                for name, value in kwargs.items():
                    log.error("%s: %s" % (name, value))

                message = self.message

        super(BmcpException, self).__init__(message)


class XClarityConnectionFailed(BmcpException):
    message = "Connection to xhmc failed: %(explanation)s"


class XClarityInternalFault(BmcpException):
    message = "Internal fault: %(explanation)s %(recovery)s"
