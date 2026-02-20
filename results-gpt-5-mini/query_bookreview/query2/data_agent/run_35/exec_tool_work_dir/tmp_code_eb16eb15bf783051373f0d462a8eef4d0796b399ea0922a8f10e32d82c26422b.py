code = """import json
# var_call_mKflDLVW691SadhIyQVDUqE7 is the path to the large JSON file with books query results
books_path = var_call_mKflDLVW691SadhIyQVDUqE7
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
# var_call_gM7Pn0HdH3AdN7SuMowaDwVi is the reviews aggregate list
reviews = var_call_gM7Pn0HdH3AdN7SuMowaDwVi

# Build dict for quick lookup of books by book_id
books_by_id = {b['book_id']: b for b in books}

results = []
for r in reviews:
    purchase_id = r.get('purchase_id')
    if not purchase_id:
        continue
    # extract numeric suffix
    parts = purchase_id.split('_')
    if len(parts) < 2:
        continue
    num = parts[-1]
    book_id = f'bookid_{num}'
    book = books_by_id.get(book_id)
    if not book:
        continue
    details = (book.get('details') or '')
    # check if English-language mentioned in details (case-insensitive)
    if 'english' not in details.lower():
        continue
    # Confirm the categories include Literature & Fiction (should already)
    categories = (book.get('categories') or '')
    if 'literature & fiction' not in categories.lower() and 'literature & fiction' not in details.lower():
        continue
    # Build result record
    try:
        avg_rating = float(r.get('avg_rating'))
    except:
        try:
            avg_rating = float(r.get('avg_rating', 0))
        except:
            avg_rating = None
    try:
        ratings_count = int(r.get('ratings_count'))
    except:
        ratings_count = None
    results.append({
        'book_id': book_id,
        'title': book.get('title'),
        'categories': book.get('categories'),
        'details': book.get('details'),
        'avg_rating': avg_rating,
        'ratings_count': ratings_count
    })

# Deduplicate by book_id (if any duplicates)
seen = set()
unique_results = []
for rec in results:
    if rec['book_id'] in seen:
        continue
    seen.add(rec['book_id'])
    unique_results.append(rec)

import json as _json
out = _json.dumps(unique_results)
print("__RESULT__:")
print(out)"""

env_args = {'var_call_rYrvSPcYhBC0gLH7M8xjih5W': ['books_info'], 'var_call_aMJtpRJ3SRVSMA0aeCMymfV7': ['review'], 'var_call_mKflDLVW691SadhIyQVDUqE7': 'file_storage/call_mKflDLVW691SadhIyQVDUqE7.json', 'var_call_gM7Pn0HdH3AdN7SuMowaDwVi': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'ratings_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'ratings_count': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'ratings_count': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'ratings_count': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'ratings_count': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'ratings_count': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'ratings_count': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'ratings_count': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'ratings_count': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'ratings_count': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'ratings_count': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'ratings_count': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'ratings_count': '1'}]}

exec(code, env_args)
