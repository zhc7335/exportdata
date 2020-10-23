import pymysql
import pandas as pd

# 参数设置 DictCursor使输出为字典模式 连接到本地用户ffzs 密码为666
config = dict(host='localhost', user='root', password='636458', port=3306,
              cursorclass=pymysql.cursors.DictCursor
              )
# 建立连接
conn = pymysql.Connect(**config)
# 自动确认commit True
conn.autocommit(1)
# 设置光标
cursor = conn.cursor()

df = pd.read_csv('emp.csv', encoding='gbk', parse_dates=['HIREDATE'])


# 一个根据pandas自动识别type来设定table的type
def make_table_sql(df):
    columns = df.columns.tolist()
    types = df.dtypes
    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in str(df[item].dtype):
            char = item + ' INT'
        elif 'float' in str(df[item].dtype):
            char = item + ' FLOAT'
        elif 'object' in str(df[item].dtype):
            char = item + ' VARCHAR(255)'
        elif 'datetime' in str(df[item].dtype):
            char = item + ' DATETIME'
        make_table.append(char)
    return ','.join(make_table)


# csv 格式输入 mysql 中
def csv2mysql(db_name, table_name, df):
    # 创建database
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE {}({})'.format(table_name, make_table_sql(df)))
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    df['HIREDATE'] = df['HIREDATE'].astype('str')
    values = df.values.tolist()
    # 根据columns个数
    '''
    for i in range(len(values)):
        # for y in range(len(df.columns)):
        # print(values[i][y])
        sb = ','.join(['%s' % values[i][y] for y in range(len(df.columns))])
        cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, sb), values)
    '''

    sb = ','.join(['%s' % df.columns[y] for y in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    z = '%s,' * len(df.columns)
    sql = "INSERT INTO {} ({}) VALUES ('%s')"%z.format(table_name, sb)
    cursor.executemany(sql, values)
    # cursor.executemany('INSERT INTO {} ({}) VALUES ({})'.format(table_name, sb), values)
    print("Write to MySQL successfully!")


if __name__ == '__main__':
    csv2mysql(db_name='petzhang', table_name='test1', df=df)
