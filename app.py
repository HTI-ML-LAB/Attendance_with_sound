#!/usr/bin/env python
from flask import stream_with_context,Flask, render_template, Response,request,redirect , url_for
# emulated camera
import uuid
import threading
import os
from urllib.parse import quote
from camera import Camera
import cv2
from io import BytesIO
import numpy as np
import random
from Process import Processor
app = Flask(__name__)
process= Processor()
threading.Thread(target=process.process_queue).start()

@app.route('/')
def live():
       return render_template("index.html")


def gen(camera):
    global frame,t,process
    """Video streaming generator function."""
    while True:
        try:
         frame = camera.get_frame()
         if(len(process.queue_tem))==0:
            process.add_process(mode="attend",data=[frame])
         x = cv2.imencode('.jpg', frame)[1].tobytes()

         yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')
        except Exception as e:
         print(e)

def gen1():
    while(True):  
        frame=cv2.imread("/home/labubuntu/Desktop/hao/Thread/face/src/res.jpg")
        x = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + x + b'\r\n')
       


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/add',methods=['GET', 'POST'])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        #Get data
	    
        name = request.form.get('name')
        year = request.form.get('year')
        phone = request.form.get('phone')
        try:
            image=request.files['input-image-new']
            bio = BytesIO()
            image.save(bio)
            image=bio.getvalue()
            image=cv2.imdecode(np.frombuffer(image, dtype=np.uint8), 1)
        except:
            image=[]

        if(name!="" and year!="" and phone !="" and image is not None):
        	process.add_process(mode="add",data=[image,name,year,phone])
        print("len : ",len(process.labels))
        print("len temp:" ,len(process.queue_tem))
        return render_template("add.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
