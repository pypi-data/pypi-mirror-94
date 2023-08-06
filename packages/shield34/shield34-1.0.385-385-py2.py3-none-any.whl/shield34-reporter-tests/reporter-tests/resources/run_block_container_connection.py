import json
import threading

import psycopg2

from resources.blockrunstep import RunStepRow
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.model.enums.row_type import RowType


class RunBlockConnection():
    mydata = threading.local()
    mydata.row = 0

    @staticmethod
    def get_block(block_name):
        RunBlockConnection.mydata.block = RunReportContainer.get_current_block_run_holder().blockRunContract.blockContract
        return RunBlockConnection.mydata.block
        
    @staticmethod
    def get_block_run():
        RunBlockConnection.mydata.block_run = RunReportContainer.get_current_block_run_holder().blockRunContract
        return RunBlockConnection.mydata.block_run

    @staticmethod
    def get_block_run_step():
        RunBlockConnection.mydata.block_run_step = []
        RunBlockConnection.mydata.row = 0
        print('get_block_run_step '+str(len(RunBlockConnection.mydata.block_run_step)))
        for row in RunReportContainer.get_current_block_run_holder().blockReport:
            RunBlockConnection.mydata.block_run_step.append(ConvertedRow(row))
        return RunBlockConnection.mydata.block_run_step




    @staticmethod
    def test_start():
        # while RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type == 'BROWSER_NETWORK':
        #     RunBlockConnection.mydata.row += 1
        RunBlockConnection.assert_rows('TEST_START_TIME', 'TEST_START_TIME')

    @staticmethod
    def test_end():
        RunBlockConnection.assert_rows('TEST_END_TIME', 'TEST_END_TIME')
        RunBlockConnection.mydata.row = 0

    @staticmethod
    def test_passed():
        RunBlockConnection.assert_rows('TEST_STATUS', 'TEST_PASSED')

    @staticmethod
    def driver_get():
        RunBlockConnection.assert_rows('ACTION', 'WEB_DRIVER_GET')

    @staticmethod
    def web_element_click():
        RunBlockConnection.assert_rows('ACTION', 'WEB_ELEMENT_CLICK')

    @staticmethod
    def driver_quit_report():
        RunBlockConnection.assert_rows('ACTION', 'WEB_DRIVER_QUIT')

    @staticmethod
    def perform_internal_action():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'PERFORM_ACTION')

    @staticmethod
    def element_position_at_viewport():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'ELEMENT_POSITION_AT_VIEW_PORT')

    @staticmethod
    def wait_for_visibility():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'WAIT_FOR_ELEMENT_VISIBILITY')

    @staticmethod
    def wait_for_clickability():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'WAIT_FOR_ELEMENT_CLICKABILITY')

    @staticmethod
    def wait_to_be_writeable():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'WAIT_FOR_ELEMENT_TO_BE_WRITABLE')

    @staticmethod
    def wait_for_element_presence():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'WAIT_FOR_ELEMENT_PRESENCE')

    @staticmethod
    def wait_for_element_number_to_be_more():
        RunBlockConnection.assert_rows('INTERNAL_ACTION', 'WAIT_FOR_ELEMENTS_NUMBER_TO_BE_MORE_THAN')

    @staticmethod
    def driver_close_report():
        RunBlockConnection.assert_rows('ACTION', 'WEB_DRIVER_CLOSE')

    @staticmethod
    def web_element_send_keys():
        RunBlockConnection.assert_rows('ACTION', 'WEB_ELEMENT_SEND_KEYS')

    @staticmethod
    def action_starterd():
        RunBlockConnection.assert_rows('TEST_ACTION', 'ACTION_STARTED')

    @staticmethod
    def action_ended():

        RunBlockConnection.assert_rows('TEST_ACTION', 'ACTION_ENDED')

    @staticmethod
    def action_key_down_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_KEY_DOWN')

    @staticmethod
    def action_key_up_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_KEY_UP')

    @staticmethod
    def actions_send_keys_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_SEND_KEYS')

    @staticmethod
    def actions_send_keys_element_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_SEND_KEYS_ELEMENT')

    @staticmethod
    def web_element_find_element():
        RunBlockConnection.assert_rows('ACTION', 'WEB_ELEMENT_FIND_ELEMENT')

    @staticmethod
    def web_element_find_elements():
        RunBlockConnection.assert_rows('ACTION', 'WEB_ELEMENT_FIND_ELEMENTS')

    @staticmethod
    def web_driver_find_elements():
        RunBlockConnection.assert_rows('ACTION', 'WEB_DRIVER_FIND_ELEMENTS')

    @staticmethod
    def html_row():
        RunBlockConnection.assert_rows('HTML', 'PAGE_HTML')
        RunBlockConnection.html_row_value()

    @staticmethod
    def html_element_row():
        RunBlockConnection.assert_rows('HTML', 'WEB_ELEMENT_HTML')
        RunBlockConnection.html_element_row_value()


    @staticmethod
    def web_driver_find_element():
        RunBlockConnection.assert_rows('ACTION', 'WEB_DRIVER_FIND_ELEMENT')

    @staticmethod
    def web_element_clear_element():
        RunBlockConnection.assert_rows('ACTION', 'WEB_ELEMENT_CLEAR')

    @staticmethod
    def action_click_element_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_CLICK_ELEMENT')

    @staticmethod
    def action_click_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_CLICK')

    @staticmethod
    def action_double_click_element_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_DOUBLE_CLICK_ELEMENT')

    @staticmethod
    def action_move_to_element_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_MOVE_TO_ELEMENT')

    @staticmethod
    def action_click_and_hold_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_CLICK_AND_HOLD_ELEMENT')

    @staticmethod
    def action_drag_and_drop_by_offset_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_DRAG_AND_DROP_ELEMENT_BY_OFFSET')

    @staticmethod
    def action_drag_and_drop_element_to_element_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_DRAG_AND_DROP_ELEMENT_TO_ELEMENT')

    @staticmethod
    def action_move_to_element_by_offset_report():
        RunBlockConnection.assert_rows('ACTION', 'ACTION_MOVE_BY_OFFSET')

    @staticmethod
    def get_row_type():
        return RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type

    @staticmethod
    def get_row_sub_type():
        return RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_sub_type

    @staticmethod
    def assert_rows(row_type, row_sub_type):
        try:
            print("Assert_rows " + row_type + " " + row_sub_type)
            while RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type == 'BROWSER_CONSOLE' or RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type == 'LOGS' or RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type == 'BROWSER_NETWORK':
                RunBlockConnection.mydata.row += 1

            assert len(RunBlockConnection.mydata.block_run_step) > 0, 'there is no block run steps'
            assert RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type == row_type, row_type + ' ' + \
                                                                                                     RunBlockConnection.mydata.block_run_step[
                                                                                                         RunBlockConnection.mydata.row].row_type
            assert RunBlockConnection.mydata.block_run_step[
                       RunBlockConnection.mydata.row].row_sub_type == row_sub_type, row_sub_type + ' ' + \
                                                                              RunBlockConnection.mydata.block_run_step[
                                                                                  RunBlockConnection.mydata.row].row_sub_type
            RunBlockConnection.mydata.row += 1
        # while  RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row].row_type ==  'BROWSER_NETWORK' :
        #     RunBlockConnection.mydata.row += 1
        except ValueError as ve:

            raise ve
        except TypeError as te:
            raise te





    # # # # # # # # # # # # # # # # # # # #  row value tests

    @staticmethod
    def web_element_find_element_row_value(locator):
        assert json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value)[
                   "locator"] == locator

    @staticmethod
    def html_row_value():
        assert len(RunBlockConnection.get_json_by_key('pageHtml')) >0


    @staticmethod
    def html_element_row_value():
        assert len(RunBlockConnection.get_json_by_key('elementHtml')) >0


    @staticmethod
    def test_start_row_value():
        assert len(json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value)["startTime"])>0



    @staticmethod
    def driver_quit_report_row_value(browser):
        assert RunBlockConnection.get_json_by_key('browser') == browser

    @staticmethod
    def driver_close_row_value(browser):
        RunBlockConnection.browser_row_value(browser)

    @staticmethod
    def browser_row_value(browser):
        assert RunBlockConnection.get_json_by_key('browser') == browser

    @staticmethod
    def locator_row_value(locator):
        assert RunBlockConnection.get_json_by_key('locator') == locator

    @staticmethod
    def driver_get_action_row_value_func(browser,url):
        assert  RunBlockConnection.get_value(json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value),'browser')== browser.lower()
        assert RunBlockConnection.get_value(json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value),'url')== url

    @staticmethod
    def web_driver_find_elements_row_value(browser, locator):
        assert RunBlockConnection.get_value(
            json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value), 'browser') == browser
        assert RunBlockConnection.get_value(
            json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value), 'locator') == locator


    @staticmethod
    def action_click_row_value(browser):
        RunBlockConnection.browser_row_value(browser)


    @staticmethod
    def actions_send_keys_element_row_value(locator,charSequenc):
        RunBlockConnection.locator_row_value(locator)
        assert RunBlockConnection.get_json_by_key('key') == charSequenc

    @staticmethod
    def action_click_element_row_value(locator):
        RunBlockConnection.locator_row_value(locator)


    @staticmethod
    def action_drag_and_drop_element_to_element_row_value(browser,source,target):
        RunBlockConnection.browser_row_value(browser)
        assert RunBlockConnection.get_json_by_key_parent('sourceWebElement','locator') == source
        assert RunBlockConnection.get_json_by_key_parent('targetWebElement','locator') == target

    @staticmethod
    def action_click_and_hold_row_value(source):
        RunBlockConnection.locator_row_value(source)

    @staticmethod
    def action_move_to_element_row_value(locator):
        RunBlockConnection.locator_row_value(locator)

    @staticmethod
    def action_double_click_element_row_value(locator):
        RunBlockConnection.locator_row_value(locator)


    @staticmethod
    def action_move_to_element_by_offset_row_value(offset_x, offset_y, browser):
        assert int(RunBlockConnection.get_json_by_key('xOffset')) == int(offset_x)
        assert int(RunBlockConnection.get_json_by_key('yOffset')) ==int( offset_y)
        assert RunBlockConnection.get_json_by_key('browser') == browser

    @staticmethod
    def action_drag_and_drop_by_offset_row_value(locator , offset_x, offset_y):
        assert int(RunBlockConnection.get_json_by_key('xOffset')) == int(offset_x)
        assert int(RunBlockConnection.get_json_by_key('yOffset')) == int(offset_y)
        RunBlockConnection.locator_row_value(locator)


    @staticmethod
    def driver_find_element_row_value(locator,browser):
        assert RunBlockConnection.get_json_by_key('browser') == browser
        assert RunBlockConnection.get_json_by_key('locator') == locator

    @staticmethod
    def find_element_row_value(locator,browser,child_locator):
        assert RunBlockConnection.get_json_by_key('browser') == browser
        assert RunBlockConnection.get_json_by_key_parent('webElement','locator') == locator
        assert RunBlockConnection.get_json_abstract('locator') == child_locator

    @staticmethod
    def web_element_find_elements_row_value(locator,browser,child_locator):
        assert RunBlockConnection.get_json_by_key('browser') == browser
        assert RunBlockConnection.get_json_by_key_parent('webElement','locator') == locator
        assert RunBlockConnection.get_json_abstract('locator') == child_locator


    @staticmethod
    def web_element_click_row_value(locator,browser):
        assert RunBlockConnection.get_json_by_key('browser') == browser
        assert RunBlockConnection.get_json_by_key('locator') == locator


    @staticmethod
    def web_element_clear_element_row_value(locator,browser):
        assert RunBlockConnection.get_json_by_key('browser') == browser
        assert RunBlockConnection.get_json_by_key('locator') == locator

    @staticmethod
    def action_key_down_row_value(browser,charSequence):
        RunBlockConnection.browser_row_value(browser)
        assert RunBlockConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def actions_send_keys_row_value(browser,charSequence):
        RunBlockConnection.browser_row_value(browser)
        assert RunBlockConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def action_key_up_row_value(browser,charSequence):
        RunBlockConnection.browser_row_value(browser)
        assert RunBlockConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def web_element_send_keys_row_value(locator,browser,charSequence):
            assert RunBlockConnection.get_json_by_key('locator') == locator
            assert RunBlockConnection.get_json_by_key('browser') == browser
            assert RunBlockConnection.get_json_by_key('charSequence') == charSequence


        # assert RunBlockConnection.get_value(
        #     json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value), 'browser') == browser
        # assert RunBlockConnection.get_value(
        #     json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value), 'locator') == locator

    @staticmethod
    def get_json_by_key(key):
        return RunBlockConnection.get_value(json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value), key)

    @staticmethod
    def get_json_by_key_parent(parent,key):
        return RunBlockConnection.get_value(
            json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value)[parent], key)

    @staticmethod
    def get_json_abstract(key):
        return json.loads(RunBlockConnection.mydata.block_run_step[RunBlockConnection.mydata.row - 1].row_value)[key]

    @staticmethod
    def get_value(json_object,key_value):
        # if key_value in json_object :
        #     return json_object[key_value]
        for key, value in json_object.items():
            if key_value in json_object:
                return json_object[key_value]
                # if a is not None:
                #     return  a
            # if (key == key_value):
            #     return value
            elif isinstance(value, dict):
                result= RunBlockConnection.get_value(value,key_value)
                if result is not None:
                    return result
            # if (result != None):
            #     return value
            # elif (key == key_value):
            #     return value


class ConvertedRow(object):
    def __init__(self, row):
        self.row_type = row.rowType.value
        self.row_sub_type = row.rowSubType.value

        if hasattr(row,'gen_row_value'):
            self.row_value = json.dumps(row.gen_row_value())