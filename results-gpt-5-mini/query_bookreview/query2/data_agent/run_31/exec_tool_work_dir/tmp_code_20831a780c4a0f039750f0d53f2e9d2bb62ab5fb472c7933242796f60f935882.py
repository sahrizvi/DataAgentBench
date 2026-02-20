code = """import json
import pandas as pd

# Load review avg=5 results available as variable
reviews = var_call_2YAKINXxuD7N0MmLcqlqKbUi

# Load books_info query result from the stored JSON file path
books_file = var_call_qeSYvmijaf6CxiHjnodfRJFI
with open(books_file, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Map purchase_id -> book_id by replacing prefix
mapped = {}
for r in reviews:
    pid = r.get('purchase_id')
    if pid is None:
        continue
    bid = pid.replace('purchaseid_', 'bookid_')
    mapped[bid] = r

# Filter books to those whose book_id is in mapped keys and language English present in details or categories
matches = []
for b in books:
    bid = b.get('book_id')
    if bid in mapped:
        details = (b.get('details') or '')
        categories = (b.get('categories') or '')
        # check for English language mention
        if ('english' in details.lower()) or ('english' in categories.lower()):
            r = mapped[bid]
            matches.append({
                'book_id': bid,
                'title': b.get('title'),
                'author': b.get('author'),
                'categories': categories,
                'details': details,
                'purchase_id': r.get('purchase_id'),
                'avg_rating': float(r.get('avg_rating')) if r.get('avg_rating') is not None else None,
                'count_reviews': int(r.get('count_reviews')) if r.get('count_reviews') is not None else None
            })

# If no matches found (possible due to mismatched prefixes), try alternative mapping: replace 'purchaseid_' with 'bookid_' but also handle numeric-only match
if not matches:
    # Build set of numeric ids from purchase ids
    purchased_nums = set()
    for r in reviews:
        pid = r.get('purchase_id')
        if pid and pid.startswith('purchaseid_'):
            try:
                num = pid.split('_')[1]
                purchased_nums.add(num)
            except:
                pass
    for b in books:
        bid = b.get('book_id')
        if bid and bid.startswith('bookid_'):
            try:
                num = bid.split('_')[1]
                if num in purchased_nums:
                    details = (b.get('details') or '')
                    categories = (b.get('categories') or '')
                    if ('english' in details.lower()) or ('english' in categories.lower()):
                        # find corresponding purchase record
                        pid = 'purchaseid_' + num
                        r = next((x for x in reviews if x.get('purchase_id')==pid), None)
                        matches.append({
                            'book_id': bid,
                            'title': b.get('title'),
                            'author': b.get('author'),
                            'categories': categories,
                            'details': details,
                            'purchase_id': pid,
                            'avg_rating': float(r.get('avg_rating')) if r and r.get('avg_rating') is not None else None,
                            'count_reviews': int(r.get('count_reviews')) if r and r.get('count_reviews') is not None else None
                        })
            except:
                pass

# Prepare JSON-serializable output
output = matches

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_glxEGMnCnuLfipw5z5ROBNdQ': ['books_info'], 'var_call_PuYSaDKkfAyWQXnUdHrSh3e5': ['review'], 'var_call_2YAKINXxuD7N0MmLcqlqKbUi': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'count_reviews': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'count_reviews': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'count_reviews': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'count_reviews': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'count_reviews': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'count_reviews': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'count_reviews': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'count_reviews': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'count_reviews': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'count_reviews': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'count_reviews': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'count_reviews': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'count_reviews': '1'}], 'var_call_qeSYvmijaf6CxiHjnodfRJFI': 'file_storage/call_qeSYvmijaf6CxiHjnodfRJFI.json'}

exec(code, env_args)
