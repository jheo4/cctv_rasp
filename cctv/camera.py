import cv2 as cv
import sys

class Camera():
  __instance = None

  @staticmethod
  def get_instance():
    if Camera.__instance is None:
      Camera()
    return Camera.__instance


  def __init__(self):
    if Camera.__instance is not None:
      raise Exception("Singleton Violation")
    else:
      Camera.__instance = self


  def init(self):
    print("Init camera device...")
    self.device = cv.VideoCapture(0)
    if self.device.isOpened is False:
      raise Exception("Camera device error")
      sys.exit(0)

    self.width = 640
    self.height = 480
    self.device.set(3, self.width)
    self.device.set(4, self.height)
    print(" width: %d, height: %d" % (self.width, self.height))
    print("Finished camera init...")


  def release(self):
    print("Release camera device...")
    self.device.release()
    print("Finish releasing camera device...")


  def get_video_size(self):
    return self.width, self.height


  def get_frame(self):
    ret, frame = self.device.read()
    if not ret:
      raise Exception("Camera read error")
      sys.exit(0)
    return frame
