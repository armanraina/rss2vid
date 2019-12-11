import os
from util import createVideo, createVideoStream
from google.cloud import storage

BASE_DIR = '/media/arman/Data1/CITR/'

names = os.listdir('/media/arman/Data1/CITR')

createVideo(BASE_DIR+names[0], BASE_DIR + names[2], BASE_DIR +'out.mkv', 'good')

