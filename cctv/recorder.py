import cv2 as cv
import time
import camera as cm
import os
import object_detector as od
from threading import Timer

class Recorder():
  __instance = None

  @staticmethod
  def get_instance():
    if Recorder.__instance is None:
      Recorder()
    return Recorder.__instance


  def __init__(self):
    if Recorder.__instance is not None:
      raise Exception("Singleton violation")
    else:
      Recorder.__instance = self
      self.video_path = './video'
      self.img_index = 0
      self.is_recording = False
      self.writer = None
      self.height = None
      self.width = None


  def init_format(self, width, height):
    print("Init recording format...")
    self.fourcc = cv.VideoWriter_fourcc('D', 'I', 'V', 'X')
    self.width = width
    self.height = height
    self.fps = 15
    print("Finished recording init...")


  def init_writer(self):
    print("Init writer...")
    if self.writer is not None:
      print(" Release previous writer")
      self.writer.release()

    if self.width is None and self.height is None:
      raise Exception("No format init")
      sys.exit(0)

    file_name = time.strftime("%Y%m%d%a_%H%M") + '.avi'
    file_dest = os.path.join(self.video_path, file_name)
    self.writer = cv.VideoWriter(file_dest, self.fourcc,
                  self.fps, (self.width, self.height))
    print("Finished writer init...")


  def release(self):
    self.record_timer.cancel()


  def stop_recording(self):
    self.is_recording = False


  def record_10mins(self):
    object_pixels = od.Object_Detector.get_instance().object_pixels
    if self.is_recording is False and object_pixels > 25600:
      self.is_recording = True
      self.init_writer()
      self.record_timer = Timer(5, self.stop_recording)
      self.record_timer.start()
      print("Start recording...")
      while self.is_recording:
        if cv.waitKey(30) & 0xFF == 27:
          break
        frame = cm.Camera.get_instance().get_frame()
        self.writer.write(frame)

      print("end recording...")
      self.writer.release()

