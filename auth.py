import cv2
import numpy as np
import time
import threading
import subprocess
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
MODEL_PATH=os.path.join(BASE_DIR,"face_model.yml")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

Secret_key = "/home/adhyan/.secret_key"
Mount_Path = "/home/adhyan/SecureMount"
Encrypted_Path = "/home/adhyan/SecureEncrypted"

def is_folder_in_use():
    result=subprocess.run(["lsof","+D",Mount_Path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return len(result.stdout)>0

def inactivity_monitor():
    start=time.time()

    while True:
        time.sleep(10)

        if time.time() - start>120:
            if not is_folder_in_use():
                os.system(f"fusermount -u {Mount_Path}")
                break
            else:
                start=time.time()

camera=cv2.VideoCapture(0)

start_time=time.time()
duration=3

match_count=0
total_predictions=0
threshold=50
confidence_scores=[]

while time.time()-start_time<duration:
    ret,frame=camera.read()
    flip_frame = cv2.flip(frame, 1)

    grey=cv2.cvtColor(flip_frame,cv2.COLOR_BGR2GRAY)

    faces=face_cascade.detectMultiScale(grey,1.3,5,minSize=(100,100))
    if len(faces)==1:
        for(x,y,w,h) in faces:
            top_left=x,y
            bottom_right=x+w,y+h

            face_region=grey[y:y+h,x:x+w]

            cv2.rectangle(flip_frame,top_left,bottom_right,(0,255,0),2)

            cv2.imshow("Win", flip_frame)
            cv2.waitKey(1)
            resized=cv2.resize(face_region,(200,200))

            label,confidence=recognizer.predict(resized)
            print(label,confidence)

            total_predictions+=1
            if confidence<threshold:
                match_count+=1

    #print("Running")
import os

if total_predictions > 0 and (match_count / total_predictions) > 0.6:
    access=True
    os.system('notify-send "ACCESS GRANTED"')

    os.system(f"gocryptfs -passfile {Secret_key} {Encrypted_Path} {Mount_Path}")

    os.system(f"xdg-open {Mount_Path}")

    monitor_thread=threading.Thread(target=inactivity_monitor,daemon=False)
    monitor_thread.start()

else:
    access=False
    os.system('notify-send "ACCESS DENIED"')

camera.release()
cv2.destroyAllWindows()
