import json
import glob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import string
from collections import Counter
# import nltk
from nltk.stem.porter import *
import unicodedata as uni
import math


def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def strip_punctuation(word):
	return "".join(char for char in word if uni.category(char).startswith('P'))

def freq(word, doc):
	return doc.count(word)

def tf(word, doc):
	return (freq(word, doc) / float(len(doc)))

def num_docs_containing(word, list_of_docs):
	count = 0
	for doc in list_of_docs:
		if freq(word, doc) > 0:
			count+= 1
	return 1+ count

def idf(word, list_of_docs):
	return math.log(len(list_of_docs) /
					float(num_docs_containing(word, list_of_docs)))

def tf_idf(word, doc, list_of_docs):
	return (tf(word, doc) * idf(word, list_of_docs))

def computeTfIdf(jsonFName):

	# tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	stopset = set(stopwords.words('english'))
	stopset |= set(['.', ',', '(', ')', ':', '...', '!', '#', '-', '?', '``', '@', '--'])
	# stopset |= set(['korea', 'seoul', 'festival', 'mgarin-Seoul-South', u'\uac00\ubb3c', u'\uae30\uc5b5\uc774', '.jpg'])
	# stopset |= set(['university', 'seoul', 'park', 'food', 'grand', 'garden'])

	vocabulary = []
	regions = {}
	photoWordList = {}

	for folder in glob.glob(jsonFName + '/*'):
		regions[folder] = {'freq':{}, 'tf':{}, 'idf':{}, 'tf-idf':{}, 'tokens':[]}

		files = [fName
				 for fName in glob.glob(folder + '/*')]
		count = Counter()
		total = 0
		userPhotoCnt = {}
		# stemmer = PorterStemmer()

		final_tokens = []


		for file in files:

			f = open(file, 'r')
			print('>>> ' + file)

			data = json.load(f)
			for photo in data['photo']:

				photoTokens = set()

				# eliminate duplicate user's photos which has more than three
				userId = photo['owner']['path_alias']
				if userId is None:
					userId = photo['owner']['nsid']
				if userPhotoCnt.get(userId) is None:
					userPhotoCnt[userId] = 1
				else:
					if userPhotoCnt[userId] > 3:
						# print('pass ' + userId)
						continue
					else:
						userPhotoCnt[userId] = userPhotoCnt[userId] + 1

				# title
				title = photo['title']['_content']
				title = title.lower()
				# title = title.translate(None, string.punctuation)
				# tokens = tokenizer.tokenize(title)
				tokens = word_tokenize(title)
				# filtered = [strip_punctuation(word) for word in tokens]
				filtered = [w for w in tokens if not w in stopset]
				# stemmed = stem_tokens(filtered, stemmer)
				count.update(filtered)
				final_tokens.extend(filtered)

				photoTokens.update(filtered)

				# tag
				tags = photo['tags']['tag']

				for tag in tags:
					tagToken = tag['_content']
					tokens = word_tokenize(tagToken)
					filtered = [w for w in tokens if not w in stopset]
					count.update(filtered)
					final_tokens.extend(filtered)
					photoTokens.update(filtered)
				total = sum(count.values())

				# Photo words list
				photoId = photo['id']
				photoWordList.update({photoId:photoTokens})

		for token in final_tokens:
			regions[folder]['freq'][token] = freq(token, final_tokens)
			regions[folder]['tf'][token] = tf(token, final_tokens)
			regions[folder]['tokens'] = final_tokens
			# a = regions[folder]['tokens'].count('seoul')

		vocabulary.append(final_tokens)

		# for el in count.most_common(30):
		# 	print el[0], el[1], el[1]/float(total)

		# print(count)

		print(count.most_common(30))

	for folder in regions:
		for token in regions[folder]['tf']:
			regions[folder]['idf'][token] = idf(token, vocabulary)

			regions[folder]['tf-idf'][token] = tf_idf(token, regions[folder]['tokens'], vocabulary)

	topTfIdfwords = {}

	for region in regions:
		words = {}
		for token in regions[region]['tf-idf']:
			if token not in words:
				words[token] = regions[region]['tf-idf'][token]
			else:
				if regions[region]['tf-idf'][token] > words[token]:
					words[token] = regions[region]['tf-idf'][token]

		topWords = []
		i = 0
		print('=============>' + region)
		for item in sorted(words.items(), key=lambda x: x[1], reverse= True):
			topWords.append(item[0])
			print "%f <= %s" % (item[1], item[0])
			i += 1
			if i>10:
				break
		tmp = {region:topWords}
		topTfIdfwords.update(tmp)

	return topTfIdfwords, photoWordList



if __name__ == '__main__':
	print('========================================')
	# jsonFName = 'json_photos_seoul'
	# jsonFName = 'json_photos_gangnamgu_0101'
	# jsonFName = 'json_photos_yuseonggu_0101'
	# jsonFName = 'json_photos_jongnogu_0101'
	jsonFName = 'fdataset'
	computeTfIdf(jsonFName)

