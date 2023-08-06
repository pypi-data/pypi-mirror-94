import time

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.reporter_proxy import ReporterProxy
from .listener_utils import ListenerUtils
from shield34_reporter.model.csv_rows.test.end_time_csv_row import EndTimeCsvRow
from shield34_reporter.model.csv_rows.general_csv_row import GeneralCsvRow
from shield34_reporter.model.csv_rows.test.start_time_csv_row import StartTimeCsvRow
from shield34_reporter.model.csv_rows.test.test_failure_csv_row import TestFailureCsvRow
from shield34_reporter.model.csv_rows.test.test_passed_csv_row import TestPassedCsvRow
from shield34_reporter.model.csv_rows.test.test_skipped_csv_row import TestSkippedCsvRow
from shield34_reporter.model.enums.block_type import BlockType
from shield34_reporter.model.enums.placement import Placement
from shield34_reporter.model.enums.status import Status
from shield34_reporter.utils.screen_shots import ScreenShot
from shield34_reporter.utils.time_utils import TimeUtils
import logging

from ..consts.shield34_properties import Shield34Properties
from ..utils import reporter_proxy


class Shield34Listener:
    logger = logging
    suiteName = "Main suite"
    parentSuiteName = "Main suite"
    current_driver = None

    def on_test_start(self, test_name, test_class_name, block_params=''):
        SdkAuthentication.login()
        RunReportContainer.get_current_block_run_holder().reset_executor()
        block_start_timestamp_as_long = time.time()
        RunReportContainer.get_current_block_run_holder().reset_block_run_contract()
        RunReportContainer.get_current_block_run_holder().blockRunContract.runContract = RunReportContainer.get_current_run_contract()
        block_contract = RunReportContainer.get_current_block_run_holder().blockRunContract.blockContract
        block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
        block_run_contract.status = Status.RUNNING
        block_run_contract.startTimestamp = TimeUtils.get_current_timestamp()
        block_contract.blockName = test_name
        block_contract.blockClassName = test_class_name
        block_contract.blockType = BlockType.TEST
        block_contract.blockParams = block_params
        block_contract.suiteName = self.suiteName
        block_contract.externalParams = ""
        RunReportContainer.get_current_block_run_holder().blockRunContract = ListenerUtils.save_or_update_block_run(block_run_contract)
        block_contract = RunReportContainer.get_current_block_run_holder().blockRunContract.blockContract
        RunReportContainer.add_report_csv_row(GeneralCsvRow(RunReportContainer.runContract.id, block_contract.id, self.parentSuiteName, block_run_contract.startTimestamp, block_start_timestamp_as_long, self.suiteName, test_class_name , test_name, ""))
        RunReportContainer.add_report_csv_row(StartTimeCsvRow(block_start_timestamp_as_long))
        ReporterProxy.start_proxy_management_server()
        if len(RunReportContainer.get_current_block_run_holder().proxyServers) > 0:
            if RunReportContainer.get_current_block_run_holder().proxyServers[0] is not None:
                reporter_proxy.create_new_har(RunReportContainer.get_current_block_run_holder().proxyServers[0])



    def on_test_finish(self):
        block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
        if block_run_contract.id == '':
            return
        if block_run_contract.status == Status.RUNNING:
            self.on_test_success()
        block_run_contract.endTimestamp = TimeUtils.get_current_timestamp()
        ListenerUtils.fetch_browser_logs()
        ListenerUtils.fetch_browser_network2()
        block_end_timestamp_as_long = time.time()
        RunReportContainer.add_report_csv_row(EndTimeCsvRow(block_end_timestamp_as_long))
        RunReportContainer.get_current_block_run_holder().shut_down_executor()
        current_test_folder = RunReportContainer.get_current_block_run_holder().get_current_test_folder()

        RunReportContainer.get_current_block_run_holder().blockRunContract = ListenerUtils.save_or_update_block_run(
            block_run_contract)
        ListenerUtils.save_report(current_test_folder, current_test_folder, block_run_contract)
        RunReportContainer.get_current_block_run_holder().reset_block_run_contract()

    def on_test_success(self):
        SdkAuthentication.login()
        block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
        if block_run_contract.id == '':
            return
        RunReportContainer.add_report_csv_row(TestPassedCsvRow())
        block_run_contract.status = Status.PASSED

    def on_test_failure(self, error):
        SdkAuthentication.login()
        block_name = RunReportContainer.get_current_block_run_holder().blockRunContract.blockContract.blockName
        ##TODO add failure screen shot
        ScreenShot.capture_screen_shoot(block_name, Placement.AFTER_FAILURE.value, True)
        block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
        if block_run_contract.id == '':
            return
        RunReportContainer.add_report_csv_row(TestFailureCsvRow(error))
        block_run_contract.status = Status.FAILED

    def on_test_skipped(self):
        SdkAuthentication.login()
        block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
        if block_run_contract.id == '':
            return
        RunReportContainer.add_report_csv_row(TestSkippedCsvRow())
        block_run_contract.status = Status.SKIPPED

    def on_suite_start(self, suite_name):
        SdkAuthentication.login()
        self.suiteName = suite_name
        RunReportContainer.create_current_run_contract(suite_name)

    def get_current_driver(self):

        self.current_driver = DriverUtils.get_current_driver()


    def set_current_driver(self, driver):
        RunReportContainer.get_current_block_run_holder().currentDriver = driver