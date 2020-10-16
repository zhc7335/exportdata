import sys
import csv
import cx_Oracle

connection = input("Enter Oracle DB connection (uid/pwd@database) : ")
orcl = cx_Oracle.connect(connection)
curs = orcl.cursor()
printHeader = True  # include column headers in each table output
sql = "select * from tab"  # get a list of all tables
curs = curs.execute(sql)
#print(curs)
for row_data in curs:
    if not str(row_data[0]).startswith('BIN$'):  # skip recycle bin tables
        tableName = str(row_data[0])
        #print(tableName)
        # output each table content to a separate CSV file
        csv_file_dest = tableName + ".csv"
        outputFile = open(csv_file_dest, 'w')  # 'wb'
        output = csv.writer(outputFile, dialect='excel')
        sql = "select * from " + tableName
        curs2 = orcl.cursor()
        curs2.execute(sql)
        if printHeader:  # add column headers if requested
            cols = []
            for col in curs2.description:
                cols.append(col[0])
            output.writerow(cols)
        for row_data in curs2:  # add table rows
            output.writerow(row_data)
        outputFile.close()
