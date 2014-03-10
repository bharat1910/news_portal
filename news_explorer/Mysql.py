__author__ = 'hjdesai2'
import mysql.connector

try:
    def insertFileDetails(filename, pathfile, date,cursor):
        name = filename
        path = pathfile
        publisheddate = date
        add_employee = ("INSERT INTO FILE"
                    "(filename, pathfile, publisheddate)"
                    "VALUES (%s, %s, %s)")
        details_file = (name, path, publisheddate)
        cursor.execute(add_employee, details_file)
        file_id = cursor.lastrowid
        return file_id

    def insert_entity(tablename, fileid, entityname, entitycount, cursor):
        add_entity = "INSERT INTO "+tablename+" (FILEID, "+tablename+"NAME, "+tablename+"COUNT) VALUES (%s, %s, %s)"
        data_entity = (fileid, entityname, entitycount)
        cursor.execute(add_entity, data_entity)
except:
    print(SystemError)





