import cv2 as cv
import numpy as np
import preProcessing as PP  # Módulo de preprocesamiento de imágenes
import Astar as A  # Algoritmo de pathfinding A*
import ClientePC as CP  # Comunicación con ESP32
import threading
import time as t
import queue as q 

# 🔹 Inicializar la cámara
cam = cv.VideoCapture(0)
ip = ""  # IP del ESP32

frameQueue= q.Queue(maxsize=1)
pathQueue = q.Queue(maxsize=1)
dataQueue = q.Queue(maxsize=1)

isPathCalculated = False
isRunning = True

def GetImageThread():
    global isRunning
    while isRunning:
        ret,frame = cam.read()
        cv.imshow('camara', frame)
        if ret: 
            if not frameQueue.full():
                 frameQueue.put(frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            isRunning = False
            print(isRunning)
            
        t.sleep(0.005)

def ProcessingThread():
    
    global isPathCalculated
    
    while isRunning:
        if frameQueue.empty():
            continue
        
        frame= frameQueue.get()
        #cv.imshow('camara', frame)
        
        canny, blur, grayImg, img, circles, th, contours = PP.IdentifyContours(frame)

        # Extraer puntos clave
        start, end, maskBlack, maskYellow, maskblue, obstacle = PP.FindCoordinates(img, contours)
        angle = PP.getCarAngle(img, maskBlack)
         
        #Calcular el factor de escalamiento
        scaleFact = PP.ScaleFactorFunc(circles, 0.1)
        
        
        if not isPathCalculated and start and end:
            startA = (start[1], start[0])
            endA = (end[1], end[0])
            
            maze = PP.PathProcessing(maskblue)  
            
            path,b = A.adastra(maze,startA,endA)
            
            if path and len(path) != 0:
                path = PP.RouteToMeters(path, scaleFact, img.shape[0])
                pathQueue.put(path)
                isPathCalculated = True
        else:
            print("No hay camino")
        
        if not dataQueue.full():
            dataQueue.put((angle,obstacle,start,end))
            
        if not pathQueue.empty():
            path = pathQueue.queue[0]
        
        t.sleep(0.1)

def sendThread():
    
    while isRunning:
        if not pathQueue.empty():
            path = pathQueue.get()
            CP.sendCoorPacks(path, ip)
        
        if not dataQueue.empty():
            angle,obstacle,start,end = dataQueue.get()
            
            if obstacle and len(obstacle) !=0:
                CP.sendCoordinates(obstacle[0], obstacle[1], ip, "obstacle")
            
            if start and end:
                CP.sendCoordinates(start[0], start[1], ip, "start")
                CP.sendCoordinates(end[0], end[1], ip, "start")
                
    time.sleep(0.5)
                
                
t1 = threading.Thread(target=GetImageThread,daemon=True)
t2 = threading.Thread(target=ProcessingThread,daemon=True)        
t3 = threading.Thread(target=sendThread,daemon=True)        

t1.start()
t2.start()
#t3.start()

t1.join()
t2.join()
#t3.join()


cam.release()
cv.destroyAllWindows()

            
            
        
                

