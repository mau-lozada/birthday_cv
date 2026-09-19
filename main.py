import os
import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
import threading
import time

#CONFIG

CAM_W = 960
CAM_H = 720

CAKE_X = 300
CAKE_Y = 350

BLOW_THRESHOLD = 0.008 #se ajusta
LIGHT_DISTANCE = 60 # distancia para "encender" velas

cake_lit = False
candles_blown = False
audio_level = 0.0

#AUDIO

def audio_callback(indata, frames, time_info, status):
    global audio_level
    volume_norm = np.linalg.norm(indata) / len(indata)
    audio_level = volume_norm

def start_audio_stream():
    stream = sd.InputStream(callback=audio_callback)
    stream.start()
    return stream

#IMAGE

def overlay_png(bg, overlay, x, y):
        # Pega un PNG con alpha encima del frame bg en posición x,y
        h, w = overlay.shape[:2] #aqui se obtiene el alto y ancho del png
    
        if x >= bg.shape[1] or y >= bg.shape[0]:
            return bg                       #revisar si esta completamente fuera del frame, si es asi no hace nada.

        if x + w <= 0 or y + h <= 0:
            return bg

        x1 = max(x, 0) #donde inicia el png, si es negativo se ajusta a 0
        y1 = max(y, 0)
        x2 = min(x + w, bg.shape[1]) #donde termina el png, si es mayor al tamaño del frame se ajusta al tamaño del frame
        y2 = min(y + h, bg.shape[0])

        #que parte del png se va a usar.
        overlay_x1 = x1 - x 
        overlay_y1 = y1 - y
        overlay_x2 = overlay_x1 + (x2 - x1)
        overlay_y2 = overlay_y1 + (y2 - y1) 

        overlay_crop = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2] #toma el pedazo del png que se va a usar

        if overlay_crop.shape[2] < 4:
            return bg
        
        alpha = overlay_crop[:, :, 3] / 255.0 #alpha es la transparencia del png, se normaliza a 0-1
        alpha = np.dstack([alpha, alpha, alpha])  #toma el control del canal alpha para mezclar el png con el fondo

        bg_crop = bg[y1:y2, x1:x2]
        overlay_rgb = overlay_crop[:, :, :3] #es la imagen png sin el canal alpha, solo RGB

        blended = (alpha * overlay_rgb + (1 - alpha) * bg_crop).astype(np.uint8) #mezcla el png con el fondo usando el canal alpha para controlar la transparencia
        bg[y1:y2, x1:x2] = blended

        return bg

