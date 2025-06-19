import sqlite3
import pandas as pd

# 打开数据库文件
conn = sqlite3.connect("googlelocal_query/dataset/review_query.db")

# 查看有哪些表
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

# 读取某个表的数据
df = pd.read_sql("SELECT * FROM meta;", conn)
print(df.head())

conn.close()
