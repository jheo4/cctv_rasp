import cv2 as cv
import time
import camera as cm
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
      self.video_path = './videos'
      self.bg_path = './bgimg'
      self.is_recording = False
      self.writer = None
      self.height = None
      self.width = None


  def init_format(self, width, height):
    print("Init recording format...")
    self.fourcc = cv.VideoWriter_fourcc('D', 'I', 'V', 'X')
    self.width = width
    self.height = height
    self.fps = 20
    print("Finished recording init...")


  def init_writer(self):
    print("Init writer...")
    if self.writer is not None:
      print(" Release previous writer")
      self.writer.release()

    if self.width is None and self.height is None:
      raise Exception("No format init")
      sys.exit(0)

    file_name = self.video_path + time.strftime("%Y%m%d%a_%H%M") + '.avi'
    self.writer = cv.VideoWriter(file_name, self.fourcc,
                  self.fps, (self.width, self.height))
    print("Finished writer init...")


  def stopper(self):
    self.is_recording = False


  def record_5mins(self):
    if self.is_recording is False:
      self.is_recording = True
      self.init_writer()

      t = Timer(3, self.stopper)
      t.start()
      print("Start recording...")

      while self.is_recording:
        if cv.waitKey(1) & 0xFF == ord('q'):
          break
        frame = cm.Camera.get_instance().get_frame()
        self.writer.write(frame)

      print("end recording...")
      self.writer.release()
