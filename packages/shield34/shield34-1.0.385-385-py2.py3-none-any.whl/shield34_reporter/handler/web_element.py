import time

from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException, TimeoutException, \
    NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.handler import SeleniumMethodHandler
from shield34_reporter.helpers import web_element_helper
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.csv_rows.html.PageHtmlCsvRow import PageHtml
from shield34_reporter.model.csv_rows.html.WebElementHtmlCsvRow import WebElementHtml
from shield34_reporter.model.csv_rows.internalactions import PutElementInViewPortCsvRow, WaitForElementVisibilityCsvRow, \
    WaitForElementClickabilityCsvRow, WaitForElementToBeWritableCsvRow, WaitForNumberOfElementToBeMoreThanCsvRow, \
    WaitForElementPresenceCsvRow
from shield34_reporter.model.csv_rows.log_base_csv_row import PreDefenseLogCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_clear_csv_row import WebElementClearCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_click_csv_row import WebElementClickCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_find_element_csv_row import WebElementFindElementCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_find_elements_csv_row import WebElementFindElementsCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_send_keys_csv_row import WebElementSendKeysCsvRow
from shield34_reporter.model.enums.action_name import ActionName
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.web_element_utils import WebElementUtils


class ElementFindElements(SeleniumMethodHandler):
    def __init__(self, driver, element, find_elements_method, by, locator):
        super(ElementFindElements, self).__init__(ActionName.WEB_ELEMENT_FIND_ELEMENTS, WebElementFindElementsCsvRow(
             element, driver, by + ": " + locator))
        self.by = by
        self.locator = locator
        self.orig_by = by
        self.orig_locator = locator
        self.parent_element = element
        self.located_web_elements = []
        self.find_elements = find_elements_method
        self.driver = driver

    def start_handle_hook(self):
        RunReportContainer.get_current_block_run_holder().update_find_element_counter()

    def do_orig_action(self):
        self.located_web_elements = self.find_elements(self.parent_element, self.by, self.locator)
        self._set_return_value(self.located_web_elements)
        return len(self.located_web_elements) > 0

    def action_pre_defenses(self):
        RunReportContainer.add_report_csv_row(PreDefenseLogCsvRow())
        before = time.time()
        try:

            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_driver_wait.until(EC.presence_of_all_elements_located(locator=(self.by, self.locator)))
            after = time.time()
            RunReportContainer.add_report_csv_row(
                WaitForNumberOfElementToBeMoreThanCsvRow(self.timeout, True, 0, (after - before)))
        except Exception as e:
            after = time.time()
            RunReportContainer.add_report_csv_row(
                WaitForNumberOfElementToBeMoreThanCsvRow(self.timeout, False, 0, (after - before)))
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("find elements pre defenses failed.", e))

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
        if isinstance(exception, NoSuchElementException):
            return self.handle_unsuccessful_action()
        return False


class ElementFindElement(SeleniumMethodHandler):
    def __init__(self, driver, element, find_element_method, by, locator):
        super(ElementFindElement, self).__init__(ActionName.WEB_ELEMENT_FIND_ELEMENT, WebElementFindElementCsvRow(element, driver, by + ": " + locator))
        self.by = by
        self.locator = locator
        self.orig_by = by
        self.orig_locator = locator
        self.parent_element = element
        self.located_web_element = None
        self.find_element = find_element_method
        self.driver = driver

    def start_handle_hook(self):
        RunReportContainer.get_current_block_run_holder().update_find_element_counter()

    def do_orig_action(self):
        self.located_web_element = self.find_element(self.parent_element, self.by, self.locator)
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
                WaitForElementPresenceCsvRow(self.timeout, False,  (after - before)))
            RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("find element pre defenses failed.", e))

    def on_successful_action(self):
        RunReportContainer.add_report_csv_row(
            WebElementHtml(
                WebElementUtils.get_element_html(self.located_web_element),
                WebElementUtils.get_element_computed_css(self.located_web_element, self.driver),
                WebElementUtils.get_element_wrapping_html(self.located_web_element, 3)))
        RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
        self._add_web_element_descriptor(self.driver, self.located_web_element, self.orig_by, self.orig_locator)
        RunReportContainer.get_current_block_run_holder().add_web_element(self.located_web_element.id, self.by + ": " + self.locator)

    def handle_unsuccessful_action(self):
        try:
            should_relocate_element = ElementDynamicLocator.validate_current_find_element_worked_in_previous_runs(
                self.orig_by, self.orig_locator)
            if should_relocate_element:
                web_element, current_by, current_value = ElementDynamicLocator.locate_element_by_element_descriptor(
                    self.driver,
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
        elif isinstance(exception, StaleElementReferenceException) or isinstance(exception, NoSuchElementException):
            self.parent_element = web_element_helper.reallocate_web_element(self.driver, self.parent_element)
            if self.parent_element is not None:
                return True
        return False


class ElementClickHandler(SeleniumMethodHandler):
    def __init__(self, driver, element, orig_click):
        super(ElementClickHandler, self).__init__(ActionName.WEB_ELEMENT_CLICK, WebElementClickCsvRow(element, driver))
        self.element = element
        self.orig_click = orig_click
        self.driver = driver
        self.use_js = False

    def action_pre_defenses(self):
        try:
            RunReportContainer.add_report_csv_row(PreDefenseLogCsvRow())
            self.wait_for_visibility()
            web_element_helper.put_element_in_view_port_old(self.driver, self.element)
            self.wait_for_enabled()
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("click element pre defenses failed.", e))

    def do_orig_action(self):
        if self.use_js:
            self.driver.execute_script('arguments[0].click();', self.element)
        else:
            self.orig_click(self.element)
        return True

    def handle_exception(self, exception):
        try:
            if isinstance(exception, ElementNotVisibleException) or isinstance(exception, ElementNotInteractableException) or isinstance(exception, ElementClickInterceptedException) or isinstance(exception, WebDriverException) and "is not clickable at point" in exception.msg:
                if not self._is_last_retry():
                    RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(False))
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", self.element)
                else:
                    self.use_js = True
                return True
            elif isinstance(exception, TimeoutException):
                self.timeout = self.timeout*2
                return True
            elif isinstance(exception, StaleElementReferenceException) or isinstance(exception, NoSuchElementException):
                self.element = web_element_helper.reallocate_web_element(self.driver, self.element)
                if self.element is not None:
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("click element handle exception failed.", e))
        return False

    def wait_for_visibility(self):
        element_is_visible = False
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_element_helper.wait_for_element_visibility(self.element, web_driver_wait)
            element_is_visible = True
        finally:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(self.timeout, element_is_visible, after - before))

    def wait_for_enabled(self):
        element_is_clickable = False
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_element_helper.wait_for_element_to_be_enabled(self.element, web_driver_wait)
            element_is_clickable = True
        finally:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForElementClickabilityCsvRow(self.timeout, element_is_clickable, after - before))


