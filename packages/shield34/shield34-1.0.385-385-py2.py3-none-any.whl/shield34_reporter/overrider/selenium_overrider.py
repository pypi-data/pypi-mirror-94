from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
# def create_function(orgin_func,name, args):
#     def y():
#         print("s")
#         orgin_func(args)
#         pass
#
#
#     y_code = types.CodeType(orgin_func.__code__.co_argcount,
#                             orgin_func.__code__.co_kwonlyargcount,
#                             orgin_func.__code__.co_nlocals,
#                             orgin_func.__code__.co_stacksize,
#                             orgin_func.__code__.co_flags,
#                             y.__code__.co_code,
#                             orgin_func.__code__.co_consts,
#                             orgin_func.__code__.co_names,
#                             orgin_func.__code__.co_varnames,
#                             y.__code__.co_filename,
#                             name,
#                             y.__code__.co_firstlineno,
#                             y.__code__.co_lnotab)
#
#     return types.FunctionType(y_code, orgin_func.__globals__, name)
from selenium.webdriver.support.wait import WebDriverWait

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.handler.action_chains import *
from shield34_reporter.handler.web_driver import DriverFindElements, DriverFindElement, DriverGetUrl, DriverQuit, \
    DriverClose
from shield34_reporter.handler.web_driver_wait import DriverWaitUntil
from shield34_reporter.handler.web_element import ElementFindElements, ElementFindElement, ElementClickHandler, \
    ElementSendKeysHandler, ElementClearHandler
from shield34_reporter.model.csv_rows.log_base_csv_row import DebugLogCsvRow
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.reporter_proxy import ReporterProxy, ProxyServerNotInitializedException


class SeleniumOverrider(object):
    is_overrided = False

    @staticmethod
    def override():
        if not SeleniumOverrider.is_overrided and SdkAuthentication.isAuthorized:
            WebElementOverrider.override()
            WebDriverOverrider.override()
            ActionsOverrider().override()
            WebDriverWaitOverrider.override()
            SeleniumOverrider.is_overrided = True


class WebElementOverrider:
    @staticmethod
    def override():
        WebElement.org_find_elements = WebElement.find_elements
        WebElement.find_elements = lambda element, by, value=None: ElementFindElements(
            DriverUtils.get_current_driver(), element, WebElement.org_find_elements, by, value).do_handle()

        WebElement.org_find_element = WebElement.find_element
        WebElement.find_element = lambda element, by, value=None: ElementFindElement(
            DriverUtils.get_current_driver(), element, WebElement.org_find_element, by, value).do_handle()

        WebElement.org_click = WebElement.click
        WebElement.click = lambda element: ElementClickHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_click).do_handle()

        WebElement.org_send_keys = WebElement.send_keys
        WebElement.send_keys = lambda element, keys: ElementSendKeysHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_send_keys, keys).do_handle()

        WebElement.org_clear = WebElement.clear
        WebElement.clear = lambda element: ElementClearHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_clear).do_handle()


class WebDriverOverrider(object):
    @staticmethod
    def override():

        WebDriver.org_init = WebDriver.__init__

        def init_web_driver(self, command_executor='http://127.0.0.1:4444/wd/hub',
                            desired_capabilities=None, browser_profile=None, proxy=None,
                            keep_alive=False, file_detector=None, options=None):
            updated_desired_capabilities = desired_capabilities
            if SdkAuthentication.is_authorized():
                if updated_desired_capabilities is None:
                    updated_desired_capabilities = {}
                updated_desired_capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
                updated_desired_capabilities['acceptInsecureCerts'] = True

                if ReporterProxy.start_proxy_management_server():
                    if options is None:
                        options = webdriver.ChromeOptions()
                    proxies_count = len(RunReportContainer.get_current_block_run_holder().proxyServers)
                    if proxies_count > 0:
                        RunReportContainer.get_current_block_run_holder().proxyServers[
                            proxies_count - 1].add_to_capabilities(updated_desired_capabilities)
                    else:
                        raise ProxyServerNotInitializedException()
                    if options is not None and isinstance(options, webdriver.ChromeOptions):
                        options.add_argument('--ignore-certificate-errors')
                        options.add_argument('--ignore-ssl-errors')
            RunReportContainer.current_driver = self
            RunReportContainer.driver_counter = RunReportContainer.driver_counter + 1
            WebDriver.org_init(self, command_executor, updated_desired_capabilities, browser_profile, proxy, keep_alive,
                               file_detector, options)

        WebDriver.__init__ = init_web_driver

        WebDriver.org_find_elements = WebDriver.find_elements
        WebDriver.find_elements = lambda obj, by, value=None: DriverFindElements(obj, WebDriver.org_find_elements, by,
                                                                                 value).do_handle()

        WebDriver.org_find_element = WebDriver.find_element
        WebDriver.find_element = lambda obj, by, value=None: DriverFindElement(obj, WebDriver.org_find_element, by,
                                                                               value).do_handle()

        WebDriver.org_get = WebDriver.get
        WebDriver.get = lambda obj, url: DriverGetUrl(obj, WebDriver.org_get, url).do_handle()

        WebDriver.org_quit = WebDriver.quit
        WebDriver.quit = lambda obj: DriverQuit(obj, WebDriver.org_quit).do_handle()

        WebDriver.org_close = WebDriver.close
        WebDriver.close = lambda obj: DriverClose(obj, WebDriver.org_close).do_handle()

        WebDriver.org_execute_script = WebDriver.execute_script

        def shield_execute_script(obj, script, *args):
            if RunReportContainer.get_current_block_run_holder().action_started_count == 0:
                RunReportContainer.add_report_csv_row(DebugLogCsvRow(script))
            return WebDriver.org_execute_script(obj, script, *args)

        WebDriver.execute_script = shield_execute_script


