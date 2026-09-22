import json
import os
from datetime import datetime
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

try:
  from PIL import Image as PILImage, ImageOps

  PIL_AVAILABLE = True
except ImportError:
  PIL_AVAILABLE = False

try:
  from jnius import autoclass, cast

  ANDROID = True
except ImportError:
  ANDROID = False


class CardLayout(BoxLayout):

  def __init__(self, bg_color=(0.15, 0.18, 0.22, 1), **kwargs):
    super(CardLayout, self).__init__(**kwargs)
    with self.canvas.before:
      Color(*bg_color)
      self.rect = RoundedRectangle(
          pos=self.pos, size=self.size, radius=[15]
      )
    self.bind(pos=self.update_rect, size=self.update_rect)

  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size


class RoundedButton(Button):

  def __init__(self, bg_color=(0.1, 0.65, 0.3, 1), radius=[35], **kwargs):
    super(RoundedButton, self).__init__(**kwargs)
    self.bg_color = bg_color
    self.radius = radius
    self.background_normal = ""
    self.background_down = ""
    self.background_color = (0, 0, 0, 0)

    with self.canvas.before:
      self.inst_color = Color(*self.bg_color)
      self.rect = RoundedRectangle(
          pos=self.pos, size=self.size, radius=self.radius
      )
    self.bind(pos=self.update_rect, size=self.update_rect)

  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size

  def set_bg_color(self, color):
    self.bg_color = color
    self.inst_color.rgba = color


