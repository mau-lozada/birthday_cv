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

El programa no usa API keys, contraseñas ni servicios externos autenticados.
Solo necesita permisos locales para acceder a la cámara y al micrófono.

## Instalación y ejecución

Este proyecto debe ejecutarse con un entorno virtual para mantener sus
dependencias separadas de la instalación global de Python.

### Usando el entorno virtual existente

El entorno usado actualmente está en:

```text
C:\Users\Latitude 7300\Documents\.venv
```

En PowerShell:

```powershell
& "C:\Users\Latitude 7300\Documents\.venv\Scripts\Activate.ps1"
Set-Location "C:\Users\Latitude 7300\Documents\birthday_cv"
python -m pip install -r requirements.txt
python main.py
```

En CMD:

```bat
"C:\Users\Latitude 7300\Documents\.venv\Scripts\activate.bat"
cd /d "C:\Users\Latitude 7300\Documents\birthday_cv"
python -m pip install -r requirements.txt
python main.py
```

También se puede ejecutar sin activar el entorno, usando directamente su
intérprete:

```powershell
& "C:\Users\Latitude 7300\Documents\.venv\Scripts\python.exe" `
  "C:\Users\Latitude 7300\Documents\birthday_cv\main.py"
```

### Crear un entorno nuevo

Si el entorno existente no está disponible:

```powershell
Set-Location "C:\Users\Latitude 7300\Documents\birthday_cv"
py -3.11 -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

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

## Publicación en GitHub

Antes de publicar, revisa que no se incluyan credenciales. El archivo
[`.gitignore`](.gitignore) excluye entornos virtuales, archivos `.env`,
credenciales, cachés y archivos generados. Este proyecto no contiene API keys
ni secretos actualmente.

Para conectar este proyecto con un repositorio vacío de GitHub:

```powershell
Set-Location "C:\Users\Latitude 7300\Documents\birthday_cv"
git init
git add .
git status
git commit -m "Add birthday computer vision app"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

El comando `git status` permite verificar los archivos antes del primer commit.
Para que otra persona pueda subir cambios desde tu equipo, debe existir una
autenticación válida de GitHub mediante Git Credential Manager, SSH o GitHub
CLI. Nunca pegues un token, contraseña o llave privada en el código, el
`README` ni en el chat.
