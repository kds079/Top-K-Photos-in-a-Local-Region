from vlfeat import *

process_image('../dataset/airplane/a25-2.JPG','tmp.sift')
l,d = read_features_from_file('tmp.sift')
