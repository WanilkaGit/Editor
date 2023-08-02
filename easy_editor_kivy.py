from PIL import Image, ImageFilter, ImageEnhance
import os

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button

from kivy.uix.widget import Widget

from kivy.uix.recycleview import RecycleView

from kivy.uix.popup import Popup

from kivy.uix.filechooser import FileChooserIconView

class EditorScreen(Screen):
    selected_dir = r"c:\Users\user\Pictures"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None

        photo_zone = Widget()

        self.btn_folder = Button(text="Папочки", size_hint=(1, 0.1))
        self.btn_folder.bind(on_release=self.chooseWorkdir)
        self.list_files = RecycleView(data=[])

        self.btn_detail = Button(text="Деталізація")
        self.btn_256_color = Button(text="Зжимання")
        self.btn_left = Button(text="Вліво")
        self.btn_right = Button(text="Вправо")
        self.btn_mirror = Button(text="Люстерко")
        self.btn_sharp = Button(text="Різкість")
        self.btn_bw = Button(text="Ч/Б")
        self.btn_blur = Button(text="Розмиття")

        col1 = BoxLayout(orientation="vertical", size_hint=(0.13, 1))
        col1.add_widget(self.btn_folder)
        col1.add_widget(self.list_files)

        row2 = BoxLayout()
        row2.add_widget(col1)
        row2.add_widget(photo_zone)

        row1 = BoxLayout(size_hint=(1, 0.1))
        row1.add_widget(self.btn_left)
        row1.add_widget(self.btn_right)
        row1.add_widget(self.btn_mirror)
        row1.add_widget(self.btn_sharp)
        row1.add_widget(self.btn_bw)
        row1.add_widget(self.btn_blur)
        row1.add_widget(self.btn_256_color)
        row1.add_widget(self.btn_detail)

        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(row2)
        main_layout.add_widget(row1)
        self.add_widget(main_layout)


    def chooseWorkdir(self, instance):
        if instance == self.btn_folder:  # Check if the button was pressed
            file_chooser = FileChooserIconView()
            file_chooser.path = EditorScreen.selected_dir
            popup = Popup(title='Виберіть папку або файл', content=file_chooser, size_hint=(0.9, 0.9))
            file_chooser.bind(on_submit=self.setWorkdir)
            popup.open()
            self.popup = popup
        
    def setWorkdir(self, instance, value, *args):
        if value is not None:
            path = value[0]
            if path:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        EditorScreen.selected_dir = path
                        self.showFileNamesList()
                    else:
                        print("Ви обрали файл:", path)
                else:
                    print("Шлях не існує:", path)
            else:
                print("Ви не обрали папку або файл")
        self.popup.dismiss()
        return True

    def showFileNamesList(self):
        extensions = [".jpg", ".png", ".jpeg", ".bmp", ".gif", ".PNG"]
        filenames = [filename for filename in os.listdir(EditorScreen.selected_dir) if os.path.splitext(filename)[1].lower() in extensions]
        self.list_files.data = [{'text': filename} for filename in filenames]
        self.list_files.refresh_from_data()

screen_editor = EditorScreen()
if screen_editor.setWorkdir:
    screen_editor.showFileNamesList()


class HeartCheck(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EditorScreen(name="editor"))
        return sm

if __name__ == "__main__":

    app = HeartCheck()

    app.run()
