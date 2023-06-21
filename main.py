import sys

import qdarktheme
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets
import os
import magic
import fitz

import subprocess as sb


class QDoubleButton(QtWidgets.QToolButton):
    right_clicked = QtCore.Signal()
    left_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(QDoubleButton, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == QtCore.Qt.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.is_double = True
            return True

        return False

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False

    def left_click_event(self):
        print('left clicked')

    def right_click_event(self):
        print('right clicked')

    def double_click_event(self):
        print('double clicked')

def open_file(*args):
    return lambda: sb.call(("xdg-open", *args))

def open_folder_func(layout, path, window):
    print(path + "1234123")
    curr_path = path
    curr_files = os.listdir(curr_path)
    print(curr_files)

    layout.takeAllWidgets()
    iconProvider = QtWidgets.QFileIconProvider()

    filetypes2icons = {"text/plain" : "text-x-generic",
                        "application/zip" : "file-archiver",
                        "application/x-bittorrent" : "ktorrent",
                        "application/msword" : "libreoffice-writer",
                        "application/vnd.debian.binary-package" : "application-vnd.debian.binary-package",
                        "text/x-shellscript" : "text-x-script",
                        "application/x-iso9660-image" : "drive-optical",
                        "application/x-executable" : "application-x-executable",
                        "application/gzip" : "file-archiver"}
    image_types = ["image/png", "image/bmp", "image/jpeg"]

    for i in curr_files:
        button = QDoubleButton(window)
        button.setText(i)
        try:
            ftype = magic.from_file(curr_path + i, mime=1)
            #print(ftype)
            if(ftype in filetypes2icons):
                button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons[ftype]))
            else:
                if(ftype in image_types):

                    button.setIcon(QtGui.QIcon(curr_path + i))
                elif(ftype == "application/pdf"):
                    pdffile = curr_path + i
                    doc = fitz.open(pdffile)
                    page = doc.load_page(0)  # number of page
                    pix = page.get_pixmap()
                    pix.save("tmp.png")
                    button.setIcon(QtGui.QIcon(QtGui.QIcon("./tmp.png")))
                    os.remove("./tmp.png")
                    doc.close()
                else:
                    button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons["text/plain"]))

            button.double_clicked.connect(self.open_file(curr_path + i))
        except:
            button.setIcon(QtGui.QIcon.fromTheme("folder"))
            button.double_clicked.connect(open_folder(layout, curr_path + i))

        button.setIconSize(QtCore.QSize(50, 50))
        button.setFixedWidth(75)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.setStyleSheet("QToolButton {padding-left : 5px; font-size: 16px;}")
        layout.addWidget(button)


def open_folder(layout, path, window):
    #print(path)
    return lambda: open_folder_func(layout, path, window)


