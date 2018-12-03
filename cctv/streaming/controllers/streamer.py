
from flask import Flask, render_template, Response, Blueprint
import cv2 as cv
import camera as cm

mod = Blueprint('streamer', __name__, url_prefix='/streamer')

@mod.route('/stream_cctv')
def stream_cctv():
    return render_template('stream_cctv.html')


def generate_frame():
    cm.Camera.get_instance()
    while True:
        frame = cm.Camera.get_instance().get_frame()
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        jpg_frame = cv.imencode('.jpg', frame)[1].tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpg_frame + b'\r\n')

    cm.Camera.get_instance().release()


@mod.route('/stream_video')
def stream_video():
    return Response(generate_frame(),
            mimetype='multipart/x-mixed-replace; boundary=frame')

