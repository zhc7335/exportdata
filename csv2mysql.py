import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接，使用pymysql模块
engine = create_engine('mysql+pymysql://root:636458@localhost:3306/petzhang')


def csv2mysql():
    df = pd.read_csv("emp.csv", sep=',')
    df.to_sql('zhc', engine, index=False)
    print("Write to MySQL successfully!")


if __name__ == '__main__':
    csv2mysql()