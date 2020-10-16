import sys
import csv
import cx_Oracle


class ExportOracle():
    def __init__(self):
        self.oracleconnection = input("Enter Oracle DB connection (uid/pwd@database) : ")
        # name = str(name)
        # pwd = str(pwd)
        # host = str(host)
        # port = str(port)
        # db = str(db)
        # self.oracleconnection = name/pwd@host:port/db

        # def link_Oracle(self, tablename):
        # connection = cx_Oracle.connect(self.name,self.pwd,self.ip/self.SID)
        # connection = cx_Oracle.connect(self.connection)
        # #printHeader = True
        # sql = '''
        #         select * from %s
        #       ''' % tablename
        # cursor = connection.cursor()
        # cursor.execute(sql)
        # #print(cur)
        # return cursor
        # print(cursor)

    def export_oracle_data(self, oradbname):
        # self.link_Oracle(tablename=oradbname)
        connection = cx_Oracle.connect(self.oracleconnection)
        csv_file_dest = oradbname + ".csv"
        outputFile = open(csv_file_dest, 'w',newline='')
        output = csv.writer(outputFile, dialect='excel')
        sql = '''
                        select * from %s
                      ''' % oradbname
        cursor = connection.cursor()
        cursor.execute(sql)
        cols = []
        for col in cursor.description:
            cols.append(col[0])
        output.writerow(cols)
        for row_data in cursor:
            output.writerow(row_data)
        print('恭喜大哥成功导出' + csv_file_dest + '！！！！')

        outputFile.close()

    # def export_mysql_data(self,mysqldbname):
