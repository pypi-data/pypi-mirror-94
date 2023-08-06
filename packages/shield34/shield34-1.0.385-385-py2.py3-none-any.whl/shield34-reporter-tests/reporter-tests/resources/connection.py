import json
import threading

import psycopg2

from resources.blockrunstep import RunStepRow


class DBConnection():

    @staticmethod
    def get_db_connection():
        # Get Database connection
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="shield34",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Failed to connect to database {}".format(error))

    @staticmethod
    def close_db_connection(connection):
        # Close Database connection
        try:
            connection.close()
        except (Exception, psycopg2.Error) as error:
            print("Failed to close database connection {}".format(error))

    def read_db_version(self):
        try:
            connection = DBConnection.get_db_connection()
            # db_Info = connection.get_server_info()
            # print("Connected to MySQL database... MySQL Server version is ", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("Your connected to - ", record)
            DBConnection.close_db_connection(connection)
        except(Exception, psycopg2.Error) as error:
            print("Failed to read database version {}".format(error))

    mydata = threading.local()
    mydata.row = 0

    @staticmethod
    def run_exec():
        try:
            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()

            if DBConnection.is_exist("SELECT id FROM  test_db.project  WHERE id = 1"):
                postgres_insert_query = """INSERT INTO test_db.project  (id, create_time, update_time, bluesnap_shopper_id, description, name)   VALUES(%s,%s,%s,%s,%s,%s);"""
                record_to_insert = (1, 1566400363354, 1566400363354, '', 'test_project_description', 'test_project')
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()

            if DBConnection.is_exist(
                    "SELECT api_key FROM  test_db.project_credentials WHERE api_key = 'cbf2d2e3-f5e4-4206-9425-12f5ec7bef05'"):
                postgres_insert_query = """INSERT INTO test_db.project_credentials  (api_key, create_time, update_time, active,api_secret, project_id)   VALUES(%s,%s,%s,%s,%s,%s);"""
                record_to_insert = ('cbf2d2e3-f5e4-4206-9425-12f5ec7bef05', 1544367027048, 1544367027048, 'true',
                                    '$2a$10$N182FwZnUfeldTiqku1dEe/aQ5F69WLt5A0f9tbmXH5pspzlxwY.q', 1)
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()

            if DBConnection.is_exist("SELECT id FROM test_db.users WHERE id = 1"):
                postgres_insert_query = """INSERT INTO test_db.users  (id, create_time, update_time, email, fullname, password,username)   VALUES(%s,%s,%s,%s,%s,%s,%s);"""
                record_to_insert = (1, 1566400363354, 1566400363354, 'test@test.com', 'full_name',
                                    '$2a$10$WOnPgJI5mHrtu5XH1gyu1Oq4L873IQLjevY2QCpSbecknKIfK8Kcq', 'test@test.com')
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()

            if DBConnection.is_exist(
                    "SELECT id FROM test_db.license WHERE id = '6fad5348-dc45-4372-a366-802d15c6daa7'"):
                postgres_insert_query = """INSERT INTO test_db.license  (id, create_time, update_time, active, annual_price, blue_snap_annual_contract_id, blue_snap_monthly_contract_id, blue_snap_product_id, description, type, machines_count, monthly_price, name)   VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                record_to_insert = (
                '6fad5348-dc45-4372-a366-802d15c6daa7', 1566476035677, 1566476035677, 'true', 50, 'null', 'null',
                'null', 'Freemium Description', 'FREEMIUM', 1, 60, 'Freemium')
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()

            if DBConnection.is_exist(
                    "SELECT id FROM test_db.project_license  WHERE id = '850b9bc6-97bb-4f0f-95ab-3bbb2d37226c'"):
                postgres_insert_query = """INSERT INTO test_db.project_license  (id	,create_time,	update_time,	active,	annual_price,	auto_renew,	bs_subscription_id,	description	,expiration_timestamp,	type,	machines_count	,monthly_price,	name	,paid	,payment_period,	purchase_timestamp,	license_id,	project_id)   VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                record_to_insert = (
                '850b9bc6-97bb-4f0f-95ab-3bbb2d37226c', 1566400363354, 1566400363354, 'true', 50, 'true', '',
                'Freemium Description', 1566400363354, 'FREEMIUM', 1, 60, 'Freemium', 'true', 'MONTHLY_PAYMENT',
                1566400363354, '6fad5348-dc45-4372-a366-802d15c6daa7', 1)
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()

            if DBConnection.is_exist("SELECT project_id FROM  test_db.project_user WHERE project_id = 1"):
                postgres_insert_query = """INSERT INTO test_db.project_user  (create_time, update_time, user_role, project_id, user_id)   VALUES(%s,%s,%s,%s,%s);"""
                record_to_insert = (1566459849149, 1566459849149, 'SUPER_USER', 1, 1)
                cursor.execute(postgres_insert_query, record_to_insert)
                connection.commit()
            # count = cursor.rowcount
            # print(count, "Record inserted successfully into  table")
        except (Exception, psycopg2.Error) as error:
            if (connection):
                print("Failed to insert record into  table", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    # @staticmethod
    # def execute_command(statement , values):

    @staticmethod
    def is_exist(statement):
        try:
            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()
            postgreSQL_select_Query = statement
            cursor.execute(postgreSQL_select_Query)
            # mobile_records = cursor.fetchall()
            return cursor.fetchone() is None
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    @staticmethod
    def select(statement):
        try:
            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()
            postgreSQL_select_Query = "select * from " + statement
            cursor.execute(postgreSQL_select_Query)
            # print("Selecting rows from  table using cursor.fetchall")
            # mobile_records = cursor.fetchall()

            # print("Print each row and it's columns values")
            return cursor.rowcount
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    @staticmethod
    def get_block(block_name):
        DBConnection.mydata.row=0
        # Read data from  table
        try:
            # Call getDbConnection method to get connection.

            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()
            sql_select_query = """SELECT * FROM test_db.block where block_name=%s"""

            cursor.execute(sql_select_query, (block_name,))
            DBConnection.mydata.block = cursor.fetchall()
            while len(DBConnection.mydata.block) == 0:
                cursor.execute(sql_select_query, (block_name,))
                DBConnection.mydata.block = cursor.fetchall()
            # print(DBConnection.mydata.block)
            # for row in mydata.block:
            #     print("Doctor Id: = ", row[0])
            #     print("Doctor Name: = ", row[1])        # Close db connection
            DBConnection.close_db_connection(connection)
            return DBConnection.mydata.block

        except psycopg2.Error as error:
            print("Failed to read table {}".format(error))

    @staticmethod
    def get_block_run():
        # Read data from  table
        try:
            # Call getDbConnection method to get connection.

            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()
            sql_select_query = """SELECT * FROM test_db.block_run where block_id=%s"""
            cursor.execute(sql_select_query, (DBConnection.mydata.block[0][0],))
            DBConnection.mydata.block_run = cursor.fetchall()
            while len(DBConnection.mydata.block_run) == 0:
                cursor.execute(sql_select_query, (DBConnection.mydata.block[0][0],))
                DBConnection.mydata.block_run = cursor.fetchall()
            # print(DBConnection.mydata.block_run)
            # Close db connection
            DBConnection.close_db_connection(connection)
            return DBConnection.mydata.block_run

        except (Exception, psycopg2.Error) as error:
            print("Failed to read table {}".format(error))

    @staticmethod
    def get_block_run_step():
        # Read data from  table
        try:
            # Call getDbConnection method to get connection.

            connection = DBConnection.get_db_connection()
            cursor = connection.cursor()
            sql_select_query = """SELECT * FROM test_db.block_run_step where block_run_id=%s AND row_type NOT LIKE 'LOGS' AND row_type NOT LIKE 'BROWSER_NETWORK'  order by timestamp asc, insert_index asc"""
            # sql_select_query = """SELECT * FROM test_db.block_run_step where block_run_id=%s AND row_type NOT LIKE 'LOGS'  order by timestamp asc, insert_index asc"""
            cursor.execute(sql_select_query, (DBConnection.mydata.block_run[0][0],))
            DBConnection.mydata.block_run_step = cursor.fetchall()
            # print(DBConnection.mydata.block_run_step[0])
            while len(DBConnection.mydata.block_run_step) == 0:
                cursor.execute(sql_select_query, (DBConnection.mydata.block_run[0][0],))
                DBConnection.mydata.block_run_step = cursor.fetchall()
            DBConnection.mydata.block_run_step = RunStepRow.convert_db_to_map(DBConnection.mydata.block_run_step)
            # Close db connection
            DBConnection.close_db_connection(connection)
            return DBConnection.mydata.block_run_step
        except (Exception, psycopg2.Error) as error:
            print("Failed to read table {}".format(error))

    @staticmethod
    def test_start():
        # while DBConnection.mydata.block_run_step[DBConnection.mydata.row].row_type == 'BROWSER_NETWORK':
        #     DBConnection.mydata.row += 1
        DBConnection.assert_rows('TEST_START_TIME', 'TEST_START_TIME')

    @staticmethod
    def test_end():
        DBConnection.assert_rows('TEST_END_TIME', 'TEST_END_TIME')
        DBConnection.mydata.row = 0

    @staticmethod
    def test_passed():
        DBConnection.assert_rows('TEST_STATUS', 'TEST_PASSED')

    @staticmethod
    def driver_get():
        DBConnection.assert_rows('ACTION', 'WEB_DRIVER_GET')

    @staticmethod
    def web_element_click():
        DBConnection.assert_rows('ACTION', 'WEB_ELEMENT_CLICK')

    @staticmethod
    def driver_quit_report():
        DBConnection.assert_rows('ACTION', 'WEB_DRIVER_QUIT')

    @staticmethod
    def driver_close_report():
        DBConnection.assert_rows('ACTION', 'WEB_DRIVER_CLOSE')

    @staticmethod
    def web_element_send_keys():
        DBConnection.assert_rows('ACTION', 'WEB_ELEMENT_SEND_KEYS')

    @staticmethod
    def action_starterd():
        DBConnection.assert_rows('TEST_ACTION', 'ACTION_STARTED')

    @staticmethod
    def action_ended():
        DBConnection.assert_rows('TEST_ACTION', 'ACTION_ENDED')

    @staticmethod
    def action_key_down_report():
        DBConnection.assert_rows('ACTION', 'ACTION_KEY_DOWN')

    @staticmethod
    def action_key_up_report():
        DBConnection.assert_rows('ACTION', 'ACTION_KEY_UP')

    @staticmethod
    def actions_send_keys_report():
        DBConnection.assert_rows('ACTION', 'ACTION_SEND_KEYS')

    @staticmethod
    def actions_send_keys_element_report():
        DBConnection.assert_rows('ACTION', 'ACTION_SEND_KEYS_ELEMENT')

    @staticmethod
    def web_element_find_element():
        DBConnection.assert_rows('ACTION', 'WEB_ELEMENT_FIND_ELEMENT')

    @staticmethod
    def web_element_find_elements():
        DBConnection.assert_rows('ACTION', 'WEB_ELEMENT_FIND_ELEMENTS')

    @staticmethod
    def web_driver_find_elements():
        DBConnection.assert_rows('ACTION', 'WEB_DRIVER_FIND_ELEMENTS')

    @staticmethod
    def html_row():
        DBConnection.assert_rows('HTML', 'PAGE_HTML')
        DBConnection.html_row_value()

    @staticmethod
    def html_element_row():
        DBConnection.assert_rows('HTML', 'WEB_ELEMENT_HTML')
        DBConnection.html_element_row_value()


    @staticmethod
    def web_driver_find_element():
        DBConnection.assert_rows('ACTION', 'WEB_DRIVER_FIND_ELEMENT')

    @staticmethod
    def web_element_clear_element():
        DBConnection.assert_rows('ACTION', 'WEB_ELEMENT_CLEAR')

    @staticmethod
    def action_click_element_report():
        DBConnection.assert_rows('ACTION', 'ACTION_CLICK_ELEMENT')

    @staticmethod
    def action_click_report():
        DBConnection.assert_rows('ACTION', 'ACTION_CLICK')

    @staticmethod
    def action_double_click_element_report():
        DBConnection.assert_rows('ACTION', 'ACTION_DOUBLE_CLICK_ELEMENT')

    @staticmethod
    def action_move_to_element_report():
        DBConnection.assert_rows('ACTION', 'ACTION_MOVE_TO_ELEMENT')

    @staticmethod
    def action_click_and_hold_report():
        DBConnection.assert_rows('ACTION', 'ACTION_CLICK_AND_HOLD_ELEMENT')

    @staticmethod
    def action_drag_and_drop_by_offset_report():
        DBConnection.assert_rows('ACTION', 'ACTION_DRAG_AND_DROP_ELEMENT_BY_OFFSET')

    @staticmethod
    def action_drag_and_drop_element_to_element_report():
        DBConnection.assert_rows('ACTION', 'ACTION_DRAG_AND_DROP_ELEMENT_TO_ELEMENT')

    @staticmethod
    def action_move_to_element_by_offset_report():
        DBConnection.assert_rows('ACTION', 'ACTION_MOVE_BY_OFFSET')

    @staticmethod
    def get_row_type():
        return DBConnection.mydata.block_run_step[DBConnection.mydata.row].row_type

    @staticmethod
    def get_row_sub_type():
        return DBConnection.mydata.block_run_step[DBConnection.mydata.row].row_sub_type

    @staticmethod
    def assert_rows(row_type, row_sub_type):
        assert len(DBConnection.mydata.block_run_step) > 0, 'there is no block run steps'
        assert DBConnection.mydata.block_run_step[DBConnection.mydata.row].row_type == row_type, row_type + ' ' + \
                                                                                                 DBConnection.mydata.block_run_step[
                                                                                                     DBConnection.mydata.row].row_type
        assert DBConnection.mydata.block_run_step[
                   DBConnection.mydata.row].row_sub_type == row_sub_type, row_sub_type + ' ' + \
                                                                          DBConnection.mydata.block_run_step[
                                                                              DBConnection.mydata.row].row_sub_type
        DBConnection.mydata.row += 1
        # while  DBConnection.mydata.block_run_step[DBConnection.mydata.row].row_type ==  'BROWSER_NETWORK' :
        #     DBConnection.mydata.row += 1






    # # # # # # # # # # # # # # # # # # # #  row value tests

    @staticmethod
    def web_element_find_element_row_value(locator):
        assert json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value)[
                   "locator"] == locator

    @staticmethod
    def html_row_value():
        assert len(DBConnection.get_json_by_key('pageHtml')) >0


    @staticmethod
    def html_element_row_value():
        assert len(DBConnection.get_json_by_key('elementHtml')) >0


    @staticmethod
    def test_start_row_value():
        assert len(json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value)["startTime"])>0



    @staticmethod
    def driver_quit_report_row_value(browser):
        assert DBConnection.get_json_by_key('browser') == browser

    @staticmethod
    def driver_close_row_value(browser):
        DBConnection.browser_row_value(browser)

    @staticmethod
    def browser_row_value(browser):
        assert DBConnection.get_json_by_key('browser') == browser

    @staticmethod
    def locator_row_value(locator):
        assert DBConnection.get_json_by_key('locator') == locator

    @staticmethod
    def driver_get_action_row_value_func(browser,url):
        assert  DBConnection.get_value(json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value),'browser')== browser
        assert DBConnection.get_value(json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value),'url')== url

    @staticmethod
    def web_driver_find_elements_row_value(browser, locator):
        assert DBConnection.get_value(
            json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value), 'browser') == browser
        assert DBConnection.get_value(
            json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value), 'locator') == locator


    @staticmethod
    def action_click_row_value(browser):
        DBConnection.browser_row_value(browser)


    @staticmethod
    def actions_send_keys_element_row_value(locator,charSequenc):
        DBConnection.locator_row_value(locator)
        assert DBConnection.get_json_by_key('key') == charSequenc

    @staticmethod
    def action_click_element_row_value(locator):
        DBConnection.locator_row_value(locator)


    @staticmethod
    def action_drag_and_drop_element_to_element_row_value(browser,source,target):
        DBConnection.browser_row_value(browser)
        assert DBConnection.get_json_by_key_parent('sourceWebElement','locator') == source
        assert DBConnection.get_json_by_key_parent('targetWebElement','locator') == target

    @staticmethod
    def action_click_and_hold_row_value(source):
        DBConnection.locator_row_value(source)

    @staticmethod
    def action_move_to_element_row_value(locator):
        DBConnection.locator_row_value(locator)

    @staticmethod
    def action_double_click_element_row_value(locator):
        DBConnection.locator_row_value(locator)


    @staticmethod
    def action_move_to_element_by_offset_row_value(offset_x, offset_y, browser):
        assert DBConnection.get_json_by_key('xOffset') ==  int(offset_x)
        assert DBConnection.get_json_by_key('yOffset') ==int( offset_y)
        assert DBConnection.get_json_by_key('browser') == browser

    @staticmethod
    def action_drag_and_drop_by_offset_row_value(locator , offset_x, offset_y):
        assert DBConnection.get_json_by_key('xOffset') == int(offset_x)
        assert DBConnection.get_json_by_key('yOffset') == int(offset_y)
        DBConnection.locator_row_value(locator)


    @staticmethod
    def driver_find_element_row_value(locator,browser):
        assert DBConnection.get_json_by_key('browser') == browser
        assert DBConnection.get_json_by_key('locator') == locator

    @staticmethod
    def find_element_row_value(locator,browser,child_locator):
        assert DBConnection.get_json_by_key('browser') == browser
        assert DBConnection.get_json_by_key_parent('webElement','locator') == locator
        assert DBConnection.get_json_abstract('locator') == child_locator

    @staticmethod
    def web_element_find_elements_row_value(locator,browser,child_locator):
        assert DBConnection.get_json_by_key('browser') == browser
        assert DBConnection.get_json_by_key_parent('webElement','locator') == locator
        assert DBConnection.get_json_abstract('locator') == child_locator


    @staticmethod
    def web_element_click_row_value(locator,browser):
        assert DBConnection.get_json_by_key('browser') == browser
        assert DBConnection.get_json_by_key('locator') == locator


    @staticmethod
    def web_element_clear_element_row_value(locator,browser):
        assert DBConnection.get_json_by_key('browser') == browser
        assert DBConnection.get_json_by_key('locator') == locator

    @staticmethod
    def action_key_down_row_value(browser,charSequence):
        DBConnection.browser_row_value(browser)
        assert DBConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def actions_send_keys_row_value(browser,charSequence):
        DBConnection.browser_row_value(browser)
        assert DBConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def action_key_up_row_value(browser,charSequence):
        DBConnection.browser_row_value(browser)
        assert DBConnection.get_json_by_key('key') == charSequence

    @staticmethod
    def web_element_send_keys_row_value(locator,browser,charSequence):
            assert DBConnection.get_json_by_key('locator') == locator
            assert DBConnection.get_json_by_key('browser') == browser
            assert DBConnection.get_json_by_key('charSequence') == charSequence


        # assert DBConnection.get_value(
        #     json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value), 'browser') == browser
        # assert DBConnection.get_value(
        #     json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value), 'locator') == locator

    @staticmethod
    def get_json_by_key(key):
        return DBConnection.get_value(json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value), key)

    @staticmethod
    def get_json_by_key_parent(parent,key):
        return DBConnection.get_value(
            json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value)[parent], key)

    @staticmethod
    def get_json_abstract(key):
        return json.loads(DBConnection.mydata.block_run_step[DBConnection.mydata.row - 1].row_value)[key]

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
                result= DBConnection.get_value(value,key_value)
                if result is not None:
                    return result
            # if (result != None):
            #     return value
            # elif (key == key_value):
            #     return value
