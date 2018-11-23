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
      self.bg_file = "./bg/background.png"
      self.img_path = "./bgimg"
      self.detect_object()
      self.background_timer = Timer(100, self.get_background)
      self.background_timer.start()
      print("finished init obejct detector...")

  def release(self):
    self.background_timer.cancel()
    self.detection_timer.cancel()


  def detect_object(self):
    threshold = 50  # adjust...
    if os.path.isfile(self.bg_file)\
        and not rc.Recorder.get_instance().is_recording:
      bg_img = cv.cvtColor(cv.imread(self.bg_file),
                              cv.COLOR_BGR2GRAY).astype(np.float64)

      camera_frame = cm.Camera.get_instance().get_frame()
      gray_frame = cv.cvtColor(camera_frame,
                                 cv.COLOR_BGR2GRAY).astype(np.float64)

      diff = np.abs(gray_frame - bg_img).astype(np.float64)

      diff_gaussian = cv.getGaussianKernel(19, 2) #adjust
      diff = cv.filter2D(diff, -1, diff_gaussian)

      over_threshold = np.where(diff > threshold, 1.0, 0.0)

      object_pixels = np.sum(over_threshold.astype(np.uint8))
      print("diff pixels : %d" % int(object_pixels))
      if object_pixels > (160 * 160): # distance adaptive
        # Test
        diff_mask = np.multiply(gray_frame, over_threshold)
        diff_mask_bin = np.where(diff_mask > 0, 255.0, 0.0)

        print("object detected...")
        img_dest = time.strftime("%H%M%S") + ".png"
        cv.imwrite(img_dest, diff_mask_bin.astype(np.uint8))

        rc.Recorder.get_instance().record_10mins()

    self.detection_timer = Timer(1, self.detect_object)
    self.detection_timer.start()


  def get_background(self):
    alpha = 0.005
    imgs = [img for img in sorted(os.listdir(self.img_path))
              if img.endswith(".png")]
    cur_frame = cv.cvtColor(cv.imread(os.path.join(self.img_path, imgs[0])),
                  cv.COLOR_BGR2GRAY).astype(np.float64)
    back_frame = cur_frame

    for img_index in range(len(imgs)):
      back_frame = ((1 - alpha) * back_frame).astype(np.float64)\
                      + (alpha * cur_frame).astype(np.float64)
      cur_frame = cv.cvtColor(cv.imread(os.path.join(self.img_path,
                    imgs[img_index])), cv.COLOR_BGR2GRAY).astype(np.float64)

    result_img = back_frame.astype(np.uint8)
    cv.imwrite(self.bg_file, result_img)

    self.background_timer = Timer(100, self.get_background)
    self.background_timer.start()

