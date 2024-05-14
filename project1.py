!pip install -q opencv-python
# Libraries for working with image processing
import numpy as np
import pandas as pd
import cv2
from google.colab.patches import cv2_imshow
# Libraries needed to edit/save/watch video clips
from moviepy import editor
import moviepy
def process_video(test_video, output_video):
	"""
	Read input video stream and produce a video file with detected lane lines.
	Parameters:
		test_video: location of input video file
		output_video: location where output video file is to be saved
	"""
	# read the video file using VideoFileClip without audio
	input_video = editor.VideoFileClip(test_video, audio=False)
	# apply the function "frame_processor" to each frame of the video
	# will give more detail about "frame_processor" in further steps
	# "processed" stores the output video
	processed = input_video.fl_image(frame_processor)
	# save the output video stream to an mp4 file
	processed.write_videofile(output_video, audio=False)
def frame_processor(image):
	"""
	Process the input frame to detect lane lines.
	Parameters:
		image: image of a road where one wants to detect lane lines
		(we will be passing frames of video to this function)
	"""
	# convert the RGB image to Gray scale
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# applying gaussian Blur which removes noise from the image 
	# and focuses on our region of interest
	# size of gaussian kernel
	kernel_size = 5
	# Applying gaussian blur to remove noise from the frames
	blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
	# first threshold for the hysteresis procedure
	low_t = 50
	# second threshold for the hysteresis procedure 
	high_t = 150
	# applying canny edge detection and save edges in a variable
	edges = cv2.Canny(blur, low_t, high_t)
	# since we are getting too many edges from our image, we apply 
	# a mask polygon to only focus on the road
	# Will explain Region selection in detail in further steps
	region = region_selection(edges)
	# Applying hough transform to get straight lines from our image 
	# and find the lane lines
	# Will explain Hough Transform in detail in further steps
	hough = hough_transform(region)
	#lastly we draw the lines on our resulting frame and return it as output 
	result = draw_lane_lines(image, lane_lines(image, hough))
	return result