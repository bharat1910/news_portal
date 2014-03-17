__author__ = 'hjdesai2'
import os
import re
import mysql.connector
import Mysql
from news_explorer.models import File, Person, Organization, Location

def insert_data_into_database():
    ORIGINALSOURCE = 'LBT'
    LOCATION = 'LOCATION'
    PERSON = 'PERSON'
    ORGANIZATION = 'ORGANIZATION'
    cnx = mysql.connector.connect(user='root', password='123',
                                  host='127.0.0.1',
                                  database='NewsExplorer')
    cursor = cnx.cursor()
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    count = 1
    for root, dirs, files in os.walk("NewsData_NER", topdown=True):
        for name in files:
            LBTLIST = []
            PERSONLIST = {}
            ORGANIZATIONLIST = {}
            LOCATIONLIST = {}
            with open(os.path.abspath(os.path.join(root, name))) as fileobject:
                for line in fileobject:
                    line = line.strip('\n')
                    if ORIGINALSOURCE in line:
                        a = re.split(' |\|', line)
                        LBTLIST.insert(0, a[1])
                        LBTLIST.insert(1, a[3])

                    if LOCATION in line or PERSON in line or ORGANIZATION in line:
                        b = re.split('\|', line)
                        for word in b[4:]:
                            c = word.split('=')
                            if c[0] == LOCATION:
                                if c[1] in LOCATIONLIST:
                                    LOCATIONLIST[c[1]] += 1
                                else:
                                    LOCATIONLIST[c[1]] = 1

                            if c[0] == PERSON:
                                if c[1] in PERSONLIST:
                                    PERSONLIST[c[1]] += 1
                                else:
                                    PERSONLIST[c[1]] = 1

                            if c[0] == ORGANIZATION:
                                if c[1] in ORGANIZATIONLIST:
                                    ORGANIZATIONLIST[c[1]] += 1
                                else:
                                    ORGANIZATIONLIST[c[1]] = 1
            #fileid = Mysql.insertFileDetails(name,os.path.abspath(os.path.join(root)),LBTLIST[0],cursor)
            f = File(id = count, name = LBTLIST[0], path = os.path.abspath(os.path.join(root)), published_date = "dummy")
            f.save();
            for person in PERSONLIST:
                #Mysql.insert_entity('PERSON',fileid,person,PERSONLIST[person],cursor)
                p = Person(file_id = count, name = person, count = PERSONLIST[person])
                p.save();
            for location in LOCATIONLIST:
                #Mysql.insert_entity('LOCATION',fileid,location,LOCATIONLIST[location],cursor)
                l = Location(file_id = count, name = location, count = LOCATIONLIST[location])
                l.save();
            for organization in ORGANIZATIONLIST:
                #Mysql.insert_entity('ORGANIZATION',fileid,organization,ORGANIZATIONLIST[organization],cursor)
                o = Organization(file_id = count, name = organization, count = ORGANIZATIONLIST[organization])
                o.save();
            count = count + 1
    fileobject.closed
    cursor.close()
    cnx.commit()
    cnx.close()



