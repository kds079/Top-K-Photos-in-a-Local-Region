import sift
import glob
from os.path import exists, splitext
from numpy import zeros, histogram, resize, sqrt, vstack, zeros_like, concatenate, empty, sum, where
import scipy.cluster.vq as vq
from cPickle import dump, HIGHEST_PROTOCOL, load
import pagerank
import tfidf
import json
import sys

PRE_ALLOCATION_BUFFER = 1000  # for sift
EXTENSIONS = [".jpg", ".bmp", ".png", ".pgm", ".tif", ".tiff"]
CODEBOOK_FILE = 'codebook2.file'
K_THRESH = 1  # early stopping threshold for kmeans originally at 1e-5, increased for speedup

def get_imgfiles(path):
	all_files = []
	# files = [fName
	# 		 for fName in glob.glob(path + '/*')
	# 		 if splitext(fName)[-1].lower() in EXTENSIONS]
	files = [fName
			 for folder1 in glob.glob(path + '/*')
			 	for folder in glob.glob(folder1 + '/*')
			 # for folder in glob.glob(path + '/seoul1')
			 		for fName in glob.glob(folder + '/*')
			 		if splitext(fName)[-1].lower() in EXTENSIONS]


	print files
	all_files.extend(files)
	return all_files

def getTagBasedImgFiles(path):
	allFiles = []
	topWordTfIdfScore = {}	# { word : tfidfscore }

	# get topTfIdfwords & photoWordsList
	jsonFName = 'fdataset'
	regionId = ''
	topTfIdfwords, photoWordsList = tfidf.computeTfIdf(jsonFName)
	cmpPath = path[len('photo_'):]
	for key in topTfIdfwords:
		if cmpPath in key:
			regionId = key
			break
	topWordTfIdfScore = topTfIdfwords[regionId]
	print topWordTfIdfScore

	photoTfIdfScore = {}
	# path = 'fphotos/' + path
	#get files contains topwords
	for folder in glob.glob(path + '/*'):
	 	for file in glob.glob(folder + '/*'):
			if splitext(file)[-1].lower() not in EXTENSIONS:
				continue
			# get Photo Id from file name
			photoId = file.split('/')[2].split('_', 1)[1].split('.')[0]
			# photoId = photoId.split('_', 1)[1]
			# photoId = file[-15:-4]
			if photoId in photoWordsList:
				photoWordSet = photoWordsList[photoId]
				wordTfIdfScore = {}
				for word in photoWordSet:
					if word in topWordTfIdfScore:
						if file not in allFiles:
							allFiles.append(file)
						wordTfIdfScore[word] = topWordTfIdfScore[word]

				if len(wordTfIdfScore) > 0:
					photoTfIdfScore[file] = wordTfIdfScore


	return allFiles, photoTfIdfScore

	# 		f = open(file, 'r')
	# 		print('>>> ' + file)
    #
	# 		data = json.load(f)
	# 		for photo in data['photo']:
	# 			photo[]
	#
	#
	# files = [fName
	# 		 for folder in glob.glob(path + '/*')
	# 		 # for folder in glob.glob(path + '/seoul1')
	# 		 	for fName in glob.glob(folder + '/*')
	# 		 	if splitext(fName)[-1].lower() in EXTENSIONS]
    #
    #
	# print files
	# all_files.extend(files)





def extractSift(input_files):
	print "extracting Sift features"
	all_features_dict = {}

	#all_features = zeros([1,128])
	for i, fname in enumerate(input_files):
		features_fname = fname + '.sift'
		if exists(features_fname) == False:
			print "calculating sift features for", fname
			sift.process_image(fname, features_fname)
		locs, descriptors = sift.read_features_from_file(features_fname)
		# print descriptors.shape
		all_features_dict[fname] = descriptors
		# if all_features.shape[0] == 1:
		# 	all_features = descriptors
		# else:
		# 	all_features = concatenate((all_features, descriptors), axis = 0)
	return all_features_dict


def dict2numpy(dict):
	nkeys = len(dict)
	array = zeros((nkeys * PRE_ALLOCATION_BUFFER, 128))
	pivot = 0
	for key in dict.keys():
		value = dict[key]
		nelements = value.shape[0]
		while pivot + nelements > array.shape[0]:
			padding = zeros_like(array)
			array = vstack((array, padding))
		array[pivot:pivot + nelements] = value
		pivot += nelements
	array = resize(array, (pivot, 128))
	return array

def computeHistograms(codebook, descriptors):
    code, dist = vq.vq(descriptors, codebook)
    histogram_of_words, bin_edges = histogram(code,
                                              bins=range(codebook.shape[0] + 1),
                                              normed=False)
    return histogram_of_words


