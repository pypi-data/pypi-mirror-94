import json

from shield34_reporter.model.csv_rows.report_csv_row import ReportCsvRow
from shield34_reporter.model.enums.row_sub_type import RowSubType
from shield34_reporter.model.enums.row_type import RowType


class LogBaseCsvRow(ReportCsvRow):
    def __init__(self, row_sub_type):
        self.rowType = RowType.LOGS
        super(LogBaseCsvRow, self).__init__(row_sub_type)


class PreDefenseLogCsvRow(LogBaseCsvRow):
    def __init__(self):
        super(PreDefenseLogCsvRow, self).__init__(RowSubType.PRE_DEFENSES)

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value),str(self.rowType.value), "{}"]


class DebugLogCsvRow(LogBaseCsvRow):
    def __init__(self, log):
        self.log = log[0:124]
        super(DebugLogCsvRow, self).__init__(RowSubType.DEBUG)

    def gen_row_value(self, lst=['log']):
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]