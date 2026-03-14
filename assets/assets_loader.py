import os
from PIL import Image, ImageTk


# ==============================
# RUTA BASE DEL PROYECTO
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICONS_PATH = os.path.join(BASE_DIR, "icons")
IMAGES_PATH = os.path.join(BASE_DIR, "images")


class Assets:

    icons = {}
    images = {}

    ICON_SIZE = (24, 24)
    IMAGE_SIZE = (120, 120)

    # =================================
    # CARGAR ICONOS
    # =================================

    @staticmethod
    def load_icons():

        if not os.path.exists(ICONS_PATH):
            print("⚠ Carpeta icons no encontrada:", ICONS_PATH)
            return

        for file in os.listdir(ICONS_PATH):

            if file.lower().endswith(".png"):

                name = file.replace(".png", "")
                path = os.path.join(ICONS_PATH, file)

                try:

                    img = Image.open(path)
                    img = img.resize(Assets.ICON_SIZE, Image.LANCZOS)

                    Assets.icons[name] = ImageTk.PhotoImage(img)

                except Exception as e:

                    print(f"Error cargando icono {file}: {e}")

    # =================================
    # CARGAR IMAGENES
    # =================================

    @staticmethod
    def load_images():

        if not os.path.exists(IMAGES_PATH):
            print("⚠ Carpeta images no encontrada:", IMAGES_PATH)
            return

        for file in os.listdir(IMAGES_PATH):

            if file.lower().endswith(".png"):

                name = file.replace(".png", "")
                path = os.path.join(IMAGES_PATH, file)

                try:

                    img = Image.open(path)
                    img = img.resize(Assets.IMAGE_SIZE, Image.LANCZOS)

                    Assets.images[name] = ImageTk.PhotoImage(img)

                except Exception as e:

                    print(f"Error cargando imagen {file}: {e}")

    # =================================
    # OBTENER ICONO
    # =================================

    @staticmethod
    def get_icon(name):

        return Assets.icons.get(name)

    # =================================
    # OBTENER IMAGEN
    # =================================

    @staticmethod
    def get_image(name):

        return Assets.images.get(name)