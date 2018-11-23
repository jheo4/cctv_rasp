from threading import Timer
import os
import time
import numpy as np
import cv2 as cv
import camera as cm
import recorder as rc


class Object_Detector():
  __instance = None

  @staticmethod
  def get_instance():
    if Object_Detector.__instance is None:
      Object_Detector()
    return Object_Detector.__instance


  def __init__(self):
    if Object_Detector.__instance is not None:
      raise Exception("Singleton Invalidation")
    else:
      print("init object detector...")
      Object_Detector.__instance = self
      self.fgbg = cv.createBackgroundSubtractorMOG2()
      self.object_pixels = 0
      self.background_mog()
      print("finished init obejct detector...")


  def release(self):
    self.mog_timer.cancel()


  def background_mog(self):
    frame = cm.Camera.get_instance().get_frame()
    fgmask = self.fgbg.apply(frame)
    self.object_pixels = np.sum(np.logical_and(fgmask, 1))
    print("diff pixels : %d" % self.object_pixels)
    if self.object_pixels > (160 * 160): # distance adaptive
      print("object detected...")
      img_dest = time.strftime("%H%M%S") + ".png"
      cv.imwrite(img_dest, fgmask)

    self.mog_timer = Timer(0.3, self.background_mog)
    self.mog_timer.start()

