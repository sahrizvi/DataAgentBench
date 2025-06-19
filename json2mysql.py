import pandas as pd
from sqlalchemy import create_engine, types

# ✅ 修改为你的 root 密码
password = "20041025"

# ✅ 创建连接
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/ucb_db")

# ✅ 读取 JSON 文件
df = pd.read_json("googlelocal_query/dataset/light_meta_LLM.json", lines=True)

# ✅ 定义字段类型，保留 JSON 结构
dtype_map = {
    'name': types.Text(),
    'gmap_id': types.Text(),
    'description': types.Text(),
    'num_of_reviews': types.Integer(),
    'hours': types.JSON(),
    'MISC': types.JSON(),
    'state': types.Text()
}

# ✅ 写入数据库表名为 meta
df.to_sql("meta", con=engine, if_exists="replace", index=False, dtype=dtype_map)

print("✅ 数据写入完成：表名 meta")
