code = """book_ids = [book['book_id'] for book in locals()['var_function-call-16143543152546113720']]
query_ids = ', '.join([f"'{book_id}'" for book_id in book_ids])
print("__RESULT__:")
print(query_ids)"""

env_args = {'var_function-call-15574486260342063264': ['books_info'], 'var_function-call-7224679516982311077': 'file_storage/function-call-7224679516982311077.json', 'var_function-call-16143543152546113720': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_9'}, {'book_id': 'bookid_13'}, {'book_id': 'bookid_30'}, {'book_id': 'bookid_36'}, {'book_id': 'bookid_37'}, {'book_id': 'bookid_38'}, {'book_id': 'bookid_39'}, {'book_id': 'bookid_44'}, {'book_id': 'bookid_49'}, {'book_id': 'bookid_55'}, {'book_id': 'bookid_69'}, {'book_id': 'bookid_70'}, {'book_id': 'bookid_74'}, {'book_id': 'bookid_77'}, {'book_id': 'bookid_82'}, {'book_id': 'bookid_84'}, {'book_id': 'bookid_89'}, {'book_id': 'bookid_92'}, {'book_id': 'bookid_93'}, {'book_id': 'bookid_98'}, {'book_id': 'bookid_99'}, {'book_id': 'bookid_101'}, {'book_id': 'bookid_106'}, {'book_id': 'bookid_109'}, {'book_id': 'bookid_111'}, {'book_id': 'bookid_122'}, {'book_id': 'bookid_137'}, {'book_id': 'bookid_142'}, {'book_id': 'bookid_144'}, {'book_id': 'bookid_161'}, {'book_id': 'bookid_167'}, {'book_id': 'bookid_171'}, {'book_id': 'bookid_177'}, {'book_id': 'bookid_179'}, {'book_id': 'bookid_180'}, {'book_id': 'bookid_182'}, {'book_id': 'bookid_187'}, {'book_id': 'bookid_188'}, {'book_id': 'bookid_195'}]}

exec(code, env_args)
