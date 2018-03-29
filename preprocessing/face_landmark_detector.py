import cv2
import dlib
import numpy as np 
import argparse
import sys

class landmark_detector:

	def __init__(self,facePredictor):

		if facePredictor == "None":
			print "Error: no shape predictor specified"
			sys.exit()

		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(facePredictor)

	def get_all_face_bounding_boxes(self,image):
		
		assert image is not None
		try:
			return self.detector(image,1)
		except Exception as e:
			print "[Error]: ", str(e)
			return []

	def get_largest_face_bounding_box(self,bounding_boxes):
		
		return max(bounding_boxes, key=lambda rect: rect.width() * rect.height())

	def findLandmarks(self,image,bounding_box):

		try:
			assert image is not None
			assert bounding_box is not None
			points = self.predictor(image,bounding_box)
			return [(p.x,p.y) for p in points.parts()]
		except Exception as e:
			print "[Error]: ", str(e)
			
	def draw_landmarks(self,image,points):

		assert image is not None
		assert points is not None
		for point in points:
			cv2.circle(image, (point[0],point[1]), 2 , (0,0,255), -1)			
		return image


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('--input-image',type=str,action='store',default=None,dest='input_image')
	parser.add_argument('--predictor-dir',type=str,action='store',default=None,dest='predictor_dir')
	args = parser.parse_args()

	detector = landmark_detector(str(args.predictor_dir))

	if args.input_image == None:
		print "Error: No image specified"
		sys.exit() 
	image = cv2.imread(args.input_image)

	boxes = detector.get_all_face_bounding_boxes(image)

	for box in boxes:
		points = detector.findLandmarks(image,box)
		image = detector.draw_landmarks(image,points)


	cv2.imshow('landmarks',image)
	if cv2.waitKey(0) & 0xFF==ord('q'):
		cv2.destroyAllWindows()
	
