import os
import re
import mysql.connector
import Mysql

ORIGINALSOURCE = 'LBT'
FILESOURCE = 'SRC'
HEADLINESOURCE = 'Type=Headline'
STORYSOURCE = 'Type=Story'
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

for root, dirs, files in os.walk("/home/hjdesai2/Desktop/TIS/NewsData_NER", topdown=True):
    for name in files:
        print name
        LBTLIST = []
        articlenumber = 0
        with open(os.path.abspath(os.path.join(root, name))) as fileobject:
            while 1:
                line = fileobject.readline()
                line = line.strip('\n')
                if FILESOURCE in line:
                    a = re.split('\|', line)
                    LBTLIST.insert(0, a[1])
                    break

            while 1:
                line = fileobject.readline()
                line = line.strip('\n')
                if ORIGINALSOURCE in line:
                    b = re.split(' |\|', line)
                    LBTLIST.insert(1, b[1])
                    LBTLIST.insert(2, b[3])
                    break

            if LBTLIST[0] != 'null':
                fileid = Mysql.insert_file(name,os.path.abspath(os.path.join(root)),LBTLIST[0], LBTLIST[1], LBTLIST[2], cursor)
            else:
                break
            flag = True

            line = fileobject.readline()
            line = line.strip('\n')

            PERSONLIST = {}
            ORGANIZATIONLIST = {}
            LOCATIONLIST = {}
            articleheadline = ''
            articlecontent = ''

            while flag:
                if HEADLINESOURCE in line:
                    articlenumber += 1
                    PERSONLIST.clear()
                    ORGANIZATIONLIST.clear()
                    LOCATIONLIST.clear()
                    articleheadline = ''
                    articlecontent = ''

                    line = fileobject.readline()

                    while 1:
                        line = fileobject.readline()
                        line = line.strip('\n')
                        b = re.split('\|', line)
                        if b[len(b)-1] is '':
                            break
                        else:
                            articleheadline += ' '+b[3]
                            if LOCATION in line or PERSON in line or ORGANIZATION in line:
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

                    while 1:
                        line = fileobject.readline()
                        line = line.strip('\n')
                        if HEADLINESOURCE in line:
                            articleid = Mysql.insert_article(fileid, articleheadline, articlenumber, articlecontent, cursor)
                            for person in PERSONLIST:
                                Mysql.insert_entity('PERSON',articleid,person,PERSONLIST[person],cursor)
                            for location in LOCATIONLIST:
                                Mysql.insert_entity('LOCATION',articleid,location,LOCATIONLIST[location],cursor)
                            for organization in ORGANIZATIONLIST:
                                Mysql.insert_entity('ORGANIZATION',articleid,organization,ORGANIZATIONLIST[organization],cursor)
                            break
                        elif STORYSOURCE in line:
                            flag = False
                            articleid = Mysql.insert_article(fileid, articleheadline, articlenumber, articlecontent, cursor)
                            for person in PERSONLIST:
                                Mysql.insert_entity('PERSON',articleid,person,PERSONLIST[person],cursor)
                            for location in LOCATIONLIST:
                                Mysql.insert_entity('LOCATION',articleid,location,LOCATIONLIST[location],cursor)
                            for organization in ORGANIZATIONLIST:
                                Mysql.insert_entity('ORGANIZATION',articleid,organization,ORGANIZATIONLIST[organization],cursor)
                            break
                        else:
                            b = re.split('\|', line)
                            articlecontent += ' '+b[3]
                            if LOCATION in line or PERSON in line or ORGANIZATION in line:
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
                elif STORYSOURCE in line:
                    flag = False

        fileobject.closed
cursor.close()
cnx.commit()
cnx.close()
