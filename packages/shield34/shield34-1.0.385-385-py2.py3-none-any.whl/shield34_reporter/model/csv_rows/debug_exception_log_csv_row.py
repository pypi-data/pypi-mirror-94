from shield34_reporter.model.csv_rows.helpers.exception_desc import ExceptionDesc
from shield34_reporter.model.csv_rows.log_base_csv_row import LogBaseCsvRow
from shield34_reporter.model.enums.row_sub_type import RowSubType


class DebugExceptionLogCsvRow(LogBaseCsvRow):

    log = ""
    expDesc = None
    exception = None

    def __init__(self, log, exception):
        self.log = log
        self.exception = exception
        self.expDesc = ExceptionDesc(exception)
        super(DebugExceptionLogCsvRow, self).__init__(RowSubType.DEBUG_EXCEPTION)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['expDesc', 'exception', 'log']
        row_value = {}
        for a in lst:
            lst_attr = getattr(self, a)
            if hasattr(lst_attr, 'gen_row_value'):
                row_value[a] = lst_attr.gen_row_value()
            else:
                row_value[a] = lst_attr
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), self.gen_row_value()]