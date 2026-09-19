# Birthday CV

Aplicación interactiva de cumpleaños basada en visión por computadora. Usa la
cámara para mostrar el video en vivo, detecta la punta del dedo índice con
MediaPipe y permite encender las velas al acercarse al pastel. Después detecta
un soplido mediante el micrófono y muestra la decoración final.

## Requisitos

- Windows
- Python 3.11 (la versión usada en el entorno existente)
- Cámara web
- Micrófono

## Instalación y ejecución

Este proyecto debe ejecutarse con un entorno virtual para mantener sus
dependencias separadas de la instalación global de Python.

### Crear y activar un entorno virtual

Desde la carpeta raíz del proyecto, crea un entorno local. La carpeta `.venv`
queda excluida del repositorio mediante `.gitignore`, así que cada persona debe
crear su propio entorno en su computadora.

En PowerShell:

```powershell
Set-Location "ruta\al\proyecto\birthday_cv"
py -3.11 -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
python main.py
```

En CMD:

```bat
cd /d "ruta\al\proyecto\birthday_cv"
py -3.11 -m venv .venv
".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
python main.py
```

Si ya existe un entorno virtual, actívalo y ejecuta los mismos comandos de
instalación y arranque. No es necesario usar una ruta específica: la ruta de
`.venv` depende de dónde se haya clonado el proyecto.

También se puede ejecutar sin activar el entorno, usando directamente el
intérprete local:

```powershell
& ".\.venv\Scripts\python.exe" ".\main.py"
```

### Si `py` o Python no están disponibles

Instala Python 3.11 o una versión compatible y asegúrate de activar la opción
para agregar Python al `PATH`. Después, abre una terminal nueva y verifica:

```powershell
python --version
py --version
```

En Windows, si PowerShell bloquea la activación de scripts, puede usarse CMD
con `activate.bat` o ejecutarse directamente `.\.venv\Scripts\python.exe`.

## Controles

- Acerca la punta del dedo índice a las velas para encenderlas.
- Sopla frente al micrófono para apagarlas.
- Presiona `R` para reiniciar el estado del pastel.
- Presiona `ESC` para cerrar la aplicación.

La sensibilidad del soplido y la posición del pastel se pueden ajustar en las
constantes de configuración de `main.py`.

## Assets

Todos los recursos visuales están en [`assets/`](assets/):

| Archivo | Uso |
| --- | --- |
| `background.png` | Fondo de la escena |
| `cake_unlit.png` | Pastel con velas apagadas |
| `cake_lit.png` | Pastel con velas encendidas |
| `cake_blown.png` | Pastel después de apagar las velas |
| `flame.png` | Llama que sigue la punta del dedo |
| `corner_left.png` | Decoración de la esquina inferior izquierda |
| `corner_right.png` | Decoración de la esquina inferior derecha |

Los PNG se cargan desde una ruta relativa al archivo `main.py`, por lo que la
carpeta `assets` debe conservarse junto al programa.

## Dependencias

Las dependencias están declaradas en [`requirements.txt`](requirements.txt):

- OpenCV: captura de cámara y ventana de video
- MediaPipe: detección de la mano
- NumPy: operaciones numéricas y mezcla de imágenes
- sounddevice: lectura del nivel de audio del micrófono
