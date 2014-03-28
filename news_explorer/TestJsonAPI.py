__author__ = 'hjdesai2'
import NewsJsonAPI
import Mysql
import MysqlConnectors
import simplejson as json

try:
    a = NewsJsonAPI.getJson('ARTICLE')
    print a


finally:
    if MysqlConnectors.cnx:
        MysqlConnectors.cnx.close()