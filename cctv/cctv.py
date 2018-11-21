import cv2 as cv
import camera as cm
import recorder as rc

def init():
  cm.Camera.get_instance().init()
  width, height = cm.Camera.get_instance().get_video_size()
  rc.Recorder.get_instance().init_format(width, height)

def release():
  cm.Camera.get_instance().release()

def run():
  # Thread per hour -> make background

  '''while True:
    if cv2.waitkey(1) & 0xFF == ord('q'):
      break
    # if object is detected
      # rc.Recorder.get_instance().record_5mins()
 '''
  init()
  rc.Recorder.get_instance().record_5mins()



if __name__ == "__main__":
  run()

