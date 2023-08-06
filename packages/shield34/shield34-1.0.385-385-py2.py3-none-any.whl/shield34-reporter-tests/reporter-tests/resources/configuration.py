import psycopg2
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "shield34",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")
    cursor = connection.cursor()

    # ostgreSQL_select_Query = "SELECT * FROM test_db.block where block_name='%s' and block_class_name='%s'"
    # cursor.execute(postgreSQL_select_Query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    # mobile_records = cursor.fetchall()


    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

