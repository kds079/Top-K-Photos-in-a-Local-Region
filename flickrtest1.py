import flickrapi

api_key = '04f85ab214f51fec3f314dfacac262f0'
api_secret = '313d2166d21addb0'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
#flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

sets = flickr.photos.search(min_taken_date=1430438400, privacy_filter=1, has_geo=1,media="photos", place_id='nz.gsghTUb4c2WAecA' )

print(str(sets))
import json
set = json.load(sets)
print(set['photo'])
str1 = sets.decode('utf-8')

f = open("tmp2.txt", 'w')
f.write(str1)
f.close()
