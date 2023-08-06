class RunStepRow():
    id = None
    create_time = None
    update_time = None
    external_action = None
    insert_index = None
    row_sub_type = None
    row_type = None
    row_value = None
    timestamp = None
    block_run_id = None

    @staticmethod
    def convert_db_to_map(db_table):
        i = 0
        vv = {}

        lst = []
        for r in db_table:
            row = RunStepRow()
            # vv['id'] =  d[0]
            row.id = r[0]
            row.create_time = r[1]
            row.update_time = r[2]
            row.external_action = r[3]
            row.insert_index = r[4]
            row.row_sub_type = r[5]
            row.row_type = r[6]
            row.row_value = r[7]
            row.timestamp = r[8]
            row.block_run_id = r[9]

            # vv['id'] = r[0]
            lst.append(row)
        return lst
        # lst[0][row_type]
        # new_db_table = {}
        # while i < len(db_table):
        #     new_db_table['id'] = db_table[i]