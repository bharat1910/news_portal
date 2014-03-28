__author__ = 'hjdesai2'
import os
import re
import mysql.connector

cnx = mysql.connector.connect(user='root', password='123',
                              host='127.0.0.1',
                              database='NewsExplorer')