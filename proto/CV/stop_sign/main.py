#!/usr/bin/env python3
import cv2
import sys
import time
import os

assert(len(sys.argv) == 2),'No input given. Please input path to image'
img_path = str(sys.argv[1])

t0 = time.time()

# Load the cascade
print('Analyzing image...')
cascade = cv2.CascadeClassifier('stop_data.xml')

# Read the image
img = cv2.imread(img_path)

# Detect desired image 
detected = cascade.detectMultiScale(img, 1.1, 4)

# Draw rectangles around faces
for (x,y,w,h) in detected:
    cv2.rectangle(img,(x,y), (x+w,y+h), (255,0,0), 5)

tf = time.time()
elapsed = tf-t0

# Save the result
cv2.imwrite('./out.png',img)
print('\nDone. Result saved to out.png')
print('Elapsed time = {:.4f} s'.format(elapsed))

os.system('xdg-open ./out.png 2>/dev/null')
