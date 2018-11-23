import cv2 as cv
import time
import camera as cm
import os
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
      self.img_path = './bgimg'
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
    self.auto_save_frame()
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
    self.frame_timer.cancel()
    self.record_timer.cancel()


  def stop_recording(self):
    self.is_recording = False


  def record_10mins(self):
    if self.is_recording is False:
      self.is_recording = True
      self.init_writer()
      self.record_timer = Timer(5, self.stop_recording)
      self.record_timer.start()
      print("Start recording...")
      while self.is_recording:
        if cv.waitKey(1) & 0xFF == ord('q'):
          break
        frame = cm.Camera.get_instance().get_frame()
        self.writer.write(frame)

      print("end recording...")
      self.writer.release()


  def auto_save_frame(self):
    img_dest = os.path.join(self.img_path, "%06d.png" % self.img_index)
    cv.imwrite(img_dest, cm.Camera.get_instance().get_frame())
    self.img_index = (self.img_index + 1) % 1200
    self.frame_timer = Timer(2, self.auto_save_frame)
    self.frame_timer.start()
