from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.handler import SeleniumMethodHandler
from shield34_reporter.helpers import web_element_helper
from shield34_reporter.model.csv_rows.actions.action_click_and_hold_csv_row import ActionClickAndHoldCsvRow, \
    ActionClickAndHoldElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_click_csv_row import ActionClickCsvRow, ActionClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_context_click_csv_row import ActionContextClickCsvRow, \
    ActionContextClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_double_click_csv_row import ActionDoubleClickCsvRow, \
    ActionDoubleClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_drag_and_drop_element_by_offset import \
    ActionDragAndDropElementByOffset
from shield34_reporter.model.csv_rows.actions.action_drag_and_drop_element_to_element_csv_row import \
    ActionDragAndDropElementToElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_key_down_csv_row import ActionKeyDownCsvRow, \
    ActionKeyDownElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_key_up_csv_row import ActionKeyUpElementCsvRow, ActionKeyUpCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_by_offset_csv_row import ActionMoveByOffsetCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_to_element_csv_row import ActionMoveToElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_to_element_with_offset_csv_row import \
    ActionMoveToElementWithOffsetCsvRow
from shield34_reporter.model.csv_rows.actions.action_send_keys_csv_row import ActionSendKeysCsvRow, \
    ActionSendKeysWithElementCsvRow
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.enums.action_name import ActionName


class ActionChainsParent(SeleniumMethodHandler):
    def __init__(self, action_name, action_csv_row, driver, action_chains, on_element=None):
        self.driver = driver
        self.on_element = on_element
        self.action_chains = action_chains
        super(ActionChainsParent,self).__init__(action_name,action_csv_row)

    def handle_exception(self, exception):
        retval = False
        if self.on_element is not None:
            is_handled, element = self._handle_element_exception(exception, self.driver, self.on_element, self.timeout,
                                                                 self.polling)
            if is_handled:
                self.on_element = element
                retval = True

        if isinstance(exception, StaleElementReferenceException):
            # bug in Selenium need to refresh action_chains as well as element
            self.action_chains = ActionChains(self.driver)
            return True

        return retval


