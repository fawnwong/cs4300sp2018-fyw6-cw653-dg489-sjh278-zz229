import Levenshtein  # package python-Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import os
import csv
import re
import cPickle
# from app.irsystem.models.helpers import *
# from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import urllib

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
#with open(os.path.join(APP_ROOT, '../data/data.json')) as f:
#	bot_data = json.loads(f.readlines()[0])
bot_data  = cPickle.load( open(os.path.join(APP_ROOT, '../data/bot_data.p'), "rb" ) )

#with open(os.path.join(APP_ROOT, '../data/BigBotComments.json')) as f:
#	big_bot_data = json.loads(f.readlines()[0])
big_bot_data  = cPickle.load( open(os.path.join(APP_ROOT, '../data/big_bot_data.p'), "rb" ) )
# json.dump(big_bot_data, open('BigBotComments.json', 'w'), cls=NumpyEncoder)
# awsurl = urllib.urlopen('https://s3.us-east-2.amazonaws.com/beepboop4300/BigBotComments.json')
# json.load(awsurl)
# # Read numpy array from a json file (where FILE_NAME is an S3 location or local file)
# BigBotComments = json.load(awsurl, object_hook=json_numpy_obj_hook, encoding='utf8')

bot_names = bot_data.keys()
botname_to_index = {botname:index for index, botname in enumerate(bot_data.keys())}
index_to_botname = {v:k for k,v in botname_to_index.items()}

n_feats = 2000
doc_by_vocab = np.empty([len(bot_data), n_feats])

	
tfidf_vec = cPickle.load( open(os.path.join(APP_ROOT, '../data/vectorizer.p'), "rb" ) )
doc_by_vocab = tfidf_vec.fit_transform([bot_data[d] for d in bot_data.keys()]).toarray()

def top_n_cos(n,query_string, tfidf):
	q_vec = tfidf.transform([query_string]).toarray()
	cosines = np.array([np.dot(q_vec, d) for d in doc_by_vocab]).T[0]
	args = np.argsort(cosines)[::-1][:n]
	return [(index_to_botname[x], bot_data[index_to_botname[x]]) for x in args]

def edit_distance(query_str, msg_str):
	return Levenshtein.distance(query_str.lower(), msg_str.lower())

def similar_names(query, msgs):
	li = [(edit_distance(query, msg),msg) for msg in msgs]
	li.sort(key=lambda x: x[0])
	return li[0:5]

def getUserCommentResults(query, bot_names_list, user_comments):
	results = {}

	# search through source files for match 
	# with open(os.path.join(APP_ROOT+"/../data/", user_comments)) as csvfile:
	# 	reader = csv.reader(csvfile) 
	# 	for row in reader:
	# 		row_res = []
	# 		category = row[0]	
	# 		print(category)			
	# 		rel_bots = row[1]
	# 		postings = rel_bots.split(')')
	# 		for posting in postings:
	# 			if re.search('[0-9]', posting):
	# 				tup = posting.split(',')

	# 				found = []
	# 				for i in range(len(tup)):
	# 					find_dec = re.search(r'[0-9]+.[0-9]+', tup[i])
	# 					if find_dec:
	# 						num = find_dec.group(0)
	# 						found.append(num)
	# 					else: 
	# 						find_num = re.search(r'[0-9]+', tup[i])
	# 						if find_num:
	# 							num = find_num.group(0)
	# 							found.append(num)


	# 				if len(found) > 0:
	# 					bot_id = found[0]
	# 					bot_score = found[1]
	# 					row_res.append((int(bot_id), float(bot_score)))
	# 		results[category] = row_res


	# with open('user_results.json', "r") as infile:
	# 	json.dump(results, outfile)
	# 	print("HELLO")

	#with open(os.path.join(APP_ROOT, '../data/user_results.json')) as infile:
		#result_dict = json.load(infile)
	result_dict = cPickle.load( open(os.path.join(APP_ROOT, '../data/user_results.p'), "rb" ) )

	if (query in result_dict.keys()):
		results = result_dict[query]
		sorted_by_score = sorted(results, key=lambda tup: tup[1])

		top5 = sorted_by_score[::-1][5:]
		if top5:
			max_score = float(top5[0][1])

		# get bot list from input csv
		with open(os.path.join(APP_ROOT, '../data/'+bot_names_list)) as csvfile:
			reader = csv.reader(csvfile) 
			bot_list = list(reader)

		final_results = []
		if top5:
			for result in top5:
				bot_index = int(result[0])
				bot_name = bot_list[bot_index][0]
				bot_score = float(result[1]) / max_score
				final_results.append((bot_name,bot_score))
			return final_results
	return False