def computeVisualVocabulary(all_features):
	print "---------------------"
	print "## computing the visual words via k-means"

	all_features_array = dict2numpy(all_features)
	print all_features_array.shape

	nfeatures = all_features_array.shape[0]
	nclusters = int(sqrt(nfeatures))
	#whitened = vq.whiten(all_features_array)
	codebook, distortion = vq.kmeans(all_features_array,
									 nclusters,
									 thresh=K_THRESH)

	with open('./dataset/' + CODEBOOK_FILE, 'wb') as f:
		dump(codebook, f, protocol=HIGHEST_PROTOCOL)

	return codebook

def buildMatrix(all_word_histgrams):
	# the count of co-occurrence of visual words between two images
	# idImageFname = {}
	id1 = 0

	imageSize = len(all_word_histgrams)
	matrix = zeros((imageSize, imageSize))

	matrixOrder = []
	for image1 in all_word_histgrams.keys():
		matrixOrder.append(image1)
		# idImageFname[id] = image1
		iHist1 = all_word_histgrams[image1]
		sum1 = sum(iHist1)
		id2 = 0
		for image2 in all_word_histgrams.keys():
			iHist2 = all_word_histgrams[image2]
			sum2 = sum(iHist2)
			if id1 == id2:
				matrix[id1][id2] = 0
			else:
				a = where(iHist1<=iHist2, iHist1, iHist2)
				b = float(sum(iHist1))
				matrix[id1][id2] = sum(where(iHist1<=iHist2, iHist1, iHist2)) /	float(sum(iHist1)+sum(iHist2))
			id2 += 1
		id1 += 1

	# nomarlize # of co-occur of visual word
	# a = matrix[0,:]
	# b = sum(a)
	# c = matrix[0,:] / b
	# matrix[0,:] /= sum(matrix[0,:])

	for i in range(0,imageSize):
		# rowMat = matrix[i,:]
		# sumRow = sum(rowMat)
		# matrix[i,:] /= sumRow
		colMat = matrix[:,i]
		sumCol = sum(colMat)
		matrix[:,i] /= sumCol
		# print sum(matrix[:,i])

	return matrix, matrixOrder

def buildRWVector(matrixOrder, photoTfIdfScore):
	rwVector = []
	for file in matrixOrder:
		tfIdfScore = photoTfIdfScore[file]
		score = float(0)
		for tfIdf in tfIdfScore:
			score += tfIdfScore[tfIdf]
		rwVector.append(score)
	rwVector = [float(i)/sum(rwVector) for i in rwVector]
	print(sum(rwVector))

	return rwVector




if __name__ == '__main__':



	# all_files = get_imgfiles('./dataset/train')
	# all_files = get_imgfiles('fphotos')
	# all_files, photoTfIdfScore = getTagBasedImgFiles('photo_jongnogu_150101')
	# all_files = getTagBasedImgFiles('photo_junggu_0101')
	all_files, photoTfIdfScore = getTagBasedImgFiles('photo_junggu_150101')

	print all_files
	all_features = extractSift(all_files)

	# codebook usase
	# 1. remove comments to use codebook from file
	f = open('dataset/'+CODEBOOK_FILE, 'r')
	fcodebook = load(f)

	# 2. make codebook and use it
	# fcodebook = computeVisualVocabulary(all_features)

	print "---------------------"
	print "## computing histgrams"
	all_word_histgrams = {}
	for imagefname in all_features.keys():
		word_histgram = computeHistograms(fcodebook, all_features[imagefname])
		all_word_histgrams[imagefname] = word_histgram

	print "---------------------"
	print "## build matrix"
	matrix, matrixOrder = buildMatrix(all_word_histgrams)

	# randomWorkVector = [] : consider tfidf score of word in each photo
	randomWorkVector = buildRWVector(matrixOrder, photoTfIdfScore)

	print "---------------------"
	print "## computing pagerank"


    # refer https://gist.github.com/diogojc/1338222/download
	# also refer https://github.com/timothyasp/PageRank
	rank = pagerank.pageRank(matrix, s=.86, rwVector=randomWorkVector)
	rankIndex = rank.argsort()[::-1]
	for i in range(0,30):
		print( str(i) + ": " + str(rank[rankIndex[i]]) + ' - ' + matrixOrder[rankIndex[i]])
		print(photoTfIdfScore[matrixOrder[rankIndex[i]]])
		for title, tfidf in (photoTfIdfScore[matrixOrder[rankIndex[i]]]).iteritems() :
			print( title + ' - ' + str(tfidf))

		# + ' - ' + all_files[rankIndex[i]])