class ActionsOverrider(object):
    def override(self):
        driver = DriverUtils.get_current_driver()
        self.override_init(driver)
        self.override_reset(driver)
        self.override_perform(driver)
        self.override_click()
        self.override_click_and_hold()
        self.override_context_click()
        self.override_double_click()
        self.override_drag_and_drop_by_offset()
        self.override_drag_and_drop()
        self.override_key_down()
        self.override_key_up()
        self.override_move_by_offset()
        self.override_send_keys()
        self.override_send_keys_to_element()
        self.override_move_to_element()
        self.override_move_to_element_with_offset()

    @staticmethod
    def override_click():
        ActionChains.orig_click = ActionChains.click

        def action_chains_click(action_chains, on_element=None):
            if is_already_in_action():
                ActionChains.orig_click(action_chains, on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsClick(DriverUtils.get_current_driver(), action_chains, ActionChains.orig_click, on_element))
            return action_chains

        ActionChains.click = action_chains_click

    @staticmethod
    def override_click_and_hold():
        ActionChains.orig_click_and_hold = ActionChains.click_and_hold

        def action_chains_click_and_hold(action_chains, on_element=None):
            if is_already_in_action():
                ActionChains.orig_click_and_hold(action_chains, on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsClickAndHold(DriverUtils.get_current_driver(), action_chains,
                                             ActionChains.orig_click_and_hold, on_element))
            return action_chains

        ActionChains.click_and_hold = action_chains_click_and_hold

    def override_init(self, driver):
        ActionChains.org_init = ActionChains.__init__

        def init_action_chains(self, driver):
            self.shield34_actions = []
            ActionChains.org_init(self, driver)

        ActionChains.__init__ = init_action_chains

    @staticmethod
    def override_reset(driver):
        ActionChains.orig_reset_actions = ActionChains.reset_actions

        def reset_action_chains(action_chains):
            action_chains.shield34_actions = []

        ActionChains.reset_actions = reset_action_chains

    @staticmethod
    def override_perform(driver):
        ActionChains.orig_perform = ActionChains.perform

        def perform_action_chains(action_chains):
            for action in action_chains.shield34_actions:
                action.do_handle()
        ActionChains.perform = perform_action_chains

    @staticmethod
    def override_context_click():
        ActionChains.orig_context_click = ActionChains.context_click

        def action_chains_context_click(action_chains, on_element=None):
            if is_already_in_action():
                ActionChains.orig_context_click(action_chains,on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsContextClick(DriverUtils.get_current_driver(), action_chains,
                                             ActionChains.orig_context_click, on_element))
            return action_chains

        ActionChains.context_click = action_chains_context_click

    @staticmethod
    def override_double_click():
        ActionChains.orig_double_click = ActionChains.double_click

        def action_chains_double_click(action_chains, on_element=None):
            if is_already_in_action():
                ActionChains.orig_double_click(action_chains,on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsDoubleClick(DriverUtils.get_current_driver(), action_chains, ActionChains.orig_double_click,
                                            on_element))
            return action_chains

        ActionChains.double_click = action_chains_double_click

    @staticmethod
    def override_drag_and_drop_by_offset():
        ActionChains.orig_drag_and_drop_by_offset = ActionChains.drag_and_drop_by_offset

        def action_chains_drag_and_drop_by_offset(action_chains, source, xoffset, yoffset):
            if is_already_in_action():
                ActionChains.orig_drag_and_drop_by_offset(action_chains, source, xoffset, yoffset)
            else:
                action_chains.shield34_actions.append(ActionChainsDragDropOffset(DriverUtils.get_current_driver(),
                                                                                 action_chains,
                                                                                 ActionChains.orig_drag_and_drop_by_offset,
                                                                                 source,
                                                                                 xoffset,
                                                                                 yoffset))
            return action_chains

        ActionChains.drag_and_drop_by_offset = action_chains_drag_and_drop_by_offset

    @staticmethod
    def override_drag_and_drop():
        ActionChains.orig_drag_and_drop = ActionChains.drag_and_drop

        def action_chains_drag_and_drop(action_chains, source, target):
            if is_already_in_action():
                ActionChains.orig_drag_and_drop(action_chains, source, target)
            else:
                action_chains.shield34_actions.append(ActionChainsDragDrop(DriverUtils.get_current_driver(),
                                                                           action_chains,
                                                                           ActionChains.orig_drag_and_drop,
                                                                           source,
                                                                           target))
            return action_chains

        ActionChains.drag_and_drop = action_chains_drag_and_drop

    @staticmethod
    def override_key_down():
        ActionChains.orig_key_down = ActionChains.key_down

        def action_chains_key_down(action_chains, value, on_element=None):
            if is_already_in_action():
                ActionChains.orig_key_down(action_chains, value, on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsKeyDown(DriverUtils.get_current_driver(), action_chains, ActionChains.orig_key_down, value,
                                        on_element))
            return action_chains

        ActionChains.key_down = action_chains_key_down

    @staticmethod
    def override_key_up():
        ActionChains.orig_key_up = ActionChains.key_up

        def action_chains_key_up(action_chains, value, on_element=None):
            if is_already_in_action():
                ActionChains.orig_key_up(action_chains, value, on_element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsKeyUp(DriverUtils.get_current_driver(), action_chains, ActionChains.orig_key_up, value,
                                      on_element))
            return action_chains

        ActionChains.key_up = action_chains_key_up

    @staticmethod
    def override_move_by_offset():
        ActionChains.orig_move_by_offset = ActionChains.move_by_offset

        def action_chains_move_by_offset(action_chains, xoffset, yoffset):
            if is_already_in_action():
                ActionChains.orig_move_by_offset(action_chains, xoffset, yoffset)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsMoveOffset(DriverUtils.get_current_driver(), action_chains,
                                           ActionChains.orig_move_by_offset, xoffset, yoffset))
            return action_chains

        ActionChains.move_by_offset = action_chains_move_by_offset

    @staticmethod
    def override_send_keys():
        ActionChains.orig_send_keys = ActionChains.send_keys

        def action_chains_send_keys(action_chains, *keys):
            if is_already_in_action():
                ActionChains.orig_send_keys(action_chains, *keys)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsSendKeys(DriverUtils.get_current_driver(), action_chains, ActionChains.orig_send_keys,
                                         *keys))
            return action_chains

        ActionChains.send_keys = action_chains_send_keys

    @staticmethod
    def override_send_keys_to_element():
        ActionChains.orig_send_keys_to_element = ActionChains.send_keys_to_element

        def action_chains_send_keys_to_element(action_chains, element, *keys_to_send):
            if is_already_in_action():
                ActionChains.orig_send_keys_to_element(action_chains, element, *keys_to_send)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsSendKeysElement(DriverUtils.get_current_driver(), action_chains,
                                                ActionChains.orig_send_keys_to_element, element, *keys_to_send))
            return action_chains

        ActionChains.send_keys_to_element = action_chains_send_keys_to_element

    @staticmethod
    def override_move_to_element():
        ActionChains.orig_move_to_element = ActionChains.move_to_element

        def action_chains_move_to_element(action_chains, element):
            if is_already_in_action():
                ActionChains.orig_move_to_element(action_chains, element)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsMoveToElement(DriverUtils.get_current_driver(), action_chains,
                                              ActionChains.orig_move_to_element, element))
            return action_chains

        ActionChains.move_to_element = action_chains_move_to_element

    @staticmethod
    def override_move_to_element_with_offset():
        ActionChains.orig_move_to_element_with_offset = ActionChains.move_to_element_with_offset

        def action_chains_move_to_element_with_offset(action_chains, element, x_offset, y_offset):
            if is_already_in_action():
                ActionChains.orig_move_to_element_with_offset(action_chains, element, x_offset, y_offset)
            else:
                action_chains.shield34_actions.append(
                    ActionChainsMoveToElementOffset(DriverUtils.get_current_driver(), action_chains,
                                                    ActionChains.orig_move_to_element_with_offset, element, x_offset,
                                                    y_offset))
            return action_chains

        ActionChains.move_to_element_with_offset = action_chains_move_to_element_with_offset


def is_already_in_action():
    return RunReportContainer.get_current_block_run_holder() is not None and \
           RunReportContainer.get_current_block_run_holder().action_already_started()


class WebDriverWaitOverrider(object):
    @staticmethod
    def override():
        WebDriverWait.org_until = WebDriverWait.until
        WebDriverWait.until = lambda web_driver_wait, method, message='': DriverWaitUntil(web_driver_wait, method,
                                                                                          message,
                                                                                          WebDriverWait.org_until).do_handle()