def resize_to_fit_with_padding(img, target_w, target_h):
    h, w = img.shape[:2]
    scale = min(target_w / w, target_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # lienzo transparente BGRA
    canvas = np.zeros((target_h, target_w, 4), dtype=np.uint8)

    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2

    canvas[y:y+new_h, x:x+new_w] = resized
    return canvas

#LOAD ASSETS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

background_path = os.path.join(ASSETS_DIR, "background.png")
cake_unlit_path = os.path.join(ASSETS_DIR, "cake_unlit.png")
cake_lit_path = os.path.join(ASSETS_DIR, "cake_lit.png")
cake_blown_path = os.path.join(ASSETS_DIR, "cake_blown.png")
flame_path = os.path.join(ASSETS_DIR, "flame.png")
#sparkles_path = os.path.join(ASSETS_DIR, "sparkles.png")
corner_left_path = os.path.join(ASSETS_DIR, "corner_left.png")
corner_right_path = os.path.join(ASSETS_DIR, "corner_right.png")

print("BASE_DIR:", BASE_DIR)
print("ASSETS_DIR:", ASSETS_DIR)
print("background exists:", os.path.exists(background_path), background_path)
print("cake_unlit exists:", os.path.exists(cake_unlit_path), cake_unlit_path)
print("cake_lit exists:", os.path.exists(cake_lit_path), cake_lit_path)
print("cake_blown exists:", os.path.exists(cake_blown_path), cake_blown_path)
print("flame exists:", os.path.exists(flame_path), flame_path)
print("corner_left exists:", os.path.exists(corner_left_path), corner_left_path)
print("corner_right exists:", os.path.exists(corner_right_path), corner_right_path)

background = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
cake_unlit = cv2.imread(cake_unlit_path, cv2.IMREAD_UNCHANGED)
cake_lit_img = cv2.imread(cake_lit_path, cv2.IMREAD_UNCHANGED)
cake_blown = cv2.imread(cake_blown_path, cv2.IMREAD_UNCHANGED)
flame = cv2.imread(flame_path, cv2.IMREAD_UNCHANGED)
corner_left = cv2.imread(corner_left_path, cv2.IMREAD_UNCHANGED)
corner_right = cv2.imread(corner_right_path, cv2.IMREAD_UNCHANGED)

print("background is None:", background is None)
print("cake_unlit is None:", cake_unlit is None)
print("cake_lit_img is None:", cake_lit_img is None)
print("cake_blown is None:", cake_blown is None)
print("flame is None:", flame is None)
print("corner_left is None:", corner_left is None)
print("corner_right is None:", corner_right is None)

if background is None or cake_unlit is None or cake_lit_img is None or cake_blown is None or flame is None:
    raise FileNotFoundError("Revisa que existan los png en la carpeta, papito.")

#opcional: redimensionar
background = cv2.resize(background, (CAM_W, CAM_H))
cake_unlit = resize_to_fit_with_padding(cake_unlit, 280, 200)
cake_lit_img = resize_to_fit_with_padding(cake_lit_img, 280, 200)
cake_blown = resize_to_fit_with_padding(cake_blown, 280, 200)
flame = resize_to_fit_with_padding(flame, 60, 60)
#sparkles = cv2.resize(sparkles, (180, 90))
corner_left = cv2.resize(corner_left, (180, 180))
corner_right = cv2.resize(corner_right, (180, 180))

#punto aproximado donde están las velas en el pastel
candle_point = (CAKE_X + 175, CAKE_Y + 25) #ajustar según el diseño del pastel

#MEDIAPIPE
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7, #ajustar según el rendimiento y precisión deseada
    min_tracking_confidence=0.6
)

#CAMERA
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

audio_stream = start_audio_stream()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        display = frame.copy()

        # pastel según estado
        if candles_blown:
            current_cake = cake_blown
        elif cake_lit:
            current_cake = cake_lit_img
        else: 
            current_cake = cake_unlit
        display = overlay_png(display, current_cake, CAKE_X, CAKE_Y)    

        # procesar mano
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        finger_x, finger_y = None, None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(display, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # landmark 8 = punta del dedo indice
            index_tip = hand_landmarks.landmark[8]
            finger_x = int(index_tip.x * CAM_W)
            finger_y = int(index_tip.y * CAM_H)

            # dibujar llama siguiendo el dedo
            display = overlay_png(display, flame, finger_x - 30, finger_y - 65)

            # si no está encendido todavía, revisar cercanía con velas
            if not cake_lit:
                dist = ((finger_x - candle_point[0]) ** 2 + (finger_y - candle_point[1]) ** 2) ** 0.5
                if dist < LIGHT_DISTANCE:
                    cake_lit = True

        # detectar soplido
        if cake_lit and not candles_blown:
            if audio_level > BLOW_THRESHOLD:
                candles_blown = True

        if candles_blown:
            #display = overlay_png(display, sparkles, 40, 40)
            #display = overlay_png(display, sparkles, CAM_W - 220, 40)

            cv2.putText(display, "It's my BDay, bitch!", (250, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 220, 173), 3)

            left_h, left_w = corner_left.shape[:2]
            right_h, right_w = corner_right.shape[:2]

            display = overlay_png(display, corner_left, 20, CAM_H - left_h - 180)
            display = overlay_png(display, corner_right, CAM_W - right_w - 20, CAM_H - right_h - 180)

        cv2.imshow("Birthday CV - Mau", display)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('r'):
            cake_lit = False
            candles_blown = False

finally:
    cap.release()
    cv2.destroyAllWindows()
    audio_stream.stop()
    audio_stream.close()
