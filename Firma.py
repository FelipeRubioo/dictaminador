import os
import subprocess
import time
import ctypes
import config
from pathlib import Path

try:
    import pyautogui
    import pyperclip
except ImportError as e:
    raise ImportError(
        "Firma.py requiere las librerias 'pyautogui' y 'pyperclip'. "
        "Instalalas con: pip install pyautogui pyperclip"
    ) from e

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageGrab
except ImportError as e:
    raise ImportError(
        "Firma.py requiere 'opencv-python' y 'Pillow'. "
        "Instalalas con: pip install opencv-python Pillow"
    ) from e

# Carpeta donde vive este archivo. Las imagenes de botones se resuelven
# relativas a esta carpeta, sin importar desde donde se ejecute el script.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta al ejecutable de FIDDO. Ajustala si esta instalado en otra ubicacion.
FIDDO_PATH = config.FIDDO_PATH

# Tiempos de espera (segundos). Aumentalos si tu equipo tarda mas en cargar.
TIEMPO_ABRIR_APP = 10      # espera a que abra FIDDO
TIEMPO_DIALOGO = 1         # espera a que aparezca el dialogo de seleccion de archivo
TIEMPO_ENTRE_ACCIONES = 1  # pausa general entre clics


def firmarPDF(rutaPDF, ejecutableFiddo=FIDDO_PATH, password=None):
    """
    Automatiza la firma de un PDF usando la aplicacion de escritorio FIDDO.

    Pasos:
        1. Abre la aplicacion FIDDO.
        2. Hace clic en el boton "seleccionar llave" y selecciona la llave.
        3. Hace clic en el boton "seleccionar pdf" y selecciona el PDF.
        4. Hace clic en el boton "firmar".
        5. Escribe la contrasena de firma.

    Parametros:
        rutaPDF (str): ruta completa del PDF a firmar.
        ejecutableFiddo (str): ruta al ejecutable de FIDDO.
        password (str): contrasena para firmar. Si es None se usa config.PASSWORDFIDDO.
    """
    if password is None:
        password = config.PASSWORDFIDDO

    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

    # 1. Abrir FIDDO
    print(f"Abriendo FIDDO desde: {ejecutableFiddo}")
    subprocess.Popen([ejecutableFiddo])
    time.sleep(TIEMPO_ABRIR_APP)

    # 2. Clic en "seleccionar llave" y elegir la llave en el dialogo de Windows
    seleccionar_llave_path = Path(__file__).parent / "images" / "seleccionar_llave.png"
    if not _clickBoton(seleccionar_llave_path, "seleccionar llave"):
        raise RuntimeError(
            "No se encontro el boton 'seleccionar llave'. "
            "Asegurate de que seleccionar_llave.png este en la misma carpeta "
            "que Firma.py y que FIDDO sea visible en alguno de los monitores."
        )
    time.sleep(TIEMPO_DIALOGO)

    pyperclip.copy(config.LLAVE_PATH)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(TIEMPO_ENTRE_ACCIONES)

    # 3. Clic en "seleccionar pdf" y pegar la ruta del PDF en el dialogo
    boton_seleccionar_pdf_path = Path(__file__).parent / "images" / "boton_seleccionar_pdf.png"
    if not _clickBoton(boton_seleccionar_pdf_path, "seleccionar pdf"):
        raise RuntimeError(
            "No se encontro el boton 'seleccionar pdf'. "
            "Asegurate de que boton_seleccionar_pdf.png este en la misma carpeta "
            "que Firma.py y que FIDDO sea visible en alguno de los monitores."
        )
    time.sleep(TIEMPO_DIALOGO)

    pyperclip.copy(rutaPDF)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(TIEMPO_ENTRE_ACCIONES)

    # 4. Clic en "firmar"
    boton_firmar_path = Path(__file__).parent / "images" / "boton_firmar.png"
    if not _clickBoton(boton_firmar_path, "firmar"):
        raise RuntimeError(
            "No se encontro el boton 'firmar'. "
            "Asegurate de que boton_firmar.png este en la misma carpeta que Firma.py."
        )
    time.sleep(TIEMPO_ENTRE_ACCIONES)

    # 5. Escribir la contrasena (el campo debe tener el foco al abrirse)
    pyautogui.write(password, interval=0.05)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    print("Archivo guardado y firmado correctamente. Cierra FIDDO manualmente si es necesario.")


