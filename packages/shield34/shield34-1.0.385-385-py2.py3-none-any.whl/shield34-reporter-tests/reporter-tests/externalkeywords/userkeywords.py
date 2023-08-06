from resources.run_block_container_connection import RunBlockConnection
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.listeners.shield34_listener import Shield34Listener
from shield34_reporter.overrider import selenium_overrider
from shield34_reporter.utils.driver_utils import DriverUtils


def init_report(test_name):



    RunBlockConnection.get_block(test_name)
    RunBlockConnection.get_block_run()
    RunBlockConnection.get_block_run_step()


def get_block_data(test_name):
        RunBlockConnection.get_block(test_name)

def get_block_run_data():
       RunBlockConnection.get_block_run()


def get_block_run_step_data():
    RunBlockConnection.get_block_run_step()


def run_sql_func():

    SdkAuthentication.login()
    Shield34Properties.binding_server_mode = 'none'
    selenium_overrider.SeleniumOverrider().override()
    Shield34Properties.screenshots_disabled = True
    Shield34Properties.screenshots_on_failure_disabled = True
    RunReportContainer.get_current_block_run_holder().reset_block_run_contract()
    Shield34Listener().on_test_start(None, None, None)


def test_success():
    Shield34Listener().on_test_success()


def print_csv_rows():
    for csv_row in RunReportContainer.get_current_block_run_holder().blockReport:
        print(csv_row.to_array())


def test_start():
    RunBlockConnection.test_start()
    RunBlockConnection.test_start_row_value()

def test_end_report():
    RunBlockConnection.test_end()


def action_start():
        RunBlockConnection.action_starterd()


def action_end():
    RunBlockConnection.action_ended()

def test_status_passsed():
    RunBlockConnection.test_passed()
    test_end_report

