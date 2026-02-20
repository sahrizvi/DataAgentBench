code = """import json
# var_call_nfVRM3R5JcmBVotXKMDye8fM contains the filepath to the JSON result from previous execute_python
results_path = var_call_nfVRM3R5JcmBVotXKMDye8fM
with open(results_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build plain-text answer lines
lines = []
for item in data:
    title = item.get('title') or ''
    book_id = item.get('book_id') or ''
    avg = item.get('avg_rating')
    n = item.get('n_reviews')
    # Format avg to 2 decimal places
    try:
        avg_f = float(avg)
        avg_s = f"{avg_f:.2f}"
    except:
        avg_s = str(avg)
    lines.append(f"{title} ({book_id}) — average rating: {avg_s} based on {n} review(s)")

final_text = "\n".join(lines)
# Print in required format as JSON string
print("__RESULT__:")
print(json.dumps(final_text))"""

env_args = {'var_call_Tng5mCe3ePl7vmyoS8qy1i9d': ['books_info'], 'var_call_hqtPEL2s4qggFdG4s5Lo6amG': ['review'], 'var_call_yVmYizuMroNQUrFDdgMR0wr0': [{'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'n_reviews': '14'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'n_reviews': '8'}, {'purchase_id': 'purchaseid_10', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_154', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'n_reviews': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_3', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_66', 'avg_rating': '5.0', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_129', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_169', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_185', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_187', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_196', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_198', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_200', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_22', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_37', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_4', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_46', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_55', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_94', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_96', 'avg_rating': '5.0', 'n_reviews': '1'}, {'purchase_id': 'purchaseid_13', 'avg_rating': '4.923076923076923', 'n_reviews': '13'}, {'purchase_id': 'purchaseid_149', 'avg_rating': '4.9', 'n_reviews': '10'}, {'purchase_id': 'purchaseid_178', 'avg_rating': '4.795918367346939', 'n_reviews': '49'}, {'purchase_id': 'purchaseid_115', 'avg_rating': '4.75', 'n_reviews': '8'}, {'purchase_id': 'purchaseid_48', 'avg_rating': '4.75', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_76', 'avg_rating': '4.75', 'n_reviews': '4'}, {'purchase_id': 'purchaseid_8', 'avg_rating': '4.709677419354839', 'n_reviews': '31'}, {'purchase_id': 'purchaseid_158', 'avg_rating': '4.708333333333333', 'n_reviews': '24'}, {'purchase_id': 'purchaseid_161', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_23', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_50', 'avg_rating': '4.5', 'n_reviews': '2'}, {'purchase_id': 'purchaseid_72', 'avg_rating': '4.5', 'n_reviews': '2'}], 'var_call_pMzup00cJgwgrzd5iyvLnWVn': 'file_storage/call_pMzup00cJgwgrzd5iyvLnWVn.json', 'var_call_nfVRM3R5JcmBVotXKMDye8fM': 'file_storage/call_nfVRM3R5JcmBVotXKMDye8fM.json'}

exec(code, env_args)
