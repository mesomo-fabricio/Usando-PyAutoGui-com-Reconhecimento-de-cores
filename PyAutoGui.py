

import cv2 as cv
import numpy as np
import pyautogui as pa
pa.FAILSAFE = False

camera = cv.VideoCapture(0) #Captura a Imagem da Câmera de índice 1


def mudouValor(x):
    pass




while True:
    xtela, ytela = pa.size() #captura o tamanho da tela em pixels
    
    
    _, frame = camera.read() #destina a imagem para a variável frame
    altura, largura, bpp = np.shape(frame) #captura a resolução da câmera
    
    frameEspelhado = cv.flip(frame, 1) #inverte a imagem da câmera para o lado correto
    frameHsv = cv.cvtColor(frameEspelhado, cv.COLOR_BGR2HSV) #Converte o frame de BGR para HSV

    #Setando as cores utilizadas
    lowerColorLaranja = np.array([0, 136, 36]) 
    lowerColorVerde = np.array([43, 73, 114])
    lowerColorRoxo = np.array([106,157,36])
    uppperColor = np.array([179, 255, 255])

    #Definindo as mascaras
    mascaraLaranja = cv.inRange(frameHsv, lowerColorLaranja, uppperColor)
    resultadoLaranja = cv.bitwise_and(frameEspelhado, frameEspelhado, mask=mascaraLaranja)
    
    mascaraRoxo = cv.inRange(frameHsv, lowerColorRoxo, uppperColor)
    resultadoRoxo = cv.bitwise_and(frameEspelhado, frameEspelhado, mask=mascaraRoxo)

    mascaraVerde = cv.inRange(frameHsv, lowerColorVerde, uppperColor)
    resultadoVerde = cv.bitwise_and(frameEspelhado, frameEspelhado, mask=mascaraVerde)

    #Definindo Bordas
    _, bordaLaranja = cv.threshold(cv.cvtColor(
        resultadoLaranja, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    _, bordaRoxo = cv.threshold(cv.cvtColor(
        resultadoRoxo, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    _, bordaVerde = cv.threshold(cv.cvtColor(
        resultadoVerde, cv.COLOR_BGR2GRAY), 3, 255, cv.THRESH_BINARY)

    #Definindo Contornos
    contornosLaranja, _ = cv.findContours(
        bordaLaranja, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    contornosRoxo, _ = cv.findContours(
        bordaRoxo, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    contornosVerde, _ = cv.findContours(
        bordaVerde, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for contornoLaranja in contornosLaranja:
        areaLaranja = cv.contourArea(contornoLaranja)
        xLaranja, yLaranja, wLaranja, hLaranja = cv.boundingRect(contornoLaranja)
        if areaLaranja > 500: #Quando a Àrea laranja encontrada for maior do que a limiar o mouse vai mexer conforme o objeto estiver sendo capturado na câmera
            cv.rectangle(frameEspelhado, (xLaranja, yLaranja), (xLaranja+wLaranja, yLaranja+hLaranja), (255, 255, 255), 4) 
          
            movx = int((xLaranja*xtela)/largura)
            movy = int((yLaranja*ytela)/altura)
            pa.moveTo(movx, movy)
            #print(movx, movy, wLaranja, hLaranja,xLaranja,yLaranja)
            
        
        for contornoRoxo in contornosRoxo:
            areaRoxo = cv.contourArea(contornoRoxo)
            xRoxo, yRoxo, wRoxo, hRoxo = cv.boundingRect(contornoRoxo)
            if areaRoxo > 500:
                cv.rectangle(frameEspelhado, (xRoxo, yRoxo), (xRoxo+wRoxo, yRoxo+hRoxo), (255, 255, 255), 4)
                pa.click(movx,movy, 1, 12, button='right')
            
        for contornoVerde in contornosVerde:
            areaVerde = cv.contourArea(contornoVerde)
            xVerde, yVerde, wVerde, hVerde = cv.boundingRect(contornoVerde)
            if areaVerde > 500:
                cv.rectangle(frameEspelhado, (xVerde, yVerde), (xVerde+wVerde, yVerde+hVerde), (255, 255, 255), 4)
                pa.click(movx,movy, 1, 12, button='left')
        
            

    cv.imshow("Camera", frameEspelhado)
    key = cv.waitKey(60)
    if key == 27:
        break


cv.destroyAllWindows()
camera.release()