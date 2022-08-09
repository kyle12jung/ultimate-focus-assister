import cv2 as cv
import imutils
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import time
import dlib

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
# never expected to be used--will only be using webcam
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())