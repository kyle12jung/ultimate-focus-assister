from re import S
import cv2 as cv
import imutils
from imutils.video import VideoStream
from imutils import face_utils
import datetime
from stopwatch import Stopwatch
from playsound import playsound
import argparse
import time
import dlib
from flask import Flask, render_template, Response

app = Flask(__name__)

FOCUS = True

def gen_frame():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--shape-predictor", required=True,
		help="path to facial landmark predictor")
	# never expected to be used--will only be using webcam
	ap.add_argument("-r", "--picamera", type=int, default=-1,
		help="whether or not the Raspberry Pi camera should be used")
	args = vars(ap.parse_args())

	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor
	print("[INFO] loading facial landmark predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(args["shape_predictor"])

	# initialize the video stream and allow the cammera sensor to warmup
	print("[INFO] camera sensor warming up...")
	vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
	time.sleep(2.0)
	def alarm():
		playsound('assets/alarm.wav')
	#initialize stopwatch
	stopwatch = Stopwatch(2)
	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream, resize it to
		# have a maximum width of 400 pixels, and convert it to
		# grayscale
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		# detect faces in the grayscale frame
		rects = detector(gray, 0)
		if len(rects): stopwatch.reset()
		else: stopwatch.start()
		print(stopwatch.duration)
		if stopwatch.duration > 10.0: 
			alarm()
		# loop over the face detections
		for rect in rects:
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			# loop over the (x, y)-coordinates for the facial landmarks
			# and draw them on the image
			for (x, y) in shape:
				circle = cv.circle(frame, (x, y), 1, (0, 0, 255), -1)

		# # show the frame
		# cv.imshow("Frame", frame)
		# key = cv.waitKey(1) & 0xFF
	
		# # if the `q` key was pressed, break from the loop
		# if key == ord("q"):
		# 	break

		ret, buffer = cv.imencode('.jpg', cv.flip(frame,1))
		frame = buffer.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	# cv.destroyAllWindows()
	# vs.stop()


@app.route('/')
def index():
	return render_template('index.html', data=FOCUS)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
	app.run(debug=True)