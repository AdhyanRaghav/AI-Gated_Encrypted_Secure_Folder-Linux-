import cv2
import numpy as np

camera=cv2.VideoCapture(0)

print(camera.isOpened())

face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+ "haarcascade_frontalface_default.xml")

sample=[]
label=[]
sample_count=0
target_samples=20

while target_samples>sample_count:
    ret,frame=camera.read()
    print("Reading frame")
    flipped_frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2GRAY)

    faces=face_cascade.detectMultiScale(gray,1.3,5,minSize=(100,100))
    print(len(faces))
    if len(faces)==1:
        for (x, y, w, h) in faces:
            top_left = x, y
            bottom_right = x + w, y + h
            cv2.rectangle(flipped_frame, top_left, bottom_right, (0, 255, 0), 2)
            face_region = gray[y:y + h, x:x + w]  # Inspect later
            resized = cv2.resize(face_region, (200, 200))
            sample.append(resized)
            label.append(0)
            sample_count += 1

            cv2.imshow("Face", resized)

            cv2.waitKey(100)
        cv2.imshow("Window", flipped_frame)
        wait = cv2.waitKey(1)
        print(wait)

        if wait == 113:
            break

camera.release()
cv2.destroyAllWindows()

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.train(sample,np.array(label))
recognizer.save("face_model.yml")