def bot_to_list(query):
	if query == None:
		return []
	edit_dist = similar_names(query, bot_names)
	cos_sim = top_n_cos(5,query, tfidf_vec)

	bot_names_list = 'bot_names.csv'
	user_comments = 'user_comment_data.csv'

	query_words = query.split()
	for query in query_words:
		myresults = getUserCommentResults(query, bot_names_list, user_comments)
		if myresults:
			break

	if not myresults:
		myresults = [("no category",0) , ("no category",0) , ("no category",0) , ("no category",0) , ("no category", 0)]
		
	data = [{"rank": "1", "list": [{"name": edit_dist[0][1], "comment": "A Comment 1", "link": "http://reddit.com/u/"+ edit_dist[0][1], "category": "bot_name"},
								   {"name": cos_sim[0][0], "comment": "B Comment 1", "link": "http://reddit.com/u/"+cos_sim[0][0], "category": "bot_comments"},
								   {"name": myresults[0][0], "comment": "C Comment 1", "link": "http://reddit.com/u/" + myresults[0][0], "category": "user_comments"}
								   ]},
			{"rank": "2",
			"list": [
					 {"name": edit_dist[1][1], "comment": "A Comment 2", "link": "http://reddit.com/u/" + edit_dist[1][1], "category": "bot_name"},
					 {"name": cos_sim[1][0], "comment": "B Comment 2", "link": "http://reddit.com/u/"+cos_sim[1][0], "category": "bot_comments"},
					 {"name": myresults[1][0], "comment": "C Comment 2", "link": "http://reddit.com/u/" + myresults[1][0], "category": "user_comments"}
					 ]},
			{"rank": "3",
			"list": [
					 {"name": edit_dist[2][1], "comment": "A Comment 3", "link": "http://reddit.com/u/" + edit_dist[2][1], "category": "bot_name"},
					 {"name": cos_sim[2][0], "comment": "B Comment 3", "link": "http://reddit.com/u/"+cos_sim[2][0], "category": "bot_comments"},
					 {"name": myresults[2][0], "comment": "C Comment 3", "link": "http://reddit.com/u/" + myresults[2][0], "category": "user_comments"}
					 ]},
			{"rank": "4",
			"list": [
					 {"name": edit_dist[3][1], "comment": "A Comment 4", "link": "http://reddit.com/u/" + edit_dist[3][1], "category": "bot_name"},
					 {"name": cos_sim[3][0], "comment": "B Comment 4", "link": "http://reddit.com/u/"+cos_sim[3][0], "category": "bot_comments"},
					 {"name": myresults[3][0], "comment": "C Comment 4", "link": "http://reddit.com/u/" + myresults[3][0], "category": "user_comments"}
					 ]},
			{"rank": "5",
			"list": [
					 {"name": edit_dist[4][1], "comment": "A Comment 5", "link":"http://reddit.com/u/" + edit_dist[4][1], "category": "bot_name"},
					 {"name": cos_sim[4][0], "comment": "B Comment 5", "link": "http://reddit.com/u/"+cos_sim[4][0], "category": "bot_comments"},
					 {"name": myresults[4][0], "comment": "C Comment 5", "link": "http://reddit.com/u/" + myresults[4][0], "category": "user_comments"}
					 ]},
			]
	return data


