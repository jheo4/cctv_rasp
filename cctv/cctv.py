import cv2 as cv
import camera as cm
import recorder as rc
import background as bg
import threading
import object_detector as od
import os
import shutil

backgournd_timer = threading.Timer(1800, bg.get_background, [0.005])

def init():
  bg_path = "./bg"
  img_path = "./bgimg"
  video_path = "./video"
  if os.path.isdir(bg_path):
    shutil.rmtree(bg_path)
  if os.path.isdir(img_path):
    shutil.rmtree(img_path)

  os.mkdir(bg_path)
  os.mkdir(img_path)

  if not os.path.isdir(video_path):
    os.mkdir(video_path)

  width, height = cm.Camera.get_instance().get_video_size()
  rc.Recorder.get_instance().init_format(width, height)
  od.Object_Detector.get_instance()


def release():
  cm.Camera.get_instance().release()
  rc.Recorder.get_instance().release()
  od.Object_Detector.get_instance().release()


def run():
  init()
  while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
      release()
      break


if __name__ == "__main__":
  run()

