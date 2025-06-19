import pandas as pd
from sqlalchemy import create_engine, types

password = "20041025"

engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/ucb_db")

df = pd.read_json("googlelocal_query/dataset/light_meta_LLM.json", lines=True)

dtype_map = {
    'name': types.Text(),
    'gmap_id': types.Text(),
    'description': types.Text(),
    'num_of_reviews': types.Integer(),
    'hours': types.JSON(),
    'MISC': types.JSON(),
    'state': types.Text()
}

df.to_sql("meta", con=engine, if_exists="replace", index=False, dtype=dtype_map)

print("数据写入完成：表名 meta")
