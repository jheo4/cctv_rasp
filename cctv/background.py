import numpy as np
import cv2 as cv
import os
from threading import Timer


def get_background(alpha):
  img_path = "./bgimg"
  result_path = "./bg"

  imgs = [img for img in sorted(os.listdir(img_path)) if img.endswith(".png")]
  cur_frame = cv.cvtColor(cv.imread(os.path.join(img_path, imgs[0])),
                          cv.COLOR_BGR2GRAY).astype(np.float64)
  back_frame = cur_frame

  for img_index in range(len(imgs)):
    back_frame = ((1 - alpha) * back_frame).astype(np.float64)\
                  + (alpha * cur_frame).astype(np.float64)
    cur_frame = cv.cvtColor(cv.imread(os.path.join(img_path, imgs[img_index])),
                            cv.COLOR_BGR2GRAY).astype(np.float64)

  result_img = back_frame.astype(np.uint8)
  cv.imwrite(os.path.join(result_path, "background.png"), result_img)


