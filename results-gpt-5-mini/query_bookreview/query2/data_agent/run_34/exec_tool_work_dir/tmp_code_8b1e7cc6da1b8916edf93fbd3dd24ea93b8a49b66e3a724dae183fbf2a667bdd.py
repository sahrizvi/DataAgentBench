code = """import json
import pandas as pd

# Load books_info result from the stored JSON file path
books_path = var_call_ti55ZXSDyByyXDgBoTOX2aCL
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Load review avg ratings result (already a list of dicts)
avg_list = var_call_9kZtqWB5ItQeMlNFCf6DaRgo

# Build mapping from purchase_id -> {avg_rating, cnt}
avg_map = {item['purchase_id']: {'avg_rating': float(item['avg_rating']), 'cnt': int(item['cnt'])} for item in avg_list}

# Convert purchase ids to corresponding book ids (fuzzy join assumption)
# e.g., purchaseid_101 -> bookid_101
purchase_to_book = {pid: pid.replace('purchaseid_', 'bookid_') for pid in avg_map.keys()}
bookid_to_pid = {b: p for p, b in purchase_to_book.items()}

# Filter books to those in avg_map (by mapping their book_id to purchase_id)
matches = []
for b in books:
    bid = b.get('book_id')
    # check if this book has a corresponding purchase id with perfect avg rating
    pid = bookid_to_pid.get(bid)
    if pid and avg_map[pid]['avg_rating'] == 5.0:
        # Check English language in details (case-insensitive)
        details = (b.get('details') or '')
        is_english = 'english' in details.lower()
        # Some entries might not have details; also consider categories field
        categories = (b.get('categories') or '')
        if not is_english:
            is_english = 'english' in categories.lower()
        if is_english:
            entry = {
                'book_id': bid,
                'title': b.get('title'),
                'author': b.get('author'),
                'categories': categories,
                'details': details,
                'avg_rating': avg_map[pid]['avg_rating'],
                'review_count_used': avg_map[pid]['cnt'],
                'purchase_id': pid
            }
            matches.append(entry)

# Also consider possibility that some book_ids in books list are not exhaustive; but we return matches found

# Print result in required format
import json as _json
print("__RESULT__:")
print(_json.dumps(matches))"""

env_args = {'var_call_ti55ZXSDyByyXDgBoTOX2aCL': 'file_storage/call_ti55ZXSDyByyXDgBoTOX2aCL.json', 'var_call_9kZtqWB5ItQeMlNFCf6DaRgo': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'cnt': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'cnt': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'cnt': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'cnt': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'cnt': '1'}]}

exec(code, env_args)
