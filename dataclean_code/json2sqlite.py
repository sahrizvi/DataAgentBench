import pandas as pd
import sqlite3

df = pd.read_json("googlelocal_query/dataset/light_review_LLM.json", lines=True)

conn = sqlite3.connect("googlelocal_query/dataset/review_query.db")

df.to_sql("meta", conn, if_exists="replace", index=False)

conn.close()

print("已成功将 JSON 转换为 SQLite 数据库")
