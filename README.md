# 🎂 Birthday CV

Un pequeño proyecto de visión por computadora que hice para mi cumpleaños.

La idea es simple:

- Mueves una pequeña llama con la punta de tu dedo
- Acercas la llama al pastel para encender las velas
- Sopla al micrófono para apagarlas
- Al final aparecen decoraciones en pantalla

Está hecho con **Python, OpenCV, MediaPipe, NumPy y sounddevice**.

🧰 Requisitos
Python 3.11
Webcam
Micrófono
Windows recomendado

# Dependencias
pip install -r requirements.txt

Ejecutas el proyecto como: 
python main.py

🎮 Cómo usarlo
Coloca tu mano frente a la cámara.
La llama seguirá la punta de tu dedo índice.
Acerca la llama a las velas para encenderlas.
Sopla hacia el micrófono para apagarlas.
Presiona R para reiniciar.
Presiona ESC para cerrar la ventana.

# ⚙️ Ajustes

En main.py puedes modificar algunos valores:

BLOW_THRESHOLD = 0.008
LIGHT_DISTANCE = 60

CAKE_X = 300
CAKE_Y = 350

**BLOW_THRESHOLD**

Controla qué tan sensible es la detección del soplido.

Si no detecta cuando soplas, prueba con un valor más bajo.
BLOW_THRESHOLD = 0.006

Si se activa con demasiado ruido, súbelo.

**LIGHT_DISTANCE**
Controla qué tan cerca debe estar la llama de las velas para encenderlas.

# 🎨 Personalizar los assets

Puedes reemplazar los PNG de la carpeta assets/ por tus propios diseños.

🧠 ¿Cómo funciona?

El proyecto combina varias cosas:

- OpenCV para capturar y mostrar la cámara.
- MediaPipe Hands para detectar la mano y localizar la punta del dedo índice.
- NumPy para trabajar con imágenes y transparencia.
- sounddevice para obtener el nivel de audio del micrófono.
- Un poco de lógica para cambiar entre los diferentes estados del pastel.

No se entrena ningún modelo desde cero.

MediaPipe ya incluye el modelo necesario para detectar la mano.

## 📄 License

This project is licensed under the MIT License.

Copyright (c) 2026 Mauricio Lozada.
