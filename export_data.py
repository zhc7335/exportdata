import sys
import csv
import cx_Oracle
import pymysql
import xlwt
import os


class ExportData():
    def __init__(self):

        db_type = input("请输入数据库类型(输入1或2：1=oracle/2=mysql):")
        if db_type == '1':
            self.oracleconnection = input("Enter Oracle DB connection (uid/pwd@database) : ")

        elif db_type == '2':
            host = input("请输入数据库服务器IP：")
            user = input("请输入您的数据库用户名：")
            pwd = input("请输入您的用户密码：")
            dbname = input("请输入您想连接的数据库名称：")
            self.host = str(host)
            self.user = str(user)
            self.pwd = str(pwd)
            self.dbname = str(dbname)
        else:
            print("请您输入正确的数据库类型！！！")
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

    def export_all_oracle_data(self):
        try:
            db_name1 = self.oracleconnection.split('/')
            db_name2 = db_name1[2]
            try:
                connection = cx_Oracle.connect(self.oracleconnection)
            except Exception as e:
                print('数据库连接信息输入错误，请重新输入！！！')
            cursor = connection.cursor()
            sql = '''
                        select * from tab
                                      '''
            cursor.execute(sql)
            output_file = "%s.csv" % db_name2
            workbook = xlwt.Workbook(output_file)
            for sheet in cursor:
                # print(sheet)
                if not str(sheet[0]).startswith('BIN$'):  # skip recycle bin tables
                    tableName = str(sheet[0])
                    # print(tableName)
                    worksheet = workbook.add_sheet(tableName)
                    # outputFile = open(output_file, 'w', sheet_name=tableName, newline='')
                    # output = csv.writer(outputFile, dialect='excel')
                    sql = '''
                                                select * from %s
                                              ''' % tableName
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    fields = cursor.description
                    for field in range(0, len(fields)):
                        # output.writerow(cols)
                        worksheet.write(0, field, fields[field][0])
                    for row_data in range(1, len(results) + 1):
                        for col in range(0, len(fields)):
                            # output.writerow(row_data)
                            worksheet.write(row_data, col, u'%s' % results[row_data - 1][col])
            workbook.save(output_file)
            print('恭喜大哥成功导出' + output_file + '！！！！')
        except Exception as e:
            print('数据导出失败！！！请重试！！！')

    def export_oracle_data(self, oradbname):
        try:
            # self.link_Oracle(tablename=oradbname)
            try:
                connection = cx_Oracle.connect(self.oracleconnection)
            except Exception as e:
                print('数据库连接信息输入错误，请重新输入！！！')
            csv_file_dest = oradbname + ".csv"
            outputFile = open(csv_file_dest, 'w', newline='')
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
        except Exception as e:
            print('数据导出失败！！！请重试！！！')

    def export_mysql_structure(self):
        connection = pymysql.connect(self.host, self.user, self.pwd, self.dbname)
        # cursor = connection.cursor()
        # sql = '''
        #             select table_name from information_schema.tables
        #                           '''

        os.system("mysqldump --column-statistics=0 -h%s -uroot -p%s %s > %s.sql" % (self.host, self.pwd, self.dbname, self.dbname))

        print('恭喜大哥成功导出' + self.dbname + '数据库结构！！！')
        #while True:
            # DATETIME = time.strftime('%Y%m%d-%H%M%S')
            # TODAYBACKUPPATH = BACKUP_PATH + DATETIME
            #print("createing backup folder!")
            # 创建备份文件夹
            # if not os.path.exists(TODAYBACKUPPATH):
            #     os.makedirs(TODAYBACKUPPATH)
            # in_file = open('%s.sql' % self.dbname, "r")
            # for dbname in in_file.readlines():
            #     dbname = dbname.strip()
            #     print("now starting backup database %s" % dbname)
            #     dumpcmd = "mysqldump --single-transaction -h" + self.host + " -u" + self.user + " -p" + self.pwd + " " + self.dbname + " > " + self.dbname + ".sql"
            #     print(dumpcmd)
            #     os.system(dumpcmd)
            # file1.close()

    def export_mysql_data(self, tablename):
        try:
            try:
                connection = pymysql.connect(self.host, self.user, self.pwd, self.dbname)
            except Exception as e:
                print('数据库连接信息输入错误，请重新输入！！！')
            cursor = connection.cursor()
            sql = '''
                            select * from %s
                          ''' % tablename
            cursor.execute(sql)
            cursor.scroll(0, mode='absolute')
            data = cursor.fetchall()
            fields = cursor.description
            filename = '%s.csv' % tablename
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                write = csv.writer(f, dialect='excel')
                cols = []
                for col in fields:
                    cols.append(col[0])
                write.writerow(cols)
                for item in data:
                    write.writerow(item)
            print('恭喜大哥成功导出' + filename + '！！！！')

        except Exception as e:
            print('数据导出失败！！！请重试！！！')
