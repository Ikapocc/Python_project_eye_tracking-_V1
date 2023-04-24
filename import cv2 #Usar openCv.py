import cv2 #Usar openCv

cap = cv2.VideoCapture("http://192.168.0.27:8080/video") #toma el video desde un direccion IP
#cap = cv2.VideoCapture("C:/Users/57317/Desktop/eye_recording.flv")#video de prueba

while True:
    ret, frame = cap.read()
    if ret is False:
        break

    roi = frame[300: 700, 750: 1300] #tamaño de la ventana
    filas, columnas, _ = roi.shape #toma puntos en el ojo
    gris_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) #Escala de grises
    gris_roi = cv2.GaussianBlur(gris_roi, (7, 7), 0) #Con blur para mejorar la toma del ojo

    _, thres = cv2.threshold(gris_roi, 3, 255, cv2.THRESH_BINARY_INV)
    contorno, _ = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno = sorted(contorno, key=lambda x: cv2.contourArea(x), reverse=True)

    for x in contorno:
        (x, y, w, h) = cv2.boundingRect(x)

        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2) #forma de rectangulo
        cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), filas), (0, 255, 0), 2) #Linea verde en la posicion de X
        cv2.line(roi, (0, y + int(h/2)), (columnas, y + int(h/2)), (0, 255, 0), 2) #Linea verde en la posicion de Y
        break

    cv2.imshow("Threshold", thres)
    cv2.imshow("roi en gris", gris_roi) #muestra escala de grises en una ventana
    cv2.imshow("Roi", roi) #muestra las lineas y el ojo en otra venta
    key = cv2.waitKey(30) #espera a que la tecla sea oprimida
    if key == "q": #Si esta tecla se oprime se acaba la operacion
        break

cv2.destroyAllWindows() #fin