import cv2 as cv
import numpy as np

cam  = cv.VideoCapture(0)

while True:
    ret, frame = cam.read() #retorna un bool y un frame(h,w,3)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    BluredGray = cv.blur(gray,(3,3))

    #cv.imshow("Camara", BluredGray)

    circles = cv.HoughCircles(BluredGray, cv.HOUGH_GRADIENT, dp=1.2, minDist=50,
                              param1=50, param2=30, minRadius=10, maxRadius=400) #minradius y maradius son los radios minimo y maximo de los circulos
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        for i in circles[0,:]:
            x,y,r = i[0],i[1],i[2]
            cv.circle(frame,(x,y),r,(0,255,0),2)
            cv.circle(frame,(x,y),1,(0,0,255),3)
            
            cv.imshow("camara", frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv.destroyAllWindows()

