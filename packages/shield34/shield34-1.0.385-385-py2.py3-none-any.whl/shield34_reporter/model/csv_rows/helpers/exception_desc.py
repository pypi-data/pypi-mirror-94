import sys
import traceback


class ExceptionDesc:

    message = ""
    cause = ""
    assertionError = False
    stackTrace = []
    additionalInfo = ""

    def __init__(self, exception):
        message = ''
        assertion_error = 'false'

        if getattr(exception, 'message', None) is not None:
            self.message = exception.message
        if getattr(exception, 'msg', None) is not None:
            self.message = exception.msg
        if getattr(exception, 'longrepr', None) is not None:
            longrepr = getattr(exception, 'longrepr')
            if getattr(longrepr, 'reprcrash', None) is not None:
                self.message = longrepr.reprcrash.message

        #self.cause = exception.cause

        if getattr(exception, 'assertionError', None) is not None:
            assertion_error = exception.assertionError
        self.assertionError = assertion_error

        etype, value, tb = sys.exc_info()
        if getattr(exception, 'stackTrace', None) is not None:
            self.stackTrace = exception.stackTrace
        else:
            self.stackTrace = traceback.format_tb(tb)

        #self.additionalInfo = exception.additionalInfo

    def gen_row_value(self, lst=['message', 'cause', 'assertionError', 'stackTrace', 'additionalInfo']):
        row_value = {}

        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value
