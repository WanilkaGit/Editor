from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout, QSpinBox
)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os


app = QApplication([])
window = QWidget()
window.resize(700, 500)
window.setWindowTitle("Easy editor")

"""Інтерфейс Програми"""

btn_folder = QPushButton("PAPKA")
list_files = QListWidget()

main_label = QLabel("Picture")

btn_detail = QPushButton("Деталізація")
btn_256_color = QPushButton("256 кольор")
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")
btn_blur = QPushButton("Розмиття")

col1 = QVBoxLayout()
col1.addWidget(btn_folder)
col1.addWidget(list_files)

col2 = QVBoxLayout()
col2.addWidget(main_label)


row1 = QHBoxLayout()
row1.addWidget (btn_left)
row1.addWidget (btn_right)
row1.addWidget (btn_mirror)
row1.addWidget (btn_sharp)
row1.addWidget (btn_bw)
row1.addWidget (btn_blur)
row1.addWidget (btn_256_color)
row1.addWidget (btn_detail)

col2.addLayout(row1)

main_layout = QHBoxLayout()

main_layout.addLayout(col1, 20)
main_layout.addLayout(col2, 80)

window.setLayout(main_layout)
window.show()
"""Функіонал програми"""

workdir = ""

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in  files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFileNamesList():
    extensions = [".jpg", ".png", ".jpeg", ".bmp", ".gif",".PNG"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)



class ImageProcessor:# клас для обробки зображень
    def __init__(self):#конструктор класу
        self.image = None#картинка
        self.dir = None#шлях до файлу
        self.filename = None# назва файлу
        self.save_dir = "Modified/"#папка бля оброблених фото

    def loadImage(self, dir, filename):#метод для додавання фото
        self.dir = dir#в зміну шлях до фото
        self.filename = filename# в зміну назву файлу
        image_path = os.path.join(dir, filename)# збираєм повний шлях до картинки
        self.image = Image.open(image_path)#сюда всю інфу про нову артинку

    def showImage(self, path):# показуємо картинку в додатку
        main_label.hide()#ховати надпис
        pix_map_image = QPixmap(path)#відкриваєм щоб бачить
        w, h = main_label.width(), main_label.height()#берем ширину і довжину в зміні
        pix_map_image = pix_map_image.scaled(w, h, Qt.KeepAspectRatio)#збираєм ще інфу про картинку в зміну
        main_label.setPixmap(pix_map_image)# уже вирявнену картинку
        main_label.show()# показування картинки

    def saveImage(self):#збереження картинки в папку
        path = os.path.join(workdir, self.save_dir)#шлях
        if not (os.path.exists(path) or os.path.isdir(path)):# якщо папки нема створюєм її якщо вона є
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip (self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpner(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_detail(self):
        self.image = self.image.filter(ImageFilter.DETAIL)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_b_w(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_256_color(self):
        self.image = self.image.convert("P")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


workimage = ImageProcessor()# тепе через це відображаєм картинку

def showChosenImage():# для вдображення картинки
    if list_files.currentRow() >= 0:# якщо більше нуля програма зрозуміла що щось натиснуто
        filename = list_files.currentItem().text()# повертає шлях
        workimage.loadImage(workdir, filename)#загружаєм картинку
        image_path = os.path.join(workdir, filename)#
        workimage.showImage(image_path)# показ вибраної картинки

btn_folder.clicked.connect(showFileNamesList)#підключаєм щоб кнпки пахали
list_files.currentRowChanged.connect(showChosenImage)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_bw.clicked.connect(workimage.do_b_w)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpner)
btn_blur.clicked.connect(workimage.do_blur)
btn_256_color.clicked.connect(workimage.do_256_color)
btn_detail.clicked.connect(workimage.do_detail)



app.exec_()