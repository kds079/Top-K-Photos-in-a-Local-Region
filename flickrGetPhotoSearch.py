import flickrapi
import json
import os

api_key = '04f85ab214f51fec3f314dfacac262f0'
api_secret = '313d2166d21addb0'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
#flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' )
# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos",  accuracy=11, place_id = 'MivxyNZQU7lbWxZ_' )
raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'cLDVUC9TWribwZR3JQ')

#print(raw_photos.decode('utf-8'))
photos = json.loads(raw_photos.decode('utf-8'))
total_page = photos['photos']['pages']

page = 1

for i in range(total_page):
	photo_fname = "json_photos_jongno_0515/photos" + str(i+1) + ".txt"
	if not os.path.exists(os.path.dirname(photo_fname)):
				os.makedirs(os.path.dirname(photo_fname))
	f = open(photo_fname, 'w')
	f.write("{\"photo\":[")
	# raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' , page = (i+1))
	# seoul
	#raw_photos = flickr.photos.search(min_taken_date=1433116800, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'MivxyNZQU7lbWxZ_' , page = (i+1))
	# jongno gu
	raw_photos = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", accuracy=11, place_id = 'cLDVUC9TWribwZR3JQ' , page = (i+1))
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

