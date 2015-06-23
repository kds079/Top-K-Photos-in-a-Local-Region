import flickrapi

api_key = '04f85ab214f51fec3f314dfacac262f0'
api_secret = '313d2166d21addb0'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
# flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# sets = flickr.places.find(query="seoul")
sets = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos",  accuracy=11, place_id = 'MivxyNZQU7lbWxZ_' )

# place_id='nz.gsghTUb4c2WAecA',lat = 37.34, lon=126.58,
#sets = flickr.tags.getHotList(period="day", count=6)
#sets = flickr.photos.geo.photosForLocation(lat=47.6, lon=-122.33, accracy=10)
#sets   = flickr.photosets.getList(user_id='8690161@N08')#sebanado')#73509078@N00')

total_page = sets['photos']['pages']
#print(str(sets))

page = 1

import json
for i in range(total_page):
	photo_fname = "photos_kor/photos" + str(i+1) + ".txt"
	f = open(photo_fname, 'w')
	f.write("{'photo':[")
	sets = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' , page = (i+1))
	photos = sets['photos']['photo']
	print(">>>>>>>>>>>>>>>>>>>>>>>page : " + str(sets['photos']['page']))

	for j in range(len(photos)):
		#print(photos[j]['id'])
		photo = flickr.photos.getInfo(photo_id = photos[j]['id'])
		f.write(str(photo['photo']))
		f.write(",")
		#print(photo)
		print(">>>>>> j : " + str(j))
		break
	f.write("]}");
	f.close()


'''
f = open("photos.txt", 'r')
f1 = open("photos1.txt", 'w')
lines = f.readlines()
for line in lines:
	line1 = line.replace("'", "\"")
	f1.write(line1.replace("None", "\"None\""))
#	f1.write(line)
f.close()
f1.close()
'''


'''
 
import json
parsed = json.loads(sets.decode('utf-8'))

print(parsed)
'''
