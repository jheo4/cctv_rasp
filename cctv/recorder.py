import cv2 as cv
import camera as cm
import os, re, time
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
      self.is_recording = False
      self.is_preparing_to_stop = False
      self.writer = None
      self.height = None
      self.width = None
      self.video_path = './video'
      if os.path.isfile('./video_index.txt'):
        f = open('video_index.txt', 'r')
        next_index = f.read()
        self.video_index = int(next_index)
        f.close()
      else:
        self.video_index = 0


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

    index_string = "%03d_" % self.video_index
    for f in os.listdir(self.video_path):
      if re.match(index_string, f):
        os.remove(os.path.join(self.video_path, f))

    file_name = '%03d_' % self.video_index + \
        time.strftime("%Y %m %d(%a)_%H:%M") + '.avi'
    file_dest = os.path.join(self.video_path, file_name)
    self.writer = cv.VideoWriter(file_dest, self.fourcc,
                    self.fps, (self.width, self.height))
    self.save_video_index()
    print("Finished writer init...")


  def release(self):
    self.record_timer.cancel()


  def prepare_to_stop(self):
    self.is_preparing_to_stop = True
    print("prepare_to_stop")
    Timer(15, self.stop_recording).start()

  def stop_recording(self):
    print("stop_recording")
    self.is_recording = False
    self.is_preparing_to_stop = False


  def record_10mins(self):
    object_pixels = od.Object_Detector.get_instance().object_pixels

    if self.is_recording is False and object_pixels > 3500:
      self.is_recording = True
      self.init_writer()
      self.record_timer = Timer(500, self.prepare_to_stop)
      self.record_timer.start()
      print("Start recording...")

      while self.is_recording:
        frame = cm.Camera.get_instance().get_frame()
        self.writer.write(frame)

      print("end recording...")
      self.writer.release()


  def save_video_index(self):
    f = open("video_index.txt", 'w')
    self.video_index = (self.video_index + 1) % 500 # depending on disk capa
    index_data = "%d\n" % self.video_index
    f.write(index_data)
    f.close()

