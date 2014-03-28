__author__ = 'hjdesai2'
from IPython.utils._process_posix import system
__author__ = 'hjdesai2'
import Mysql
import MysqlConnectors
import simplejson as json
try:
    NewsJsonCursor = MysqlConnectors.cnx.cursor()

    def getJson(file):
        NewsJson = Mysql.select_data(file,NewsJsonCursor)
        b = json.dumps(NewsJson,indent=4 * ' ')
        return b

except:
    print (SystemError)
