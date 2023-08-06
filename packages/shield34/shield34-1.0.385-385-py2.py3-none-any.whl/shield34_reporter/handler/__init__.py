import time
import traceback

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    StaleElementReferenceException, InvalidSelectorException, ErrorInResponseException, InvalidElementStateException, \
    ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.helpers import web_element_helper
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.csv_rows.exception_caught_csv_row import ExceptionCaughtCsvRow
from shield34_reporter.model.csv_rows.helpers.exception_desc import ExceptionDesc
from shield34_reporter.model.csv_rows.html.PageHtmlCsvRow import PageHtml
from shield34_reporter.model.csv_rows.internalactions import RetryActionCsvRow, PerformActionCsvRow, \
    ExceptionRecoveredCsvRow, PutElementInViewPortCsvRow, WaitForElementClickabilityCsvRow, \
    ClickElementAtSpecificPositionCsvRow
from shield34_reporter.model.csv_rows.log_base_csv_row import DebugLogCsvRow
from shield34_reporter.model.csv_rows.step_failed_csv_row import StepFailedCsvRow
from shield34_reporter.model.csv_rows.test_action.action_ended_csv_row import ActionEndedCsvRow
from shield34_reporter.model.csv_rows.test_action.action_started_csv_row import ActionStartedCsvRow
from shield34_reporter.model.enums.click_position import ClickPosition
from shield34_reporter.model.enums.exception_type import ExceptionType
from shield34_reporter.model.enums.placement import Placement
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.screen_shots import ScreenShot


class HandlerAPI(object):
    return_value = None

    def start_handle_hook(self):
        pass

    def do_orig_action(self):
        return False

    def action_pre_defenses(self):
        pass

    def action_validation(self):
        return True

    def on_successful_action(self):
        pass

    def handle_unsuccessful_action(self):
        return True

    def handle_exception(self, exception):
        return False

    def _set_return_value(self, value):
        self.return_value = value

    def _returned_value(self):
        return self.return_value


