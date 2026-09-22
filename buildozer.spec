[app]

# (str) Title of your application
title = Gestor de Lotes y Fotos

# (str) Package name
package.name = customcamera

# (str) Package domain (needed for android packaging)
package.domain = org.customcamera

# (list) Source files to include (let it include python, json, images, etc.)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Source files to exclude (optional)
#source.exclude_exts = spec

# (list) List of directory to include (from source.dir)
source.include_dir = 

# (str) Application versioning
version = 1.0

# (list) Application requirements
# ¡Importante! Incluye python3, kivy, pillow y pyjnius (que es el nombre del paquete para jnius)
requirements = python3,kivy,pillow,pyjnius

# (list) Supported orientations
# Permite tanto vertical como horizontal para que respete el giro de tu app y la cámara
orientation = landscape,portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Necesarios para usar la cámara y guardar en la carpeta DCIM/PYTHON del almacenamiento
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support. 21 is standard.
android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) Use Android X
android.androidx = True

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
