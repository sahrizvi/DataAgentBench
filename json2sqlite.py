import pandas as pd
import sqlite3

# 读取 JSON Lines 文件
df = pd.read_json("googlelocal_query/dataset/light_review_LLM.json", lines=True)

# 创建 SQLite 数据库连接（自动生成文件）
conn = sqlite3.connect("googlelocal_query/dataset/review_query.db")

# 写入数据库，表名为 "meta"
df.to_sql("meta", conn, if_exists="replace", index=False)

# 关闭数据库连接
conn.close()

print("已成功将 JSON 转换为 SQLite 数据库")
