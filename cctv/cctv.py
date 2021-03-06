import cv2 as cv
import camera as cm
import recorder as rc
import threading, os
import object_detector as od
from streaming import app
from time import sleep

def init():
  video_path = "./video"
  if not os.path.isdir(video_path):
    os.mkdir(video_path)

  image_path = "./capture"
  if not os.path.isdir(image_path):
    os.mkdir(image_path)

  width, height = cm.Camera.get_instance().get_video_size()
  rc.Recorder.get_instance().init_format(width, height)
  od.Object_Detector.get_instance()


def release():
  cm.Camera.get_instance().release()
  rc.Recorder.get_instance().release()
  od.Object_Detector.get_instance().release()


def run():
  init()
  print("warm up...")
  sleep(3)
  print("start to overwatch...")
  while True:
    rc.Recorder.get_instance().record_10mins()


if __name__ == "__main__":
  #threading.Thread(target=run).start()
  #app.run(host='0.0.0.0')
  run()

