import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

img = cv.imread("IMG_1200.jpg")
 
def  resizeIMG(frame, scaleFactor=0.5):
    width = int(frame.shape[1] * scaleFactor)
    height = int(frame.shape[0] * scaleFactor)
    return cv.resize(frame, (width, height))

resized_img = resizeIMG(img,0.2)
cv.imshow('original',resized_img)

gray_img = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)

blur = cv.GaussianBlur(gray_img, (5,5), 0)

_,th1= cv.threshold(blur, 60, 255, cv.THRESH_BINARY)
#th1 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)


cv.imshow('threshold',th1)
cv.imshow('gray',gray_img)
cv.imshow("original",resized_img)   

# Apply Canny edge detection
edges = cv.Canny(th1, 80, 100)

kernel = np.ones((3,3), np.uint8)
edges_clean = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)
edges_clean = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel)

cv.imshow('edges', edges)

cv.waitKey(0)
cv.destroyAllWindows()