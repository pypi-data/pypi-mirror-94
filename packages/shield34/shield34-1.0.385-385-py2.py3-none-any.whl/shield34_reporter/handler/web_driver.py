import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.handler import SeleniumMethodHandler
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.csv_rows.html.PageHtmlCsvRow import PageHtml
from shield34_reporter.model.csv_rows.html.WebElementHtmlCsvRow import WebElementHtml
from shield34_reporter.model.csv_rows.internalactions import WaitForNumberOfElementToBeMoreThanCsvRow, \
    WaitForElementPresenceCsvRow
from shield34_reporter.model.csv_rows.log_base_csv_row import PreDefenseLogCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_close_csv_row import WebDriverCloseCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_find_element_csv_row import WebDriverFindElementCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_find_elements_csv_row import WebDriverFindElementsCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_get_csv_row import WebDriverGetCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_quit_csv_row import WebDriverQuitCsvRow
from shield34_reporter.model.enums.action_name import ActionName
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.web_element_utils import WebElementUtils


class DriverFindElements(SeleniumMethodHandler):
    def __init__(self, driver, find_elements_method, by, locator):
        super(DriverFindElements, self).__init__(ActionName.WEB_DRIVER_FIND_ELEMENTS,
                                                 WebDriverFindElementsCsvRow(driver, by + ": " + locator))
        self.by = by
        self.locator = locator
        self.orig_by = by
        self.orig_locator = locator
        self.driver = driver
        self.located_web_elements = []
        self.find_elements = find_elements_method
        self.timeout = 4
        self.polling = 0.2

    def start_handle_hook(self):
        RunReportContainer.get_current_block_run_holder().update_find_element_counter()

    def do_orig_action(self):
        self.located_web_elements = self.find_elements(self.driver, self.by, self.locator)
        self._set_return_value(self.located_web_elements)
        return len(self.located_web_elements) > 0

    def action_pre_defenses(self):
        RunReportContainer.add_report_csv_row(PreDefenseLogCsvRow())
        before = time.time()
        try:

            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_driver_wait.until(EC.presence_of_all_elements_located(locator=(self.by, self.locator)))
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForNumberOfElementToBeMoreThanCsvRow(self.timeout, True, 0, (after-before)))
        except Exception as e:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForNumberOfElementToBeMoreThanCsvRow(self.timeout, False, 0, (after-before)))
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("find elements pre defenses failed.", e))

    def action_validation(self):
        return len(self.located_web_elements) > 0

    def on_successful_action(self):
        RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
        self._add_web_element_descriptor(self.driver, self.located_web_elements[0], self.orig_by, self.orig_locator)
        for elem in self.located_web_elements:
            RunReportContainer.get_current_block_run_holder().add_web_element(elem.id, self.by + ": " + self.locator)

    def handle_unsuccessful_action(self):
        should_relocate_element = ElementDynamicLocator.validate_current_find_element_worked_in_previous_runs(
            self.orig_by, self.orig_locator)
        if should_relocate_element:
            web_elements, current_by, current_value = ElementDynamicLocator.locate_elements_by_element_descriptor(
                self.driver, self.orig_by, self.orig_locator)
            if web_elements is not None and len(web_elements) > 0:
                self.by = current_by
                self.locator = current_value
                return True
        return False

    def handle_exception(self, exception):
        if isinstance(exception, TimeoutException):
            return self.handle_unsuccessful_action()
        if isinstance(exception, NoSuchElementException):
            return self.handle_unsuccessful_action()
        return False


