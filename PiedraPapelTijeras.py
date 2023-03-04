import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

# Se inicia la captura de vídeo en el dispositivo 0
cap = cv2.VideoCapture(0)
# Dimensiones de la captura de vídeo
cap.set(3, 640)
cap.set(4, 480)

# Configuración del detector de manos
detector = HandDetector(detectionCon=0.8, maxHands=1)

timer = 0
stateResult = False
startGame = False
set_end = False
tiempofinal = 0
scores = [0, 0]  # [IA, Jugador]

# Se cargan algunas imagenes
reaccion_devil = cv2.imread(f'Resources/Devil.png', cv2.IMREAD_UNCHANGED)
reaccion_cry = cv2.imread(f'Resources/Cry.png', cv2.IMREAD_UNCHANGED)
imgPL_Wins = cv2.imread(f'Resources/Jugador.png', cv2.IMREAD_UNCHANGED)
imgAI_Wins = cv2.imread(f'Resources/IA.png', cv2.IMREAD_UNCHANGED)

while True:
    # Se lee la imagen  de fondo, debe estar dentro del loop para reiniciarse
    imgBG = cv2.imread("Resources/BG.png")

    # Se llama a la señal de captura de vídeo (Webcam)
    success, img = cap.read()

    # Se ajusta las dimensiones de la señal de vídeo recibida
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Encuentra las manos de la señal recibida por la camara
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            # Contador de cuanto tiempo se tiene desde que se presionó la tecla para iniciar
            timer = time.time() - initialTime
            # Se muestra en pantalla el contador, nótese la conversión a entero
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                # La asignación de verdadero al 'stateResult' detiene el contador e inicia el juego 
                # como tal
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    # El método siguiente retorna una salida como un array de 5 elementos, cada 
                    # uno asociado a un dedo [Pulgar, Indice, Medio, Anular, Meñique]
                    fingers = detector.fingersUp(hand)
                    # Todos los dedos abajo, piedra
                    if fingers == [0, 0, 0, 0, 0]:  
                        # Se asigna '1' para piedra
                        playerMove = 1
                    # Todos los dedos arriba, papel              
                    if fingers == [1, 1, 1, 1, 1]:  
                        # Se asigna '2' para papel
                        playerMove = 2       
                    # Indice y medio arriba, tijeras       
                    if fingers == [0, 1, 1, 0, 0]:  
                        # Se asigna '3' para tijeras
                        playerMove = 3
                    # Se genera el movimiento de la IA siguiendo las asignaciones siguientes
                    # (1 para piedra, 2 para papel, 3 para tijeras)
                    randomNumber = random.randint(1, 3)
                    # Se asigna una imagen de acuerdo al movimiento generado
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # El jugador gana cuando usa piedra vs tijeras, etc
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # La IA gana cuando el jugador usa tijeras vs piedra, etc
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    # Dentro de la imagen de fondo se inserta la captura de video del usuario
    imgBG[234:654, 795:1195] = imgScaled

    # Se muestran en pantalla las puntuaciones del jugador y la IA
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # De ser 'stateResult = True' implica que finalizó un juego, por ende la IA hizo un 
    # movimiento y debe mostrarse, además muestra algunos mensajes en base al ganador
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
        if scores[0]==2:
            
            imgBG = cvzone.overlayPNG(imgBG, imgAI_Wins, (77, 30))
            imgBG = cvzone.overlayPNG(imgBG, reaccion_devil, (406, 169))
            imgBG = cvzone.overlayPNG(imgBG, reaccion_cry, (1112, 169))
            set_end = True
        if scores[1]==2:
            
            imgBG = cvzone.overlayPNG(imgBG, imgPL_Wins, (77, 30))
            imgBG = cvzone.overlayPNG(imgBG, reaccion_cry, (406, 169))
            imgBG = cvzone.overlayPNG(imgBG, reaccion_devil, (1112, 169))
            set_end = True
            
    
    cv2.imshow("Presiona 's' para iniciar juego. 'q' para salir", imgBG)

    if set_end and tiempofinal==0:
            tiempofinal = time.time()

    # Al terminar un 'set' (alguien llega a una puntuación de 2), se reinician los puntajes
    if set_end:
        contador = time.time() - tiempofinal
        if contador > 3:
            scores = [0, 0]
            tiempofinal = 0
            set_end = False
            startGame = False
            stateResult = False
    # Espera a la tecla para iniciar el juego (s) o terminar la aplicación (q)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        # Toma el tiempo de inicio del juego
        initialTime = time.time()
        stateResult = False
    
    if key == ord('q'):
        break
