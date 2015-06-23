import os
import json
import urllib
import glob

if __name__ == '__main__':
	userPhotoCnt = {}

	readFolder = 'json_photos_jongno_0601'
	# readFolder = 'photos_kor'
	files = [fName
			 for fName in glob.glob(readFolder + '/*')]
	# files = [readFolder+'/photos1.txt']

	# fileIndex = 1
	writeFolderName = 'photo_jongno_0601/seoul'

	for file in files:

		# f = open('dataset/'+'codebook.file', 'r')
		f = open(file, 'r')
		print('>>> ' + file)
		fileId = file[len(readFolder+'/photos'):-4]


		i = 0L
		data = json.load(f)
		for photo in data['photo']:
			location = photo['location']['region']['_content']
			id = photo['id']

			# eliminate duplicate user's photos which has more than three
			userId = photo['owner']['path_alias']
			if userId is None:
				userId = photo['owner']['nsid']
			if userPhotoCnt.get(userId) is None:
				userPhotoCnt[userId] = 1
			else:
				if userPhotoCnt[userId] > 3:
					print('pass ' + userId)
					i += 1
					continue
				else:
					userPhotoCnt[userId] = userPhotoCnt[userId] + 1

			# if location == 'California':
			farmId = photo['farm']
			serverId = photo['server']
			secret = photo['secret']
			url = 'https://farm'+ str(farmId) + '.staticflickr.com/' + str(serverId) + '/' + str(id) + '_' + secret + '.jpg'
			print(url)
			weburl = photo['urls']['url'][0]['_content']
			print( weburl )
			wFolder = writeFolderName + fileId
			pName = wFolder + '/' + str(i) + '_' + fileId + '_' + id + '.jpg'
			print(pName)
			if not os.path.exists(os.path.dirname(pName)):
				os.makedirs(os.path.dirname(pName))
			urllib.urlretrieve(url, pName )
			i += 1

		# fileIndex += 1

	# data['photo'].si
	# print(data["photo"][0]["location"]['region']['_content']);