def find_element_report_func(locator,browser,child_locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_element_find_element()
    RunBlockConnection.find_element_row_value(locator, browser, child_locator)
    RunBlockConnection.wait_for_element_presence()
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.html_element_row()
    RunBlockConnection.html_row()
    # RunBlockConnection.web_element_find_element_row_value(locator)
    RunBlockConnection.action_ended()

def find_elements_report_func(locator,browser,child_locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_element_find_elements()
    RunBlockConnection.web_element_find_elements_row_value(locator, browser, child_locator)
    RunBlockConnection.wait_for_element_number_to_be_more()
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.html_row()
    RunBlockConnection.action_ended()

def driver_find_elements_report_func(browser,locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_driver_find_elements()
    RunBlockConnection.web_driver_find_elements_row_value(browser,locator)
    RunBlockConnection.wait_for_element_number_to_be_more()
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.html_row()
    RunBlockConnection.action_ended()

def driver_find_element_report_func(browser,locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_driver_find_element()
    RunBlockConnection.driver_find_element_row_value(locator,browser)
    RunBlockConnection.wait_for_element_presence()
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.html_element_row()
    RunBlockConnection.html_row()
    RunBlockConnection.action_ended()

def clear_element_report_func(locator,browser):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_element_clear_element()
    RunBlockConnection.web_element_clear_element_row_value(locator,browser)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()

def driver_get_action(browser,url):
    RunBlockConnection.action_starterd()
    RunBlockConnection.driver_get()
    RunBlockConnection.driver_get_action_row_value_func(browser,url)
    RunBlockConnection.mydata.row += 1
    RunBlockConnection.action_ended()

def web_element_click_report_func(browser,locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.web_element_click()
    RunBlockConnection.web_element_click_row_value(browser,locator)
    RunBlockConnection.wait_for_visibility()
    RunBlockConnection.element_position_at_viewport()
    RunBlockConnection.wait_for_clickability()
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()

def web_element_send_keys_report_func(locator,browser,charSequence):
        RunBlockConnection.action_starterd()
        RunBlockConnection.web_element_send_keys()
        RunBlockConnection.web_element_send_keys_row_value(locator,browser,charSequence)
        RunBlockConnection.wait_for_visibility()
        RunBlockConnection.wait_for_clickability()
        RunBlockConnection.wait_to_be_writeable()

        RunBlockConnection.perform_internal_action()
        RunBlockConnection.action_ended()



# def keys_down_up_report_func(browser,charSequence):
#     action_key_down_report_func(browser,charSequence)
#     action_key_up_report_func(browser,charSequence)
        # RunBlockConnection.action_starterd()
        # RunBlockConnection.action_key_down_report()
        # RunBlockConnection.action_ended()
        # RunBlockConnection.action_starterd()
        # RunBlockConnection.action_key_up_report()
        # RunBlockConnection.action_ended()


def driver_quit_report_func(browser):
            RunBlockConnection.action_starterd()
            RunBlockConnection.driver_quit_report()
            RunBlockConnection.driver_quit_report_row_value(browser)
            RunBlockConnection.perform_internal_action()
            RunBlockConnection.action_ended()


def driver_close_report_func(browser):
    RunBlockConnection.action_starterd()
    RunBlockConnection.driver_close_report()
    RunBlockConnection.driver_close_row_value(browser)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()


def action_click_element_report_func():
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_click_element_report()
    RunBlockConnection.action_ended()


def action_click_report_func(locator,offset_x,offset_y,browser):
    action_move_to_element_report_func(locator)
    action_move_to_element_by_offset_report_func(offset_x,offset_y,browser)
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_click_report()
    RunBlockConnection.action_click_row_value(browser)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()

def action_double_click_element_report_func(locator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_double_click_element_report()
    RunBlockConnection.action_double_click_element_row_value(locator)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()
    #action_move_to_element_report_func(locator)


def action_move_to_element_report_func(lcoator):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_move_to_element_report()
    RunBlockConnection.action_move_to_element_row_value(lcoator)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()

def action_move_to_element_by_offset_report_func(offset_x,offset_y,browser):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_move_to_element_by_offset_report()
    RunBlockConnection.action_move_to_element_by_offset_row_value( offset_x, offset_y, browser)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()

def action_key_down_report_func(browser,charSequence):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_key_down_report()
    RunBlockConnection.action_key_down_row_value(browser,charSequence)
    RunBlockConnection.action_ended()

def action_key_up_report_func(browser,charSequence):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_key_up_report()
    RunBlockConnection.action_key_up_row_value(browser,charSequence)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()


def press_keys_report_func(browser,charSequence):
        RunBlockConnection.action_starterd()
        RunBlockConnection.actions_send_keys_report()
        RunBlockConnection.actions_send_keys_row_value(browser,charSequence)
        RunBlockConnection.perform_internal_action()
        RunBlockConnection.action_ended()
        #action_key_up_report_func(browser,charSequence)


def actions_send_keys_element_report_func(browser,locator,charSequenc):
    RunBlockConnection.action_starterd()
    RunBlockConnection.actions_send_keys_element_report()
    RunBlockConnection.actions_send_keys_element_row_value(locator,charSequenc)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()


def action_click_and_hold_report_func(source):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_click_and_hold_report()
    RunBlockConnection.action_click_and_hold_row_value(source)
    action_move_to_element_report_func(source)
    # action_move_to_element_report_func(source)
    RunBlockConnection.action_ended()

def action_drag_and_drop_by_offset_report_func(browser,locator,xoffset,yoffset):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_drag_and_drop_by_offset_report()
    RunBlockConnection.action_drag_and_drop_by_offset_row_value(locator,xoffset,yoffset)
    RunBlockConnection.perform_internal_action()
    #action_click_and_hold_report_func(locator)
    #action_move_to_element_by_offset_report_func(xoffset,yoffset,browser)
    RunBlockConnection.action_ended()

def action_drag_and_drop_element_to_element_report_func(browser , source,target):
    RunBlockConnection.action_starterd()
    RunBlockConnection.action_drag_and_drop_element_to_element_report()
    RunBlockConnection.action_drag_and_drop_element_to_element_row_value(browser , source,target)
    RunBlockConnection.perform_internal_action()
    RunBlockConnection.action_ended()


def remote_close_report_func():
    DriverUtils.get_current_driver().close();

def driver_find_element_func(locator):
    return DriverUtils.get_current_driver().find_element_by_id(locator)

# def driver_find_element_func(by ,locator):
#     DriverUtils.get_current_driver().find_element(by,locator)

def get_child_func(parent_locator , locator):
    element = DriverUtils.get_current_driver().find_element_by_id(parent_locator)
    element.find_element_by_id(locator)

def get_childs_func(parent_locator , locator):
    # element = DriverUtils.get_current_driver().find_element(By.CLASS_NAME, "#pancakes")
    element = DriverUtils.get_current_driver().find_element_by_id(parent_locator)
    return  element.find_elements_by_class_name(locator)

def get_element_x(element):
    return element.location.get('x')

def action_send_keys_func(keys_to_send):
    actions = ActionChains(DriverUtils.get_current_driver())
    # actions.key_down(keys.Keys.SHIFT)
    actions.send_keys(keys_to_send)
    # actions.key_up(keys.Keys.SHIFT)
    actions.perform()

def action_send_keys_element_func(element,keys):
    actions = ActionChains(DriverUtils.get_current_driver())
    actions.send_keys_to_element(element,keys)
    actions.perform()



# row value func
def driver_get_action_row_value(browser,url):
    RunBlockConnection.driver_get_action_row_value_func(browser,url)





