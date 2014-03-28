__author__ = 'hjdesai2'
import mysql.connector

try:
    def insert_file(filename, pathfile, filesource, publisheddate, publishedlocation, cursor):
        add_entity = "INSERT INTO FILE (FILENAME, PATHFILE, FILESOURCE, PUBLISHEDDATE, PUBLISHEDLOCATION) VALUES (%s, %s, %s, %s, %s)"
        data_entity = (filename, pathfile, filesource, publisheddate, publishedlocation)
        cursor.execute(add_entity, data_entity)
        return cursor.lastrowid


    def insert_article(fileid, articleheadline, articlenumber, articlecontent, cursor):
        add_entity = "INSERT INTO ARTICLE (FILEID, ARTICLEHEADLINE, ARTICLENUMBER, ARTICLECONTENT) VALUES (%s, %s, %s, %s)"
        data_entity = (fileid, articleheadline, articlenumber, articlecontent)
        cursor.execute(add_entity, data_entity)
        return cursor.lastrowid


    def insert_entity(tablename, articleid, entityname, entitycount, cursor):
        add_entity = "INSERT INTO " + tablename + " (ARTICLEID, " + tablename + "NAME, " + tablename + "COUNT) VALUES (%s, %s, %s)"
        data_entity = (articleid, entityname, entitycount)
        cursor.execute(add_entity, data_entity)

    def select_data(file,NewsJsonCursor):
        select_entity = "Select * from  news_explorer_"+ file +""
        #select_entity = "Select * from "+file+""
        NewsJsonCursor.execute(select_entity)
        rows = NewsJsonCursor.fetchall()
        return rows



except:
    print(SystemError)





