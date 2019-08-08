import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])

cap.set(1,int(sys.argv[2]))

ret,frame=cap.read()

cv2.imshow("",frame)
cv2.waitKey(0)