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

            button.double_clicked.connect(open_file(curr_path + i))
        except:
            button.setIcon(QtGui.QIcon.fromTheme("folder"))
            button.double_clicked.connect(lambda: open_folder(layout, curr_path + i))

        button.setIconSize(QtCore.QSize(50, 50))
        button.setFixedWidth(75)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.setStyleSheet("QToolButton {padding-left : 5px; font-size: 16px;}")
        layout.addWidget(button)


def open_folder(*args):
    #print(path)
    return lambda: open_folder_func(*args)


class LeFiles(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LeFiles")
        QtGui.QIcon.setThemeName("candy-icons")

        self.mygroupbox = QtWidgets.QGroupBox()



        self.layout = qfluentwidgets.FlowLayout(needAni=True)

        self.mygroupbox.setLayout(self.layout)
        self.mygroupbox.setContentsMargins(0,0,0,0)

        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setContentsMargins(0,0,0,0)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)



        self.layout.setAnimation(500, QtCore.QEasingCurve.OutQuad)

        #self.layout.setContentsMargins(0, 0, 0, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(20)

        self.curr_path = "/home/legoshi/"#os.path.expanduser('~')
        self.curr_files = os.listdir(self.curr_path)
        #sorted(self.curr_path)

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

        for i in self.curr_files:
            button = QDoubleButton(self)
            button.setText(i)
            try:
                ftype = magic.from_file(self.curr_path + i, mime=1)
                print(ftype)
                if(ftype in filetypes2icons):
                    button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons[ftype]))
                else:
                    if(ftype in image_types):

                        button.setIcon(QtGui.QIcon(self.curr_path + i))
                    elif(ftype == "application/pdf"):
                        pdffile = self.curr_path + i
                        doc = fitz.open(pdffile)
                        page = doc.load_page(0)  # number of page
                        pix = page.get_pixmap()
                        pix.save("tmp.png")
                        button.setIcon(QtGui.QIcon(QtGui.QIcon("./tmp.png")))
                        os.remove("./tmp.png")
                        doc.close()
                    else:
                        button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons["text/plain"]))

                button.double_clicked.connect(open_file(self.curr_path + i))
            except:
                button.setIcon(QtGui.QIcon.fromTheme("folder"))
                button.double_clicked.connect(lambda: open_folder(self.layout, self.curr_path + i, self))


            #fileInfo = QtCore.QFileInfo(self.curr_path + i)
            #print(fileInfo)
            #print(iconProvider)
            #icon = iconProvider.icon(fileInfo)
            #print(icon)
            #button.setIcon(icon)
            #button.setIcon(QtGui.QIcon.fromTheme("folder"))

            button.setIconSize(QtCore.QSize(50, 50))
            button.setFixedWidth(75)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet("QToolButton {padding-left : 5px; font-size: 16px;}")
            self.layout.addWidget(button)


        self.setCentralWidget(self.scroll)

        #ui = conf.UI()
        #ui.setUI()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    qdarktheme.setup_theme()

    app.setFont(QtGui.QFont("Ubuntu Mono"))

    lefiles = LeFiles()
    lefiles.resize(800, 600)
    lefiles.show()

    sys.exit(app.exec())
