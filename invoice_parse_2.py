import pymysql

json_data = "{'name' : 'Tom', 'age' : '24'}"


class MySQLUtil():
    def connectDB(self, host, user, psw, db_name, charset='utf8'):
        self.db = pymysql.connect(host=host, user=user, password=psw, db=db_name, charset=charset)

    def closeDB(self):
        self.db.close()

    def execQuery(self, sql):
        try:
            # execute sql statement
            cursor = self.db.cursor()
            cursor.execute(sql)
            # get all rows in mysql
            results = cursor.fetchall()
            return results
        except:
            print("Error: unable to fecth data")
            return None

    def execSql(self, sql):
        # sql is insert, delete or update statement
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            # commit sql to mysql
            self.db.commit()
            cursor.close()
            return True
        except:
            self.db.rollback()
        return False


mysql = MySQLUtil()
mysql.connectDB(host='localhost', user='root', psw='Qazx1324!', db_name='NZU')
json_data = pymysql.escape_string(json_data)
sql = "insert into all_tag ( index_name) values ('" + json_data + "') "
mysql.execSql(sql)
mysql.closeDB()