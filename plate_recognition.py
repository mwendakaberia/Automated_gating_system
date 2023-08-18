import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from car_person_recognition import path

#path="C:/Users/MeanRegression/Desktop/dataset/images/Cars27.png"
image=cv2.imread(path)

# plt.imshow(image)
# plt.show()

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur=cv2.bilateralFilter(gray,11,30,90)
edges=cv2.Canny(blur,90,90)

contours,new=cv2.findContours(edges.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
image_copy=image.copy()
_=cv2.drawContours(image_copy,contours,-1,(0,0,255),2)
contours=sorted(contours,key=cv2.contourArea,reverse=True)[:30]
image_copy=image.copy()
_=cv2.drawContours(image_copy,contours,-1,(0,0,255),2)

plate = None
for c in contours:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(c)
        plate = image[y:y + h, x:x + w]
        break

cv2.imwrite("plate.png", plate)

pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
text=pytesseract.image_to_string(plate)
print(text)

image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
image=cv2.putText(image,text,(x-100,y-50),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,0),6,cv2.LINE_AA)

cv2.imshow("final image",image)
cv2.waitKey(0)