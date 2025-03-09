import cv2 as cv
import numpy as np
import Astar as astar
from matplotlib import pyplot as plt

def resizeIMG(frame, scaleFactor=0.5):
    width = int(frame.shape[1] * scaleFactor)
    height = int(frame.shape[0] * scaleFactor)
    return cv.resize(frame, (width, height))

def IdentifyContours(frame):
    # Cargar imagen
    img = frame

    # Verificar si la imagen se cargó correctamente
    if img is None:
        print(f"Error: No se pudo cargar la imagen en {frame}.")
        return None, None, None, None, None, None

    # Convertir a escala de grises
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(grayImg, (5,5), 0)

    # Detección de círculos
    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, dp=1.2, minDist=50,
                              param1=50, param2=30, minRadius=10, maxRadius=40)

    # Dibujar los círculos detectados
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 3)  # Contorno
            cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)  # Centro

    # Aplicar umbralización adaptativa
    th = cv.adaptiveThreshold(grayImg, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv.THRESH_BINARY_INV, 11, 2)
    
    # Detectar bordes con Canny
    kernel = np.ones((6,6), np.uint8)
    canny = cv.Canny(th, 125, 175)
    #canny = cv.dilate(canny, kernel, iterations=1) 
    
    # Encontrar los contornos
    contours, _ = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    return canny, blur, grayImg, img, circles, th, contours

# Llamar a la función con la imagen correcta

def FindCoordinates(img, contours):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Verificar que la imagen se procesó correctamente
    if img is not None:
    # Dibujar contornos en la imagen
        cv.drawContours(img, contours, -1, (32, 75, 216), 2)  # Azul para los contornos
    
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)


# Variables para el inicio (negro) y final (amarillo)
        start = None  # Figura negra
        end = None  # Figura amarilla

# Filtrar figuras por color
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])  # Limite más alto en V

        mask_black = cv.inRange(hsv, lower_black, upper_black)  # Máscara de negro
        contours_black, _ = cv.findContours(mask_black, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours_black:
            largest_black = max(contours_black, key=cv.contourArea)
            x, y, w, h = cv.boundingRect(largest_black)
            start = (x + w//2, y + h//2)
            cv.circle(img, start, 7, (0, 255, 0), -1)  # Punto verde para inicio

    # **Nueva forma de detectar amarillo**
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        mask_yellow = cv.inRange(hsv, lower_yellow, upper_yellow)  # Máscara de amarillo
        contours_yellow, _ = cv.findContours(mask_yellow, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #cv.imshow("yellowMask",mask_yellow)

        if contours_yellow:
            largest_yellow = max(contours_yellow, key=cv.contourArea)
            x, y, w, h = cv.boundingRect(largest_yellow)
            end = (x + w//2, y + h//2)
            #cv.circle(img, end, 7, (0, 0, 255), -1)
        
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([130,255,255])

        mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
        #cv.imshow("mask_blue", mask_blue)
        contours_blue, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours_blue:
            largest_blue = max(contours_blue, key=cv.contourArea)
            x, y, w, h = cv.boundingRect(largest_blue)
            obstacle = (x + w//2, y + h//2)
            cv.circle(img, obstacle, 7, (0, 0, 255), -1)
    

    return(start,end,mask_black,mask_yellow,mask_blue,obstacle)


def getCarAngle(img, mask_black):
    # Encontrar contornos en la máscara de negro
    contours_black, _ = cv.findContours(mask_black, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours_black:
        # Tomar el contorno más grande (asumiendo que es el carro)
        largest_black = max(contours_black, key=cv.contourArea)

        # Obtener el rectángulo mínimo que encierra el carro
        rect = cv.minAreaRect(largest_black)

        # Extraer el ángulo de rotación
        angle = rect[2]  

        # Ajuste de ángulo
        if angle < -45:
            angle += 90  # Para asegurar que el ángulo esté en un rango correcto
        
        box = cv.boxPoints(rect)
        box = np.array(box, dtype=np.int32)

        cv.drawContours(img, [box], 0, (0, 255, 255), 2)  # Dibujar en amarillo

        # Mostrar el ángulo en la imagen
        center = (int(rect[0][0]), int(rect[0][1]))
        cv.putText(img, f"{angle:.2f} deg", center, cv.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2, cv.LINE_AA)


        return rect[2]

def ScaleFactorFunc(circles,realdistance):
    center = [(int(i[0]), int(i[1])) for i in circles[0, :]] if circles is not None else []

    if len(center) >= 2:
        x1, y1 = center[0]
        x2, y2 = center[1]

        pixelDistance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        scaleFactor = realdistance / pixelDistance

    return scaleFactor

def RouteToMeters(path,scaleFactor,imgHeight):

    convertedPath = [(x*scaleFactor, (imgHeight-y)*scaleFactor) for x, y in path]

    return convertedPath

def PathProcessing(mask):
    # Aplicar operaciones morfológicas
    kernel = np.ones((21,80), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=1)
    return mask




if __name__ == "__main__":

    image= "TestCarroVlv.jpg"
    image = cv.imread(image)
    canny, blur, grayImg, img, circles, th, contours = IdentifyContours(image)
    start,end,maskBlack,maskYellow,maskblue,obstacle = FindCoordinates(img, contours)
    angle = getCarAngle(img,maskBlack)
    imgHeight = img.shape[0]

    start = (start[1],start[0])
    end = (end[1],end[0])

    getted = ScaleFactorFunc(circles,0.1)
    maze = PathProcessing(maskblue)


    path,maze = astar.adastra(maze, start, end)
    print(len(path))


    for i in range(len(path) - 1):
        cv.line(img, (path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]), (0, 0, 255), 2)  #

    cv.imshow("Maze",img)



    cv.waitKey(0)
    cv.destroyAllWindows()