class DriverFindElement(SeleniumMethodHandler):
    def __init__(self, obj, find_element_method, by, locator):
        super(DriverFindElement, self).__init__(ActionName.WEB_DRIVER_FIND_ELEMENT,
                                                WebDriverFindElementCsvRow(DriverUtils.get_current_driver(),
                                                                           by + ": " + locator))
        self.by = by
        self.locator = locator
        self.orig_by = by
        self.orig_locator = locator
        self.driver = obj
        self.located_web_element = None
        self.find_element = find_element_method

    def start_handle_hook(self):
        RunReportContainer.get_current_block_run_holder().update_find_element_counter()

    def do_orig_action(self):
        self.located_web_element = self.find_element(self.driver, self.by, self.locator)
        self._set_return_value(self.located_web_element)
        return self.located_web_element is not None

    def action_pre_defenses(self):
        RunReportContainer.add_report_csv_row(PreDefenseLogCsvRow())
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_driver_wait.until(EC.presence_of_element_located(locator=(self.by, self.locator)))
            after = time.time()
            RunReportContainer.add_report_csv_row(
                WaitForElementPresenceCsvRow(self.timeout, True, (after - before)))
        except Exception as e:
            after = time.time()
            RunReportContainer.add_report_csv_row(
                WaitForElementPresenceCsvRow(self.timeout, False, (after - before)))
            RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("find element pre defenses failed.", e))

    def on_successful_action(self):
        RunReportContainer.add_report_csv_row(
            WebElementHtml(
                WebElementUtils.get_element_html(self.located_web_element),
                WebElementUtils.get_element_computed_css(self.located_web_element,
                                                         self.driver),
                WebElementUtils.get_element_wrapping_html(self.located_web_element, 3)))
        RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
        self._add_web_element_descriptor(self.driver, self.located_web_element, self.orig_by, self.orig_locator)
        RunReportContainer.get_current_block_run_holder().add_web_element(self.located_web_element.id,
                                                                          self.by + ": " + self.locator)

    def handle_unsuccessful_action(self):
        try:
            should_relocate_element = ElementDynamicLocator.validate_current_find_element_worked_in_previous_runs(
                self.orig_by, self.orig_locator)
            if should_relocate_element:
                web_element, current_by, current_value = ElementDynamicLocator.locate_element_by_element_descriptor(self.driver,
                                                                                                      self.orig_by,
                                                                                                  self.orig_locator)
                if web_element is not None:
                    self.by = current_by
                    self.locator = current_value
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))
        return False

    def handle_exception(self, exception):
        if isinstance(exception, NoSuchElementException):
            return self.handle_unsuccessful_action()
        return False


class DriverGetUrl(SeleniumMethodHandler):
    def __init__(self, driver, get_url_method, url):
        super(DriverGetUrl, self).__init__(ActionName.WEB_DRIVER_GET, WebDriverGetCsvRow(driver, url))
        self.driver = driver
        self.url = url
        self.get_url = get_url_method
        self.take_snapshots = False

    def do_orig_action(self):
        self.get_url(self.driver, self.url)
        return True


class DriverQuit(SeleniumMethodHandler):
    def __init__(self, driver, quit_method):
        super(DriverQuit, self).__init__(ActionName.WEB_DRIVER_QUIT, WebDriverQuitCsvRow(driver))
        self.driver = driver
        self.quit = quit_method
        self.take_snapshots = False

    def do_orig_action(self):
        self.quit(self.driver)
        return True

    def action_pre_defenses(self):
        try:
            from shield34_reporter.listeners.listener_utils import ListenerUtils
            ListenerUtils.fetch_browser_logs()
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("driver quit pre defenses failed.", e))


class DriverClose(SeleniumMethodHandler):
    def __init__(self, driver, close_method):
        super(DriverClose, self).__init__(ActionName.WEB_DRIVER_CLOSE, WebDriverCloseCsvRow(driver))
        self.driver = driver
        self.close = close_method
        self.take_snapshots = False

    def do_orig_action(self):
        self.close(self.driver)
        return True

    def action_pre_defenses(self):
        try:
            if len(RunReportContainer.get_current_block_run_holder().proxyServers) == 1:
                var = RunReportContainer.get_current_block_run_holder().proxyServers[0].har
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("driver close pre defenses failed.", e))
