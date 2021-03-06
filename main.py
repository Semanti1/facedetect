from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
import sys
app = Flask(__name__)
faceCascade = cv2.CascadeClassifier(sys.argv[1])
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        #new code
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
		    gray,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags=cv2.CASCADE_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
        for (x, y, w, h) in faces:
		    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.imshow('Video', frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