class LeFiles(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.curr_path = os.path.expanduser('~')
        print(self.curr_path)
        self.forward_folder_path = self.curr_path

        self.setWindowTitle("LeFiles")
        QtGui.QIcon.setThemeName("candy-icons")

        self.main_group = QtWidgets.QGroupBox()
        self.main_group.setContentsMargins(0,0,0,0)
        self.main_group.setStyleSheet("QGroupBox {border: 0px;}")


        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(0,0,0,0)

        self.mygroupbox = QtWidgets.QGroupBox()

        self.main_group.setLayout(self.vbox)

        self.layout = qfluentwidgets.FlowLayout(needAni=True)

        self.mygroupbox.setLayout(self.layout)
        self.mygroupbox.setContentsMargins(0,0,0,0)

        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setContentsMargins(0,0,0,0)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea {border: 0px;}")


        self.back_folder_button = QtWidgets.QToolButton()
        self.back_folder_button.setText("<")
        self.back_folder_button.setStyleSheet("QToolButton {font-size: 25px;}")
        #self.back_folder_button.setIcon(QtGui.QIcon("./custom_icons/left-arrow.svg"))
        #self.back_folder_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #self.back_folder_button.setIconSize(QtCore.QSize(17, 17))
        self.back_folder_button.setFixedWidth(30)
        self.back_folder_button.setFixedHeight(30)
        self.back_folder_button.clicked.connect(self.go_to_back_folder_path)

        self.forward_folder_button = QtWidgets.QToolButton()
        self.forward_folder_button.setText(">")
        self.forward_folder_button.setStyleSheet("QToolButton {font-size: 25px;}")
        #self.back_folder_button.setIcon(QtGui.QIcon("./custom_icons/left-arrow.svg"))
        #self.back_folder_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #self.back_folder_button.setIconSize(QtCore.QSize(17, 17))
        self.forward_folder_button.setFixedWidth(30)
        self.forward_folder_button.setFixedHeight(30)
        self.forward_folder_button.clicked.connect(self.go_to_forward_folder)

        #⊚


        self.input_path = QtWidgets.QLineEdit()
        self.input_path.setText(self.curr_path)
        #self.input_path.setStyleSheet("QLineEdit { margin-right: 25px;}")

        self.go_to_button = QtWidgets.QToolButton()
        self.go_to_button.setText("⊚")
        self.go_to_button.setStyleSheet("QToolButton {font-size: 25px;}")
        #self.back_folder_button.setIcon(QtGui.QIcon("./custom_icons/left-arrow.svg"))
        #self.back_folder_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #self.back_folder_button.setIconSize(QtCore.QSize(17, 17))
        self.go_to_button.setFixedWidth(30)
        self.go_to_button.setFixedHeight(30)
        self.go_to_button.clicked.connect(self.go_to_line_folder)

        self.hbox_groub_box = QtWidgets.QGroupBox()
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setContentsMargins(10,0,10,0)
        self.hbox.addWidget(self.back_folder_button)
        self.hbox.addWidget(self.forward_folder_button)
        self.hbox.addWidget(self.input_path)
        self.hbox.addWidget(self.go_to_button)

        self.hbox_groub_box.setLayout(self.hbox)


        self.vbox.addWidget(self.hbox_groub_box)
        self.vbox.addWidget(self.scroll)

        self.layout.setAnimation(500, QtCore.QEasingCurve.OutQuad)


        self.open_folder_func(self.layout, self.curr_path)
        self.setCentralWidget(self.main_group)

        #ui = conf.UI()
        #ui.setUI()

    def go_to_line_folder(self):
        text = self.input_path.text()
        if(text[-1] == "/"):
            self.open_folder_func(self.layout, text[:-1])
        else:
            self.open_folder_func(self.layout, text)

    def go_to_forward_folder(self):
        print("forward")
        print(self.forward_folder_path)
        #if(self.forward_folder_path == self.curr_path):
            #self.forward_folder_path =
        self.open_folder_func(self.layout, self.forward_folder_path)

    def go_to_back_folder_path(self):
        #print(self.curr_path)
        self.forward_folder_path = self.curr_path[:-1]
        tmp = self.curr_path.split("/")
        new_path = "/"
        for i in range(1, len(tmp) - 2):
            new_path += tmp[i] + "/"
        self.open_folder_func(self.layout, new_path[:-1])

    def open_file(self, *args):
        return lambda: sb.call(("xdg-open", *args))

    def open_folder_func(self, layout, path):
        #print(path + "1234123")
        self.curr_path = path + "/"
        self.input_path.setText(self.curr_path[:-1])
        print(self.curr_path)
        curr_files = os.listdir(self.curr_path)
        #print(curr_files)

        self.layout.takeAllWidgets()
        iconProvider = QtWidgets.QFileIconProvider()

        filetypes2icons = {"zip" : "file-archiver",
                           "deb" : "application-vnd.debian.binary-package",
                           "xz" : "file-archiver",
                           "torrent" : "ktorrent",
                           "gz" : "file-archiver",
                           "js" : "application-javascript",
                           "zip" : "file-archiver",
                           "json" : "application-json",
                           "css" : "text-css"}
        image_types = ["png", "bmp", "jpeg", "jpg", "svg"]

        for i in curr_files:
            button = QDoubleButton(self)
            button.setText(i)
            fileInfo = QtCore.QFileInfo(self.curr_path + i)
            #print(fileInfo.suffix())
            ftype = fileInfo.suffix()#magic.from_file(curr_path + i, mime=1)
            #print(i)
            #print(ftype)
            flag = 1
            if(ftype in filetypes2icons):
                button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons[ftype]))
                flag = 0
            else:
                if(ftype in image_types):
                    button.setIcon(QtGui.QIcon(self.curr_path + i))
                    flag = 0
                elif(ftype == "application/pdf"):
                    pdffile = self.curr_path + i
                    doc = fitz.open(pdffile)
                    page = doc.load_page(0)  # number of page
                    pix = page.get_pixmap()
                    pix.save("tmp.png")
                    button.setIcon(QtGui.QIcon("./tmp.png"))
                    os.remove("./tmp.png")
                    doc.close()
                    flag = 0
            if(not flag):
                button.double_clicked.connect(self.open_file(self.curr_path + i))
            if(fileInfo.isDir() and flag):
                button.setIcon(QtGui.QIcon.fromTheme("folder"))
                button.double_clicked.connect(self.open_folder(layout, self.curr_path + i))
            elif flag:
                button.setIcon(QtGui.QIcon("custom_icons/question-mark.svg"))
                button.double_clicked.connect(self.open_file(self.curr_path + i))
            button.setIconSize(QtCore.QSize(50, 50))
            button.setFixedWidth(75)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet("QToolButton {padding-left : 5px; font-size: 16px;}")
            layout.addWidget(button)


    def open_folder(self, layout, path):
        #print(path)
        return lambda: self.open_folder_func(layout, path)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    qdarktheme.setup_theme()

    app.setFont(QtGui.QFont("Ubuntu Mono"))

    lefiles = LeFiles()
    lefiles.resize(800, 600)
    lefiles.show()

    sys.exit(app.exec())
