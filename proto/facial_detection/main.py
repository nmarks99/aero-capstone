#!/usr/bin/env python3
import cv2
import sys
import time

assert(len(sys.argv) == 2),'No input given. Please input path to image'
img_path = str(sys.argv[1])

t0 = time.time()

# Load the cascade
print('Analyzing image...')
face_cascade = cv2.CascadeClassifier('face_detector.xml')

# Read the image
img = cv2.imread(img_path)

# Detect faces
faces = face_cascade.detectMultiScale(img, 1.1, 4)

# Draw rectangles around faces
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y), (x+w,y+h), (0,0,255), 2)

# Save the result 
cv2.imwrite('out.png',img)
tf = time.time()
elapsed = tf-t0
print('\nDone. Result saved to out.png')
print('Elapsed time = {:.4f} s'.format(elapsed))



