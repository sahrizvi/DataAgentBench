code = """import json
import pandas as pd

# Load data from storage files
with open(var_call_Mg0T2w7pQxDBuG1N4IkzzBN7, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_z2B2TKQ77Eu9WTQi3Gsnwpnd, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Create DataFrames
dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# Filter books for Literature & Fiction and English language
mask_cat = dfb['categories'].str.contains('Literature & Fiction', case=False, na=False)
mask_eng = dfb['details'].str.contains('English', case=False, na=False)
dfb_filtered = dfb[mask_cat & mask_eng].copy()

# Extract numeric id suffix for joining
dfb_filtered['id_num'] = dfb_filtered['book_id'].astype(str).str.split('_').str[-1]
dfr['id_num'] = dfr['purchase_id'].astype(str).str.split('_').str[-1]

# Convert ratings to numeric
dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

# Compute average rating per id_num
avg = dfr.groupby('id_num', as_index=False)['rating'].mean()

# Select those with perfect average of 5.0
perfect = avg[avg['rating'] == 5.0]

# Join with filtered books
res = dfb_filtered.merge(perfect, on='id_num', how='inner')

# Prepare output records
out = res[['book_id', 'title', 'categories', 'details']].to_dict(orient='records')

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_Px29ckng94cKeoHIggTLMxSC': ['books_info'], 'var_call_Mg0T2w7pQxDBuG1N4IkzzBN7': 'file_storage/call_Mg0T2w7pQxDBuG1N4IkzzBN7.json', 'var_call_0UK3sCWp7Lwqo9DXljbOIuIc': ['review'], 'var_call_z2B2TKQ77Eu9WTQi3Gsnwpnd': 'file_storage/call_z2B2TKQ77Eu9WTQi3Gsnwpnd.json'}

exec(code, env_args)