def _capturarTodosLosMonitores():
    """
    Captura el espacio de escritorio completo (todos los monitores) usando
    PIL directamente, sin depender de pyscreeze.

    Devuelve (imagen_bgr_numpy, offset_x, offset_y).
    offset_x/y es la esquina superior-izquierda del espacio virtual, necesaria
    para convertir coordenadas de la imagen en coordenadas reales de pantalla.
    """
    # En Windows el escritorio virtual puede empezar en coordenadas negativas
    # si hay un monitor a la izquierda o arriba del principal.
    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    offset_x = ctypes.windll.user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    offset_y = ctypes.windll.user32.GetSystemMetrics(SM_YVIRTUALSCREEN)

    captura_pil = ImageGrab.grab(all_screens=True)
    captura_rgb = np.array(captura_pil.convert("RGB"))
    captura_bgr = cv2.cvtColor(captura_rgb, cv2.COLOR_RGB2BGR)

    print(f"Captura de pantalla completa: {captura_pil.size[0]}x{captura_pil.size[1]} px "
          f"(offset virtual: {offset_x}, {offset_y})")
    return captura_bgr, offset_x, offset_y


def _clickBoton(imagenBoton, nombreBoton, confianza=0.8):
    """
    Localiza un boton en cualquiera de los monitores conectados y hace clic.

    Usa PIL + OpenCV directamente, sin pasar por pyscreeze, por lo que no
    requiere que pyscreeze este instalado.

    Pasos internos:
      1. Captura todos los monitores con ImageGrab.grab(all_screens=True).
      2. Carga el template del boton y lo convierte a BGR (elimina alfa).
      3. Usa cv2.matchTemplate para localizar el boton.
      4. Ajusta las coordenadas con el offset del escritorio virtual.
      5. Llama a pyautogui.click() con las coordenadas reales de pantalla.
    """
    # Resolver ruta relativa a la carpeta del script
    ruta = imagenBoton if os.path.isabs(imagenBoton) else os.path.join(_BASE_DIR, imagenBoton)

    if not os.path.exists(ruta):
        print(f"ERROR: no existe el archivo de imagen '{ruta}'.")
        return False

    # Cargar template como BGR (sin canal alfa)
    template_pil = Image.open(ruta).convert("RGB")
    template_bgr = cv2.cvtColor(np.array(template_pil), cv2.COLOR_RGB2BGR)
    t_alto, t_ancho = template_bgr.shape[:2]

    try:
        captura_bgr, offset_x, offset_y = _capturarTodosLosMonitores()
    except Exception as e:
        print(f"Error al capturar pantalla: {e}")
        return False

    # Reintentar con confianzas decrecientes por si hay diferencia de escala
    for conf in (confianza, 0.7, 0.6, 0.5):
        resultado = cv2.matchTemplate(captura_bgr, template_bgr, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        print(f"  '{nombreBoton}': mejor coincidencia {max_val:.3f} (umbral {conf})")

        if max_val >= conf:
            # max_loc es la esquina superior-izquierda del match en la imagen capturada.
            # Le sumamos el offset del escritorio virtual para obtener coordenadas reales.
            centro_x = max_loc[0] + t_ancho // 2 + offset_x
            centro_y = max_loc[1] + t_alto  // 2 + offset_y
            print(f"Boton '{nombreBoton}' encontrado — clic en ({centro_x}, {centro_y}).")
            pyautogui.click(centro_x, centro_y)
            return True

    print(f"No se localizo '{nombreBoton}' en ninguno de los monitores "
          f"(mejor coincidencia: {max_val:.3f}).")
    print("Sugerencias: verifica que FIDDO sea visible en pantalla, que el "
          "escalado de Windows este al 100%, o reemplaza _clickBoton por "
          "coordenadas fijas con pyautogui.click(x, y).")
    return False

