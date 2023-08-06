import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.handler import SeleniumMethodHandler, HandlerAPI
from shield34_reporter.model.csv_rows.internalactions import WaitForElementPresenceCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_wait_until_csv_row import WebDriverWaitUntilCsvRow
from shield34_reporter.model.enums.action_name import ActionName
from shield34_reporter.model.enums.row_sub_type import RowSubType
from shield34_reporter.utils.driver_utils import DriverUtils


class DriverWaitUntil(SeleniumMethodHandler):
    def __init__(self, web_driver_wait, wait_method, message, orig_method):
        self.until = orig_method
        self.web_driver_wait = web_driver_wait
        self.wait_method = wait_method
        self.message = message

        attributes = ''
        for key in wait_method.__dict__.keys():
            value = str(wait_method.__dict__[key])
            if attributes != '':
                attributes = attributes + ', '
            attributes = attributes + key + '=' + value
        super(DriverWaitUntil, self).__init__(ActionName.WEB_DRIVER_WAIT_UNTIL, WebDriverWaitUntilCsvRow(
            web_driver_wait._timeout, RowSubType.WAIT_FOR_CONDITION, type(wait_method).__name__, attributes))

        if isinstance(wait_method, presence_of_element_located):
            self.delegate = WaitPresenseOfElementLocated(self.web_driver_wait, wait_method, message, self.until, self)
        else:
            self.delegate = WaitBase(self.web_driver_wait, wait_method, message, self.until, self)

    def do_orig_action(self):
        return self.delegate.do_orig_action()

    def action_pre_defenses(self):
        self.delegate.action_pre_defenses()

    def action_validation(self):
        return self.delegate.action_validation()

    def on_successful_action(self):
        self.delegate.on_successful_action()

    def handle_unsuccessful_action(self):
        return self.delegate.handle_unsuccessful_action()

    def handle_exception(self, exception):
        if isinstance(exception, TimeoutException):
            return self.delegate.handle_exception(exception)
        return False


class WaitBase(HandlerAPI):
    def __init__(self, web_driver_wait, wait_method, message, until_method, parent):
        self.web_driver_wait = web_driver_wait
        self.wait_method = wait_method
        self.message = message
        self.until = until_method
        self.parent = parent

    def action_pre_defenses(self):
        pass

    def action_validation(self):
        return True

    def on_successful_action(self):
        self.after = time.time()

    def handle_unsuccessful_action(self):
        return True

    def handle_exception(self, timeout_exception):
        self.after = time.time()
        self.web_driver_wait._timeout = self.web_driver_wait._timeout*2
        return True

    def do_orig_action(self):
        self.before = time.time()
        value = self.until(self.web_driver_wait, self.wait_method, self.message)
        if value:
            self.parent._set_return_value(value)
        return True


class WaitPresenseOfElementLocated(HandlerAPI):
    def __init__(self, web_driver_wait, wait_method, message, until_method, parent):
        self.web_driver_wait = web_driver_wait
        self.wait_method = wait_method
        self.message = message
        self.until = until_method
        self.parent = parent
        self.locator = wait_method.locator

    def action_pre_defenses(self):
        pass

    def action_validation(self):
        return True

    def on_successful_action(self):
        RunReportContainer.add_report_csv_row(
            WaitForElementPresenceCsvRow(self.web_driver_wait._timeout, True,  (self.after - self.before)))


    def handle_unsuccessful_action(self):
        return True

    def handle_exception(self, timeout_exception):
        self.after = time.time()
        RunReportContainer.add_report_csv_row(
            WaitForElementPresenceCsvRow(self.web_driver_wait._timeout, False, (self.after - self.before)))
        web_element, current_by, current_value = ElementDynamicLocator.locate_element_by_element_descriptor(DriverUtils.get_current_driver(),
                                                               self.locator[0], self.locator[1])
        if web_element is not None:
            self.wait_method = expected_conditions.presence_of_element_located((current_by,current_value))
        else:
            self.web_driver_wait._timeout = self.web_driver_wait._timeout*2
        return True

    def do_orig_action(self):
        self.before = time.time()
        self.web_element = self.until(self.web_driver_wait, self.wait_method, self.message)
        self.after = time.time()
        self.parent._set_return_value(self.web_element)
        return self.web_element is not None