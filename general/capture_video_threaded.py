from threading import Thread 
from Queue import Queue
import numpy as np 
import cv2
import argparse
import sys
import os
import time

class capture_video(object):
    """docstring for capture_video"""
    def __init__(self, device_no=None, file_name=None, queue_size=128):

        super(capture_video, self).__init__()       
        if device_no!=None and file_name!=None:
            print "[Error]: Multiple sources specified"
            sys.exit()
        if device_no == None:
            if file_name == None:
                print "[Error]: No source specified for the video capture."
                sys.exit()
            else:
                self.file_name = file_name
                if not os.path.exists(self.file_name):
                    print "Error: No such file exists."
                    sys.exit()
                self.initialize_capture(self.file_name)
        else:
            self.device_no = device_no
            self.initialize_capture(self.device_no)
        self.Q = Queue(maxsize=queue_size)
        self.stopped = False

    def initialize_capture(self,source):
        try:
            self.cap = cv2.VideoCapture(source)
            if self.cap is None or not self.cap.isOpened():
                print 'Warning: unable to open video source: ', source
                sys.exit()
        except Exception as e:
            print "Error: ", str(e)
            sys.exit()
        
    def update(self):
        while True:
            if self.stopped:
                break
            if not self.Q.full():
                try:
                    grabbed,frame = self.cap.read()                 
                    if not grabbed:
                        print "[Error]: No frame grabbed."
                        self.stop()
                        os._exit(1)
                    else:
                        self.Q.put(frame)
                except Exception as e:
                    print "Error: ", str(e)
                    os._exit(1)
                    
    def start(self):
        print "[Initializing]: Starting thread for video capture"
        self.stopped = False
        try:
            self.t = Thread(target=self.update, args=())
            self.t.start()
        except Exception as e:
            print "Error: ", str(e)
            sys.exit()
        return

    def read(self):
        return self.Q.get()

    def more(self):
        print self.Q.qsize()
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True
        time.sleep(0.5) 
        self.cap.release()
        cv2.destroyAllWindows() 
        del(self.t)
        print "[Stoped]: Video capture has been stoped."



if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help = True)
    parser.add_argument('--video-device', type=int , action='store', default=None, dest='video_device')
    parser.add_argument('--file', type=str , action='store', default=None, dest='file_name')
    parser.add_argument('--queue-size', type=int , action='store', default=128, dest='queue_size')

    args = parser.parse_args()

    video_capture = capture_video(device_no=args.video_device, file_name=args.file_name, queue_size=args.queue_size)

    video_capture.start()

    while not video_capture.stopped:
    
        frame = video_capture.read()

        cv2.imshow('Capture',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.stop()
            break





