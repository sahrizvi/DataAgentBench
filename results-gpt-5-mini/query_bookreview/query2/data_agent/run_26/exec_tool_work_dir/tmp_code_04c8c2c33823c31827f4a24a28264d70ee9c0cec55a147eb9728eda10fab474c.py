code = """import json

# Load books list from file (path provided in var_call_MNwN8NPK9hFIjltn8L2YYMNF)
with open(var_call_MNwN8NPK9hFIjltn8L2YYMNF, 'r') as f:
    books = json.load(f)

# Reviews average-rating results
reviews = var_call_5aOB940nZLiYBBXGtePzOlyc

# Convert purchase_id values to corresponding book_id format (assumes numeric suffix mapping)
bookids = set()
for r in reviews:
    pid = r.get('purchase_id','')
    if pid.startswith('purchaseid_'):
        suffix = pid.split('_',1)[1]
        bookids.add('bookid_' + suffix)
    else:
        # fallback: replace 'purchaseid' with 'bookid'
        bookids.add(pid.replace('purchaseid','bookid'))

# Filter books that are English-language and in Literature & Fiction (books list already queried for that category)
matches = []
for b in books:
    bid = b.get('book_id')
    details = (b.get('details') or '')
    categories = (b.get('categories') or '')
    # Check English in details (case-insensitive)
    if bid in bookids and 'english' in details.lower():
        matches.append({
            'book_id': bid,
            'title': b.get('title'),
            'author': b.get('author'),
            'categories': categories,
            'details': details
        })

print("__RESULT__:")
print(json.dumps(matches))"""

env_args = {'var_call_MNwN8NPK9hFIjltn8L2YYMNF': 'file_storage/call_MNwN8NPK9hFIjltn8L2YYMNF.json', 'var_call_5aOB940nZLiYBBXGtePzOlyc': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'num_reviews': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'num_reviews': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'num_reviews': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'num_reviews': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'num_reviews': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'num_reviews': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'num_reviews': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'num_reviews': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'num_reviews': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'num_reviews': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'num_reviews': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'num_reviews': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'num_reviews': '1'}]}

exec(code, env_args)
