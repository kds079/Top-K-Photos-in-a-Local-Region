import json
import urllib
import glob
# def extractSift(input_files):
# 	print "extracting Sift features"
# 	all_features_dict = {}
#
# 	#all_features = zeros([1,128])
# 	for i, fname in enumerate(input_files):
# 		features_fname = fname + '.sift'
# 		if exists(features_fname) == False:
# 			print "calculating sift features for", fname
# 			sift.process_image(fname, features_fname)
# 		locs, descriptors = sift.read_features_from_file(features_fname)
# 		print descriptors.shape
# 		all_features_dict[fname] = descriptors
# 		# if all_features.shape[0] == 1:
# 		# 	all_features = descriptors
# 		# else:
# 		# 	all_features = concatenate((all_features, descriptors), axis = 0)
# 	return all_features_dict

if __name__ == '__main__':
	readFolder = 'photos_kor'
	# files = [fName
	# 		 for fName in glob.glob(readFolder + '/*')]
	files = [readFolder+'/photos1.txt']
	for file in files:
		folderName = 'photo_Seoul/'
		# f = open('dataset/'+'codebook.file', 'r')
		f = open(file, 'r')
		print('>>> ' + file)
		fileId = file[len(readFolder+'/photos'):-4]

		i = 0L
		data = json.load(f)
		for photo in data['photo']:
			location = photo['location']['region']['_content']
			id = photo['id']

			# if location == 'California':
			farmId = photo['farm']
			serverId = photo['server']
			secret = photo['secret']
			url = 'https://farm'+ str(farmId) + '.staticflickr.com/' + str(serverId) + '/' + str(id) + '_' + secret + '.jpg'
			print(url)
			weburl = photo['urls']['url'][0]['_content']
			print( weburl )
			pName = folderName + str(i) + '_' + fileId + '_' + id + '.jpg'
			print(pName)
			urllib.urlretrieve(url, pName )
			i += 1
		break

	# data['photo'].si
	# print(data["photo"][0]["location"]['region']['_content']);