class CustomCameraApp(App):

  def build(self):
    from kivy.core.window import Window

    Window.clearcolor = (0.08, 0.10, 0.12, 1)

    saved_lote, saved_modelo, saved_ancho, saved_alto, saved_calidad = (
        self.load_state()
    )

    root_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

    self.layout = BoxLayout(
        orientation="vertical", padding=25, spacing=20, size_hint_y=None
    )
    self.layout.bind(minimum_height=self.layout.setter("height"))

    # --- 1 y 2. LOTE Y MODELO EN UNA SOLA LÍNEA ---
    lote_modelo_card = CardLayout(
        orientation="horizontal",
        padding=15,
        spacing=15,
        size_hint_y=None,
        height=210,
        bg_color=(0.14, 0.18, 0.24, 1),
    )

    # LOTE (Excepción: tamaño de fuente más grande)
    col_lote = BoxLayout(orientation="vertical", spacing=5, size_hint_x=0.65)
    col_lote.add_widget(
        Label(
            text="LOTE:",
            font_size=40,
            size_hint_y=None,
            height=50,
            color=(0.7, 0.8, 1, 1),
        )
    )
    self.lote_input = TextInput(
        text=saved_lote,
        font_size=75,
        multiline=False,
        size_hint_y=None,
        height=100,
        halign="center",
        background_color=(0.2, 0.24, 0.3, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.lote_input.bind(
        text=lambda instance, value: (self.save_state(), self.actualizar_conteo())
    )
    col_lote.add_widget(self.lote_input)
    lote_modelo_card.add_widget(col_lote)

    # MODELO (Limitado a 7 caracteres, fuente grande y centrada)
    col_modelo = BoxLayout(orientation="vertical", spacing=5, size_hint_x=0.35)
    col_modelo.add_widget(
        Label(
            text="MODELO:",
            font_size=40,
            size_hint_y=None,
            height=50,
            color=(1, 0.82, 0, 1),
        )
    )
    self.modelo_input = TextInput(
        text=saved_modelo[:7],
        font_size=65,
        multiline=False,
        size_hint_y=None,
        height=100,
        halign="center",
        background_color=(0.2, 0.24, 0.3, 1),
        foreground_color=(1, 1, 1, 1),
    )

    def limitar_modelo(instance, value):
      if len(value) > 7:
        instance.text = value[:7]
      self.save_state()

    self.modelo_input.bind(text=limitar_modelo)
    col_modelo.add_widget(self.modelo_input)
    lote_modelo_card.add_widget(col_modelo)

    self.layout.add_widget(lote_modelo_card)

    # --- 3, 4 y 5. ANCHO, ALTO Y CALIDAD EN UNA SOLA LÍNEA ---
    params_card = CardLayout(
        orientation="horizontal",
        padding=15,
        spacing=15,
        size_hint_y=None,
        height=210,
        bg_color=(0.14, 0.18, 0.24, 1),
    )

    # ANCHO
    col_ancho = BoxLayout(orientation="vertical", spacing=5)
    col_ancho.add_widget(
        Label(
            text="ANCHO",
            font_size=40,
            size_hint_y=None,
            height=50,
            color=(0.8, 0.8, 1, 1),
        )
    )
    self.ancho_input = TextInput(
        text=saved_ancho,
        font_size=65,
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=100,
        halign="center",
        background_color=(0.2, 0.24, 0.3, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.ancho_input.bind(text=lambda instance, value: self.save_state())
    col_ancho.add_widget(self.ancho_input)
    params_card.add_widget(col_ancho)

    # ALTO
    col_alto = BoxLayout(orientation="vertical", spacing=5)
    col_alto.add_widget(
        Label(
            text="ALTO",
            font_size=40,
            size_hint_y=None,
            height=50,
            color=(0.8, 0.8, 1, 1),
        )
    )
    self.alto_input = TextInput(
        text=saved_alto,
        font_size=65,
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=100,
        halign="center",
        background_color=(0.2, 0.24, 0.3, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.alto_input.bind(text=lambda instance, value: self.save_state())
    col_alto.add_widget(self.alto_input)
    params_card.add_widget(col_alto)

    # CALIDAD
    col_calidad = BoxLayout(orientation="vertical", spacing=5)
    col_calidad.add_widget(
        Label(
            text="CALIDAD",
            font_size=40,
            size_hint_y=None,
            height=50,
            color=(0.6, 0.9, 0.6, 1),
        )
    )
    self.calidad_input = TextInput(
        text=saved_calidad,
        font_size=65,
        multiline=False,
        input_filter="int",
        size_hint_y=None,
        height=100,
        halign="center",
        background_color=(0.2, 0.24, 0.3, 1),
        foreground_color=(1, 1, 1, 1),
    )
    self.calidad_input.bind(text=lambda instance, value: self.save_state())
    col_calidad.add_widget(self.calidad_input)
    params_card.add_widget(col_calidad)

    self.layout.add_widget(params_card)

    # --- 6. BOTÓN DE TOMAR FOTO ---
    self.btn_open_cam = RoundedButton(
        text="TOMAR FOTO",
        font_size=70,
        bold=True,
        bg_color=(0.1, 0.65, 0.3, 1),
        radius=[30],
        size_hint_y=None,
        height=140,
    )
    self.btn_open_cam.bind(on_press=self.open_native_camera)
    self.layout.add_widget(self.btn_open_cam)

    # --- 7. ETIQUETA DE CONTEO DE FOTOS ---
    self.count_label = Label(
        text="FOTOS TOMADAS EN ESTE LOTE: 0",
        font_size=42,
        size_hint_y=None,
        height=80,
        color=(0.9, 0.9, 0.9, 1),
    )
    self.layout.add_widget(self.count_label)

    root_scroll.add_widget(self.layout)

    self.actualizar_conteo()

    return root_scroll

  def get_state_file_path(self):
    return os.path.join(self.user_data_dir, "app_state.json")

  def load_state(self):
    path = self.get_state_file_path()
    if os.path.exists(path):
      try:
        with open(path, "r") as f:
          data = json.load(f)
          return (
              data.get("lote", "LOTE01"),
              data.get("modelo", "MOD_A"),
              data.get("ancho", "1280"),
              data.get("alto", "720"),
              data.get("calidad", "90"),
          )
      except Exception:
        pass
    return "LOTE01", "MOD_A", "1280", "720", "90"

  def save_state(self):
    path = self.get_state_file_path()
    try:
      data = {
          "lote": self.lote_input.text.strip().upper(),
          "modelo": self.modelo_input.text.strip().upper()[:7],
          "ancho": self.ancho_input.text.strip(),
          "alto": self.alto_input.text.strip(),
          "calidad": self.calidad_input.text.strip(),
      }
      with open(path, "w") as f:
        json.dump(data, f)
    except Exception as e:
      print(f"Error guardando JSON: {e}")

  def obtener_carpeta_lote(self):
    if not ANDROID:
      return None
    try:
      Environment = autoclass("android.os.Environment")
      File = autoclass("java.io.File")
      dcim_dir = Environment.getExternalStoragePublicDirectory(
          Environment.DIRECTORY_DCIM
      )
      python_folder = File(dcim_dir, "PYTHON")
      lote_text = self.lote_input.text.strip().upper() or "SIN_LOTE"
      lote_folder = File(python_folder, lote_text)
      return lote_folder
    except Exception:
      return None

  def actualizar_conteo(self):
    if not ANDROID:
      return
    try:
      lote_folder = self.obtener_carpeta_lote()
      if lote_folder and lote_folder.exists():
        archivos = lote_folder.list()
        cantidad = len([f for f in archivos if f.endswith(".jpg")])
        self.count_label.text = f"FOTOS TOMADAS EN ESTE LOTE: {cantidad}"
      else:
        self.count_label.text = "FOTOS TOMADAS EN ESTE LOTE: 0"
    except Exception:
      self.count_label.text = "FOTOS TOMADAS EN ESTE LOTE: 0"

  def open_native_camera(self, instance):
    if not ANDROID:
      return

    lote_text = self.lote_input.text.strip().upper() or "SIN_LOTE"
    modelo_text = self.modelo_input.text.strip().upper()[:7] or "FOTO"

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_filename = f"{lote_text}_{modelo_text}_{timestamp}"

    try:
      StrictMode = autoclass("android.os.StrictMode")
      builder = autoclass("android.os.StrictMode$VmPolicy$Builder")
      StrictMode.setVmPolicy(builder().build())

      PythonActivity = autoclass("org.kivy.android.PythonActivity")
      Intent = autoclass("android.content.Intent")
      MediaStore = autoclass("android.provider.MediaStore")
      File = autoclass("java.io.File")
      Uri = autoclass("android.net.Uri")

      current_activity = PythonActivity.mActivity
      lote_folder = self.obtener_carpeta_lote()
      if lote_folder and not lote_folder.exists():
        lote_folder.mkdirs()

      self.photo_file = File(lote_folder, f"{full_filename}.jpg")

      photo_uri = Uri.parse("file://" + self.photo_file.getAbsolutePath())
      uri_parcelable = cast("android.os.Parcelable", photo_uri)

      intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
      intent.putExtra(MediaStore.EXTRA_OUTPUT, uri_parcelable)

      current_activity.startActivityForResult(intent, 0x123)

      from kivy.clock import Clock

      Clock.schedule_once(
          lambda dt: self.corregir_orientacion_y_redimensionar(), 2.0
      )

    except Exception as e:
      print(f"Error al abrir cámara: {e}")

  def corregir_orientacion_y_redimensionar(self):
    if not PIL_AVAILABLE:
      print("Pillow no está disponible.")
      return

    try:
      if hasattr(self, "photo_file") and self.photo_file.exists():
        ruta_path = self.photo_file.getAbsolutePath()

        with PILImage.open(ruta_path) as img:
          img = ImageOps.exif_transpose(img)

          orig_width, orig_height = img.size

          base_ancho = int(self.ancho_input.text.strip() or 1280)
          base_alto = int(self.alto_input.text.strip() or 720)
          calidad_val = int(self.calidad_input.text.strip() or 90)
          calidad_val = max(1, min(100, calidad_val))

          es_vertical_real = orig_height > orig_width
          es_vertical_config = base_alto > base_ancho

          if es_vertical_real != es_vertical_config:
            ancho_deseado = base_alto
            alto_deseado = base_ancho
          else:
            ancho_deseado = base_ancho
            alto_deseado = base_alto

          img_resized = img.resize(
              (ancho_deseado, alto_deseado), PILImage.Resampling.LANCZOS
          )
          img_resized.save(ruta_path, "JPEG", quality=calidad_val)

          self.actualizar_conteo()
    except Exception as ex:
      print(f"Error al procesar la foto: {ex}")


if __name__ == "__main__":
  CustomCameraApp().run()