class ActionChainsClick(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsClick, self).__init__(ActionName.ACTION_CLICK,
                                                    ActionClickCsvRow(driver), driver, action_chains_obj, on_element)
        else:
            super(ActionChainsClick, self).__init__(ActionName.ACTION_CLICK_ELEMENT,
                                                    ActionClickElementCsvRow(driver, on_element),driver, action_chains_obj, on_element)
        self.click = click_method

    def do_orig_action(self):
        ActionChains(self.driver).click(self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsClickAndHold(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsClickAndHold, self).__init__(ActionName.ACTION_CLICK_AND_HOLD,
                                                           ActionClickAndHoldCsvRow(driver),
                                                           driver,
                                                           action_chains_obj,
                                                           on_element)
        else:
            super(ActionChainsClickAndHold, self).__init__(ActionName.ACTION_WEB_ELEMENT_CLICK_AND_HOLD,
                                                           ActionClickAndHoldElementCsvRow(driver, on_element),
                                                           driver,
                                                           action_chains_obj,
                                                           on_element)
        self.click_and_hold = click_method

    def do_orig_action(self):
        ActionChains(self.driver).click_and_hold(self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsContextClick(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsContextClick, self).__init__(ActionName.ACTION_CONTEXT_CLICK,
                                                           ActionContextClickCsvRow(driver),
                                                           driver,
                                                           action_chains_obj,
                                                           on_element)
        else:
            super(ActionChainsContextClick, self).__init__(ActionName.ACTION_WEB_ELEMENT_CONTEXT_CLICK,
                                                           ActionContextClickElementCsvRow(driver, on_element),
                                                           driver,
                                                           action_chains_obj,
                                                           on_element)
        self.context_click = click_method

    def do_orig_action(self):
        ActionChains(self.driver).context_click(self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDoubleClick(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsDoubleClick, self).__init__(
                ActionName.ACTION_DOUBLE_CLICK,
                ActionDoubleClickCsvRow(driver),
                driver,
                action_chains_obj,
                on_element)
        else:
            super(ActionChainsDoubleClick, self).__init__(
                ActionName.ACTION_WEB_ELEMENT_DOUBLE_CLICK,
                ActionDoubleClickElementCsvRow(driver, on_element),
                driver,
                action_chains_obj,
                on_element)
        self.double_click = click_method

    def do_orig_action(self):
        ActionChains(self.driver).double_click(self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDragDropOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, drag_method, source, xoffset, yoffset):
        super(ActionChainsDragDropOffset, self).__init__(
            ActionName.ACTION_DRAG_AND_DROP_ELEMENT_BY_OFFSET,
            ActionDragAndDropElementByOffset(driver, source, xoffset, yoffset))
        self.drag_and_drop_by_offset = drag_method
        self.driver = driver
        self.action_chains = action_chains_obj
        self.source = source
        self.xoffset = xoffset
        self.yoffset = yoffset

    def do_orig_action(self):
        ActionChains(self.driver).drag_and_drop_by_offset(self.source, self.xoffset, self.yoffset).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDragDrop(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, drag_method, source, target):
        super(ActionChainsDragDrop, self).__init__(ActionName.ACTION_DRAG_AND_DROP_ELEMENT_TO_ELEMENT,
                                                   ActionDragAndDropElementToElementCsvRow(driver, source, target))
        self.drag_and_drop = drag_method
        self.driver = driver
        self.action_chains = action_chains_obj
        self.source = source
        self.target = target

    def do_orig_action(self):
        ActionChains(self.driver).drag_and_drop( self.source, self.target).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsKeyDown(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, key_down_method, value, on_element=None):
        if on_element is None:
            super(ActionChainsKeyDown, self).__init__(ActionName.ACTION_KEY_DOWN,
                                                      ActionKeyDownCsvRow(driver, value),
                                                      driver,
                                                      action_chains_obj,
                                                      on_element)
        else:
            super(ActionChainsKeyDown, self).__init__(ActionName.ACTION_KEY_DOWN_ELEMENT,
                                                      ActionKeyDownElementCsvRow(driver, on_element, value),
                                                      driver,
                                                      action_chains_obj,
                                                      on_element)
        self.key_down = key_down_method
        self.value = value

    def do_orig_action(self):
        ActionChains(self.driver).key_down(self.value, self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsKeyUp(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, key_up_method, value, on_element=None):
        if on_element is None:
            super(ActionChainsKeyUp, self).__init__(ActionName.ACTION_KEY_UP,
                                                    ActionKeyUpCsvRow(driver, value),
                                                    driver,
                                                    action_chains_obj,
                                                    on_element)
        else:
            super(ActionChainsKeyUp, self).__init__(
                ActionName.ACTION_KEY_UP_ELEMENT,
                ActionKeyUpElementCsvRow(driver, on_element, value),
                driver,
                action_chains_obj,
                on_element)
        self.key_up = key_up_method
        self.value = value

    def do_orig_action(self):
        ActionChains(self.driver).key_up( self.value, self.on_element).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsMoveOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, move_by_offset_method, xoffset, yoffset):
        super(ActionChainsMoveOffset, self).__init__(
            ActionName.ACTION_MOVE_BY_OFFSET,
            ActionMoveByOffsetCsvRow(driver, xoffset, yoffset))

        self.move_by_offset = move_by_offset_method
        self.driver = driver
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        ActionChains(self.driver).move_by_offset(self.xoffset, self.yoffset).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsSendKeys(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, send_keys_method, *keys):
        super(ActionChainsSendKeys, self).__init__(ActionName.ACTION_SEND_KEYS, ActionSendKeysCsvRow(driver, *keys))

        self.send_keys = send_keys_method
        self.driver = driver
        self.keys = keys
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        ActionChains(self.driver).send_keys(*self.keys).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsSendKeysElement(ActionChainsParent):
    def __init__(self, driver, action_chains_obj, send_keys_method, element, *keys):
        super(ActionChainsSendKeysElement, self).__init__(ActionName.ACTION_SEND_KEYS_ELEMENT,
                                                          ActionSendKeysWithElementCsvRow(driver, element, *keys),
                                                          driver,
                                                          action_chains_obj,
                                                          element)
        self.send_keys_to_element = send_keys_method
        self.keys = keys

    def do_orig_action(self):
        ActionChains(self.driver).send_keys_to_element(self.on_element, *self.keys).orig_perform()
        self._set_return_value(self.action_chains)
        return True


class ActionChainsMoveToElement(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, orig_method, element):
        super(ActionChainsMoveToElement, self).__init__(ActionName.ACTION_MOVE_TO_ELEMENT,
                                                        ActionMoveToElementCsvRow(driver, element))
        self.move_to_element = orig_method
        self.driver = driver
        self.element = element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        ActionChains(self.driver).move_to_element(self.element).orig_perform()
        self._set_return_value(self.action_chains)
        return True

    def handle_exception(self, exception):
        try:
            if isinstance(exception, StaleElementReferenceException):
                self.element = web_element_helper.reallocate_web_element(self.driver, self.element)
                if self.element is not None:
                    self.action_chains = ActionChains(self.driver)
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("move to element handle exception failed.", e))
        return False


class ActionChainsMoveToElementOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, orig_method, element, xoffset, yoffset):
        super(ActionChainsMoveToElementOffset, self).__init__(
            ActionName.ACTION_MOVE_TO_ELEMENT_WITH_OFFSET,
            ActionMoveToElementWithOffsetCsvRow(driver, element, xoffset, yoffset))
        self.move_to_element_with_offset = orig_method
        self.driver = driver
        self.element = element
        self.x_offset = xoffset
        self.y_offset = yoffset
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        ActionChains(self.driver).move_to_element_with_offset(self.element, self.x_offset, self.y_offset).orig_perform()
        self._set_return_value(self.action_chains)
        return True

    def handle_exception(self, exception):
        try:
            if isinstance(exception, StaleElementReferenceException):
                self.element = web_element_helper.reallocate_web_element(self.driver, self.element)

                if self.element is not None:
                    self.action_chains = ActionChains(self.driver)
                    return True
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("move to element with offset handle exception failed.", e))
        return False


