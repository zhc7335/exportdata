import pandas as pd
import numpy

df = pd.read_csv('emp.csv', encoding='gbk', parse_dates=['HIREDATE'])
values = df.values.tolist()
print(len(df.columns))
# for i in range(len(values)):
# for y in range(len(df.columns)):
# print(values[i][y])

sb = ','.join(['%s' % df.columns[y] for y in range(len(df.columns))])
#     #print(",".join(sb))
# #print(sb)
table_name = 'zhc'
z = '%s,' * len(df.columns)
print(z)
print("INSERT INTO {} ({}) VALUES ('%s')"%z.format(table_name, sb))
# sb = ','.join(['%s'% values for _ in range(len(df.columns))])
# print(sb)
