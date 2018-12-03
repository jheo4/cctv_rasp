import cv2 as cv
import camera as cm
import recorder as rc
import threading, os
import object_detector as od
from streaming import app

def init():
  video_path = "./video"
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
    rc.Recorder.get_instance().record_10mins()
    if (cv.waitKey(30) & 0xFF) == 27:
      release()
      break


if __name__ == "__main__":
  threading.Thread(target=run).start()
  app.run(host='0.0.0.0')