class SeleniumMethodHandler(HandlerAPI):
    value = None

    def __init__(self, action_name, action_csv_row):
        self.action_name = action_name
        self.action_csv_row = action_csv_row
        self.original_exception = None
        self.retry_count = 3
        self.retry_counter = 0
        self.timeout = 10
        self.polling = 0.2

    def _on_failed_action(self, exception):
        RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
        if not Shield34Properties.screenshots_on_failure_disabled:
            ScreenShot.capture_screen_shoot(self.action_name.value, Placement.AFTER_FAILURE.value)
        if exception is not None:
            RunReportContainer.add_report_csv_row(StepFailedCsvRow(ExceptionDesc(exception).message))
            raise exception

    def _add_web_element_descriptor(self, driver, web_element, by, locator):
        try:
            web_element_descriptor = ElementDynamicLocator.get_element_descriptor(web_element,
                                                                                  driver,
                                                                                  by, locator)
            if web_element_descriptor is not None:
                RunReportContainer.get_current_block_run_holder().webElementDescriptors.append(web_element_descriptor)
                RunReportContainer.get_current_block_run_holder().webElementDescriptorsMap[web_element.id] = web_element_descriptor
        except Exception as e:
            from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))

    def _is_last_retry(self):
        return self.retry_counter == self.retry_count-1

    def do_handle(self):
        timing_total = Timing("total")

        if not SdkAuthentication.is_authorized():
            self.do_orig_action()
            return self._returned_value()
        current_block_run = RunReportContainer.get_current_block_run_holder()
        if current_block_run is None:
            self.do_orig_action()
            return self._returned_value()
        if current_block_run.action_already_started():
            self.do_orig_action()
            return self._returned_value()

        self.start_handle_hook()
        timing_total.measure("start")
        RunReportContainer.add_report_csv_row(ActionStartedCsvRow())
        RunReportContainer.add_report_csv_row(self.action_csv_row)
        try:
            success = False
            failed_action = False
            self.retry_counter = 0
            forced_step = False
            while not success and self.retry_counter < self.retry_count and not failed_action:
                try:
                    if self.retry_counter > 0:
                        RunReportContainer.add_report_csv_row(RetryActionCsvRow(self.retry_counter, self.action_name))
                    self.retry_counter = self.retry_counter + 1
                    self.action_pre_defenses()

                    if not Shield34Properties.screenshots_disabled:
                        ScreenShot.capture_screen_shoot(self.action_name.value, Placement.BEFORE.value)
                    RunReportContainer.add_report_csv_row(PerformActionCsvRow(self.action_name.value, forced_step))
                    if self.do_orig_action() and self.action_validation():
                        self.on_successful_action()
                        success = True
                    else:
                        forced_step = True
                        failed_action = not self.handle_unsuccessful_action()
                except Exception as e:
                    RunReportContainer.add_report_csv_row(ExceptionCaughtCsvRow(exception=e, exception_type=ExceptionType.MAIN_ACTION))
                    if self.retry_counter == 1:
                        self.original_exception = e
                    if self.handle_exception(e):
                        forced_step = True
                        RunReportContainer.add_report_csv_row(
                            ExceptionRecoveredCsvRow(True, e, ExceptionType.INTERNAL_ACTION))
                    else:
                        failed_action = True

            if not success:
                self._on_failed_action(self.original_exception)
            return self._returned_value()
        finally:
            RunReportContainer.add_report_csv_row(ActionEndedCsvRow())

            timing_total.measure("end")
            timing_total.report()

    def _handle_element_exception(self, exception, driver, element, timeout, polling):
        try:
            if isinstance(exception, StaleElementReferenceException):
                element = web_element_helper.reallocate_web_element(driver, element)
                if element is not None:
                    return True, element

            if isinstance(exception, ElementClickInterceptedException):
                web_element_helper.click_at_center(element, driver)
                RunReportContainer.add_report_csv_row(
                    ClickElementAtSpecificPositionCsvRow(ClickPosition.CENTER, element))
                return True, element
            if isinstance(exception, ElementNotInteractableException):
                RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(False))
                driver.execute_script("arguments[0].scrollIntoView(false);", element)
                return True, element
            if isinstance(exception, ElementNotVisibleException):
                RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(False))
                driver.execute_script("arguments[0].scrollIntoView(false);", element)
                return True, element
            if isinstance(exception, ErrorInResponseException):
                # retry
                return True, element
            if isinstance(exception, InvalidElementStateException):
                before = time.time()
                web_driver_wait = WebDriverWait(driver, timeout, polling)
                web_element_helper.wait_for_element_to_be_enabled(element, web_driver_wait)
                after = time.time()
                RunReportContainer.add_report_csv_row(
                    WaitForElementClickabilityCsvRow(timeout, True, after - before))
                return True, element
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("handle element exception failed.", e))
        return False, element


    def _handle_lookup_exception(self, exception, driver, by, locator):
        try:
            if isinstance(exception, InvalidSelectorException) or isinstance(exception, NoSuchElementException):
                # try dynamic locator
                should_relocate_element = ElementDynamicLocator.validate_current_find_element_worked_in_previous_runs(
                    by, locator)
                if should_relocate_element:
                    web_element, current_by, current_value = ElementDynamicLocator.locate_element_by_element_descriptor(
                        driver,
                        by,
                        locator)
                    if web_element is not None:
                        return True, current_by, current_value
            if isinstance(exception, ErrorInResponseException):
                # retry
                return True, by, locator
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("handle lookup exception failed.", e))
        return False, by, locator




class Timing(object):
    def __init__(self, name):
        self.timestamps = []
        self.name = name

    def measure(self, label):
        self.timestamps.append((time.time(), label))

    def report(self):
        ts_after = self.timestamps[0]
        for ts in self.timestamps:
            ts_before = ts_after
            ts_after = ts
            RunReportContainer.add_report_csv_row(DebugLogCsvRow(
                self.name+" duration from " + str(ts_before[1]) + " to " + str(ts_after[1]) + " is " + str(
                    ts_after[0] - ts_before[0])))