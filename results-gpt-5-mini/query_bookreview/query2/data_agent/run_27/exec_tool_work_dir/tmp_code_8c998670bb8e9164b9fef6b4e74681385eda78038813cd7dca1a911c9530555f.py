code = """import json
import pandas as pd

# Load previous tool results from storage variables
data_file_path = var_call_pxo7Stu0rDxUkmWN0rQtQVZV
perfect_avg_list = var_call_1qwTWp790T1H9kmZFHBpTktN

# Load the large books_info result from the JSON file
with open(data_file_path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# Create DataFrame
df = pd.DataFrame(books_data)

# Build set of candidate book_ids by converting purchase_id -> book_id
candidate_ids = set()
for rec in perfect_avg_list:
    pid = rec.get('purchase_id')
    if not pid:
        continue
    # Common mapping: purchaseid_### -> bookid_###
    if pid.startswith('purchaseid_'):
        candidate_ids.add(pid.replace('purchaseid_', 'bookid_'))
        # also try numeric suffix just in case
        num = pid.split('_')[-1]
        candidate_ids.add('bookid_' + num)
    else:
        # fallback: try direct prefix swap
        candidate_ids.add(pid.replace('purchase', 'book'))

# Filter dataframe for those book_ids
df_candidates = df[df['book_id'].isin(candidate_ids)].copy()

# Further filter for English-language books: check details or categories for the word 'English'
def contains_english(x):
    if not isinstance(x, str):
        return False
    return 'english' in x.lower()

mask_english = df_candidates['details'].apply(contains_english) | df_candidates['categories'].apply(contains_english)

df_final = df_candidates[mask_english]

# Prepare output: list of dicts with selected fields
output = []
for _, row in df_final.iterrows():
    output.append({
        'book_id': row.get('book_id'),
        'title': row.get('title'),
        'author': row.get('author'),
        'categories': row.get('categories'),
        'details': row.get('details')
    })

# If no matches found, return empty list
import json as _json
print("__RESULT__:")
print(_json.dumps(output))"""

env_args = {'var_call_zz0mzsYn9M4KxEuySLUfuFtU': [], 'var_call_7gIqyuoIaynh9DZpe2qntcw2': [{'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'categories': '["Books", "Christian Books & Bibles", "Literature & Fiction"]'}, {'categories': '["Books", "Literature & Fiction", "Classics"]'}, {'categories': '["Books", "Literature & Fiction", "Contemporary"]'}, {'categories': '["Books", "Literature & Fiction", "Dramas & Plays"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Literature & Fiction", "Humor & Satire"]'}, {'categories': '["Books", "Literature & Fiction", "Mythology & Folk Tales"]'}, {'categories': '["Books", "Literature & Fiction", "Poetry"]'}, {'categories': '["Books", "Literature & Fiction", "Short Stories & Anthologies"]'}, {'categories': '["Books", "Literature & Fiction", "United States"]'}, {'categories': '["Books", "Literature & Fiction"]'}], 'var_call_pxo7Stu0rDxUkmWN0rQtQVZV': 'file_storage/call_pxo7Stu0rDxUkmWN0rQtQVZV.json', 'var_call_1qwTWp790T1H9kmZFHBpTktN': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0'}]}

exec(code, env_args)