class ElementSendKeysHandler(SeleniumMethodHandler):
    def __init__(self, driver, element, orig_method, *value):
        super(ElementSendKeysHandler, self).__init__(ActionName.WEB_ELEMENT_SEND_KEYS, WebElementSendKeysCsvRow(
            element, driver, *value))
        self.element = element
        self.orig_send_keys = orig_method
        self.driver = driver
        self.value = value

    def action_pre_defenses(self):
        RunReportContainer.add_report_csv_row(PreDefenseLogCsvRow())
        try:
            self.wait_for_visibility()
            self.wait_for_enabled()
            self.wait_to_be_writeable()
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("send keys pre defenses failed.", e))

    def wait_for_visibility(self):
        element_is_visible = False
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_element_helper.wait_for_element_visibility(self.element, web_driver_wait)
            element_is_visible = True
        finally:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(self.timeout, element_is_visible, after - before))

    def wait_for_enabled(self):
        element_is_clickable = False
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_element_helper.wait_for_element_to_be_enabled(self.element, web_driver_wait)
            element_is_clickable = True
        finally:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForElementClickabilityCsvRow(self.timeout, element_is_clickable, after - before))

    def wait_to_be_writeable(self):
        element_is_visible = False
        before = time.time()
        try:
            web_driver_wait = WebDriverWait(self.driver, self.timeout, self.polling)
            web_element_helper.wait_for_textarea_to_be_writable(self.element, web_driver_wait)
            element_is_visible = True
        finally:
            after = time.time()
            RunReportContainer.add_report_csv_row(WaitForElementToBeWritableCsvRow(self.timeout, element_is_visible, after - before))

    def do_orig_action(self):
        self.orig_send_keys(self.element, *self.value)
        return True

    def handle_exception(self, exception):
        try:
            if isinstance(exception, ElementNotVisibleException) or isinstance(exception, ElementNotInteractableException ) and exception.message.contains("is not clickable at point"):
                RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(False))
                self.driver.execute_script("arguments[0].scrollIntoView(false);", self.element)
                return True
            elif isinstance(exception, TimeoutException):
                self.timeout = self.timeout*2
                return True
            elif isinstance(exception, StaleElementReferenceException) or isinstance(exception, NoSuchElementException):
                self.element = web_element_helper.reallocate_web_element(self.driver, self.element)
                if self.element is not None:
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("click element reallocate_web_element failed.", e))
        return False


class ElementClearHandler(SeleniumMethodHandler):
    def __init__(self, driver, element, orig_method):
        super(ElementClearHandler, self).__init__(ActionName.WEB_ELEMENT_CLEAR, WebElementClearCsvRow(
            element, driver))
        self.element = element
        self.clear = orig_method
        self.driver = driver

    def do_orig_action(self):
        self.clear(self.element)
        return True

    def action_pre_defenses(self):
        pass

    def action_validation(self):
        return True

    def on_successful_action(self):
        pass

    def handle_unsuccessful_action(self):
        return True

    def handle_exception(self, exception):
        try:
            if isinstance(exception, StaleElementReferenceException) or isinstance(exception, NoSuchElementException):
                self.element = web_element_helper.reallocate_web_element(self.driver, self.element)
                if self.element is not None:
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("clear element handle exception failed.", e))
        return False


