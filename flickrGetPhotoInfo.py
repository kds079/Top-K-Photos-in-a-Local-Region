import flickrapi
import json
import os
import urllib
import glob

def getPhotoJson(jsonFileName):
	api_key = '04f85ab214f51fec3f314dfacac262f0'
	api_secret = '313d2166d21addb0'

	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
	#flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

	# sets = flickr.places.find(query="kaist")

	# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' )
	# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos",  accuracy=11, place_id = 'MivxyNZQU7lbWxZ_' )
	# raw_photos = flickr.photos.search(text = 'coex', min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11)#, place_id = 'cLDVUC9TWribwZR3JQ')
	# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Flh3hrJTWriST0HwPg')
	# raw_photos = flickr.photos.search(min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Flh3hrJTWriST0HwPg')
	# raw_photos = flickr.photos.search(min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'P6trs9NTWrjlJ6MVrA')
	raw_photos = flickr.photos.search(min_taken_date=1388534400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Ez3nlixTWrgxk5hPQw')

	#print(raw_photos.decode('utf-8'))
	photos = json.loads(raw_photos.decode('utf-8'))
	total_page = photos['photos']['pages']

	page = 1

	for i in range(total_page):
		photo_fname = jsonFileName + '/photos' + str(i+1) + ".txt"
		if not os.path.exists(os.path.dirname(photo_fname)):
					os.makedirs(os.path.dirname(photo_fname))
		f = open(photo_fname, 'w')
		f.write("{\"photo\":[")
		# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' , page = (i+1))
		# seoul
		#raw_photos = flickr.photos.search(min_taken_date=1433116800, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'MivxyNZQU7lbWxZ_' , page = (i+1))
		# jongno gu
		# raw_photos = flickr.photos.search(min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'cLDVUC9TWribwZR3JQ' , page = (i+1))
		# jung gu
		# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Flh3hrJTWriST0HwPg', page = (i+1))
		# raw_photos = flickr.photos.search(min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Flh3hrJTWriST0HwPg', page = (i+1))
		# Gangnam gu
		# raw_photos = flickr.photos.search(min_taken_date=1420070400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'P6trs9NTWrjlJ6MVrA', page = (i+1))
		#'place_id': u'Ez3nlixTWrgxk5hPQw', u'_content': u'Yuseong-Gu'}
		raw_photos = flickr.photos.search(min_taken_date=1388534400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'Ez3nlixTWrgxk5hPQw', page = (i+1))

		photos1 = json.loads(raw_photos.decode('utf-8'))
		photos = photos1['photos']['photo']
		print(">>>>>>>>>>>>>>>>>>>>>>>page : " + str(photos1['photos']['page']))

		for j in range(len(photos)):
			#print(photos[j]['id'])
			raw_photo = flickr.photos.getInfo(photo_id = photos[j]['id'])
			photo = json.loads(raw_photo.decode('utf-8'))
			f.write(json.dumps(photo['photo']))
			if j != (len(photos)-1):
				f.write(",")
			#print(photo)
			print(">>>>>> j : " + str(j))

		f.write("]}");
		f.close()

def getPhoto(jsonFName, photoFolder):
	userPhotoCnt = {}

	readFolder = jsonFName #'json_photos_jongno_0601'
	# readFolder = 'photos_kor'
	files = [fName
			 for fName in glob.glob(readFolder + '/*')]
	# files = [readFolder+'/photos1.txt']

	# fileIndex = 1
	writeFolderName = photoFolder + '/seoul'

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

if __name__ == '__main__':

	# jsonFName = 'json_photos_jongno_0515'
	# jsonFName = 'json_photos_test_0101'
	jsonFName = 'json_photos_yuseonggu_0101'
	getPhotoJson(jsonFName)

	# photoFolder = 'photo_jongno_0515'
	# photoFolder = 'photo_test_0101'
	photoFolder = 'photo_yuseonggu_0101'
	getPhoto(jsonFName, photoFolder)

