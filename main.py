import sys

import qdarktheme
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets  as qfw
import os
import magic
import fitz
import src.widgets as c_widgets

import subprocess as sb

class NewFolderDialog(QtWidgets.QMainWindow):
    def __init__(self, parent = None, layout = None, path = None):
        super().__init__()
        self.parent = parent
        self.layout = layout
        self.path = path

        self.main_group = QtWidgets.QGroupBox(self)
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.main_group.setLayout(self.main_vbox)

        self.folder_name_line_edit = QtWidgets.QLineEdit(text = "New Folder")

        self.cancel_create_group = QtWidgets.QGroupBox()
        self.cancel_create_hbox = QtWidgets.QHBoxLayout()

        self.cancel_button = QtWidgets.QPushButton(text = "Cancel")
        self.cancel_button.clicked.connect(lambda: self.hide())

        self.create_button = QtWidgets.QPushButton(text = "Create")
        self.create_button.clicked.connect(self.CreateFolder)

        self.cancel_create_hbox.addWidget(self.cancel_button)
        self.cancel_create_hbox.addWidget(self.create_button)

        self.cancel_create_group.setLayout(self.cancel_create_hbox)

        self.main_vbox.addWidget(self.folder_name_line_edit)
        self.main_vbox.addWidget(self.cancel_create_group)

        self.setCentralWidget(self.main_group)
        self.show()


    def CreateFolder(self):
        sb.call(["mkdir", self.path + "/" + self.folder_name_line_edit.text()])
        self.parent.open_folder_func(self.layout, self.path[:-1])

        self.hide()

class RenameDialog(QtWidgets.QMainWindow):
    def __init__(self, parent = None, layout = None, path = None, current_name = None):
        super().__init__()
        self.parent = parent
        self.layout = layout
        self.path = path
        self.current_name = current_name

        #self.path = ""

        self.main_group = QtWidgets.QGroupBox(self)
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.main_group.setLayout(self.main_vbox)

        self.name_line_edit = QtWidgets.QLineEdit(text = self.current_name)

        self.cancel_rename_group = QtWidgets.QGroupBox()
        self.cancel_rename_hbox = QtWidgets.QHBoxLayout()

        self.cancel_button = QtWidgets.QPushButton(text = "Cancel")
        self.cancel_button.clicked.connect(lambda: self.hide())

        self.rename_button = QtWidgets.QPushButton(text = "Rename")
        self.rename_button.clicked.connect(self.rename)

        self.cancel_rename_hbox.addWidget(self.cancel_button)
        self.cancel_rename_hbox.addWidget(self.rename_button)

        self.cancel_rename_group.setLayout(self.cancel_rename_hbox)

        self.main_vbox.addWidget(self.name_line_edit)
        self.main_vbox.addWidget(self.cancel_rename_group)

        self.setCentralWidget(self.main_group)
        self.show()

    def setPath(self, path):
        self.path = path

    def rename(self):
        print(self.path + "/" + self.current_name)
        sb.call(["mv", self.path + "/" + self.current_name, self.path + "/" + self.name_line_edit.text()])
        self.parent.open_folder_func(self.layout, self.path[:-1])

        self.hide()

class RemoveDialog(QtWidgets.QMainWindow):
    def __init__(self, parent = None, layout = None, path = None, current_name = None):
        super().__init__()
        self.parent = parent
        self.layout = layout
        self.path = path
        self.current_name = current_name

        #self.path = ""

        self.main_group = QtWidgets.QGroupBox(self)
        self.main_vbox = QtWidgets.QVBoxLayout()
        self.main_group.setLayout(self.main_vbox)

        self.label = QtWidgets.QLabel(text = "Are you sure to remove \"" + self.current_name + "\"?\nYou can't restore file after removing.")

        self.cancel_remove_group = QtWidgets.QGroupBox()
        self.cancel_remove_hbox = QtWidgets.QHBoxLayout()

        self.cancel_button = QtWidgets.QPushButton(text = "Cancel")
        self.cancel_button.clicked.connect(lambda: self.hide())

        self.remove_button = QtWidgets.QPushButton(text = "Remove")
        self.remove_button.clicked.connect(self.remove)

        self.cancel_remove_hbox.addWidget(self.cancel_button)
        self.cancel_remove_hbox.addWidget(self.remove_button)

        self.cancel_remove_group.setLayout(self.cancel_remove_hbox)

        self.main_vbox.addWidget(self.label)
        self.main_vbox.addWidget(self.cancel_remove_group)

        self.setCentralWidget(self.main_group)
        self.show()

    def setPath(self, path):
        self.path = path

    def remove(self):
        #print(self.path + "/" + self.current_name)
        sb.call(["rm", "-r", self.path + "/" + self.current_name])
        self.parent.open_folder_func(self.layout, self.path[:-1])

        self.hide()

class LeFlowWidget(QtWidgets.QWidget):

    right_clicked = QtCore.Signal()

    def __init__(self, parent=None, needAni=False, isTight=False):
        #super(LeFlowLayout, self).__init__(parent, needAni, isTight)
        super().__init__()
        self.layout = qfw.FlowLayout(self, needAni = needAni, isTight = isTight)

        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.x = 0
        self.y = 0
        #self.widgetEvent(QtCore.QEvent())

    def takeAllWidgets(self):
        self.layout.takeAllWidgets()

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def eventFilter(self, obj, event):
        #print(333)
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() != QtCore.Qt.LeftButton:
                tmp = QtGui.QCursor.pos().toPointF()
                self.x = tmp.x()
                self.y = tmp.y()
                self.right_clicked.emit()

                return 1
        return 0

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

        self.x = 0
        self.y = 0

        self.setMouseTracking(True)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() != QtCore.Qt.LeftButton and event.button() != QtCore.QEvent.MouseButtonDblClick:
                tmp = QtGui.QCursor.pos().toPointF()
                self.x = tmp.x()
                self.y = tmp.y()
                self.right_clicked.emit()
                return 1
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == QtCore.Qt.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
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


class LeFiles(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.active_folder_path = os.path.expanduser('~')
        print(self.active_folder_path)
        self.forward_folder_path = self.active_folder_path

        self.setWindowTitle("LeFiles")
        QtGui.QIcon.setThemeName("candy-icons")

        self.main_group_widget = QtWidgets.QGroupBox()
        self.main_group_widget.setContentsMargins(0,0,0,0)
        self.main_group_widget.setStyleSheet("QGroupBox {border: 0px;}")


        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(0,0,0,0)

        #self.mygroupbox = QtWidgets.QGroupBox()


        self.main_group_widget.setLayout(self.vbox)

        self.leflow = LeFlowWidget(needAni=True)
        self.leflow.right_clicked.connect(self.folder_menu)

        #self.layout = self.mygroupbox

        #self.mygroupbox.setLayout(self.layout)
        #self.mygroupbox.setContentsMargins(0,0,0,0)

        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setContentsMargins(0,0,0,0)
        self.scroll.setWidget(self.leflow)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea {border: 0px;}")


        self.active_area_group = QtWidgets.QGroupBox()

        self.fast_activities_list_widget = c_widgets.SideBar(self, item_size = 35, item_icon_size = 35, font_size = 14, show_menu_button = 0)
        self.fast_activities_list_widget.setMinimumWidth(35)
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("user-home"), "test", self.open_folder(self.leflow, os.path.expanduser('~')))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("user-desktop-symbolic"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Desktop"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("folder-documents-symbolic"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Documents"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("folder-downloads"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Downloads"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("folder-music"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Music"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("folder-pictures"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Pictures"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("folder-videos"), "test", self.open_folder(self.leflow, os.path.expanduser('~') + "/Videos"))
        self.fast_activities_list_widget.addButton(QtGui.QIcon.fromTheme("user-trash-full"), "test", None)


        #self.active_area_group = QtWidgets.QGroupBox()

        self.active_area_hbox = QtWidgets.QHBoxLayout()
        self.active_area_hbox.setContentsMargins(0,0,0,0)
        self.active_area_hbox.addWidget(self.fast_activities_list_widget)
        self.active_area_hbox.addWidget(self.scroll)

        self.active_area_group.setLayout(self.active_area_hbox)




        self.back_folder_button = QtWidgets.QToolButton()
        self.back_folder_button.setText("<")
        self.back_folder_button.setStyleSheet("QToolButton {font-size: 25px;}")
        self.back_folder_button.setFixedWidth(30)
        self.back_folder_button.setFixedHeight(30)
        self.back_folder_button.clicked.connect(self.go_to_back_folder_path)

        self.forward_folder_button = QtWidgets.QToolButton()
        self.forward_folder_button.setText(">")
        self.forward_folder_button.setStyleSheet("QToolButton {font-size: 25px;}")
        self.forward_folder_button.setFixedWidth(30)
        self.forward_folder_button.setFixedHeight(30)
        self.forward_folder_button.clicked.connect(self.go_to_forward_folder)

        self.input_path = QtWidgets.QLineEdit()
        self.input_path.setText(self.active_folder_path)

        self.go_to_button = QtWidgets.QToolButton()
        self.go_to_button.setText("⊚")
        self.go_to_button.setStyleSheet("QToolButton {font-size: 25px;}")
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
        self.vbox.addWidget(self.active_area_group)

        #self.layout.setAnimation(250, QtCore.QEasingCurve.OutQuad)


        self.open_folder_func(self.leflow, self.active_folder_path)
        self.setCentralWidget(self.main_group_widget)

        #ui = conf.UI()
        #ui.setUI()

    def go_to_line_folder(self):
        text = self.input_path.text()
        if(text[-1] == "/"):
            self.open_folder_func(self.leflow, text[:-1])
        else:
            self.open_folder_func(self.leflow, text)

    def go_to_forward_folder(self):
        print("forward")
        print(self.forward_folder_path)
        #if(self.forward_folder_path == self.active_folder_path):
            #self.forward_folder_path =
        self.open_folder_func(self.leflow, self.forward_folder_path)

    def go_to_back_folder_path(self):
        #print(self.active_folder_path)
        self.forward_folder_path = self.active_folder_path[:-1]
        tmp = self.active_folder_path.split("/")
        new_path = "/"
        for i in range(1, len(tmp) - 2):
            new_path += tmp[i] + "/"
        self.open_folder_func(self.leflow, new_path[:-1])

    def open_file(self, *args):
        return lambda: sb.call(("xdg-open", *args))

    def open_folder_func(self, layout, path):
        #print(path + "1234123")
        self.active_folder_path = path + "/"
        self.input_path.setText(self.active_folder_path)
        print(self.active_folder_path)
        curr_files = os.listdir(self.active_folder_path)
        curr_files.sort()
        #print(curr_files)

        layout.takeAllWidgets()
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
            fileInfo = QtCore.QFileInfo(self.active_folder_path + i)
            #print(fileInfo.suffix())
            ftype = fileInfo.suffix()#magic.from_file(active_folder_path + i, mime=1)
            #print(i)
            #print(ftype)
            flag = 1
            if(ftype in filetypes2icons):
                button.setIcon(QtGui.QIcon.fromTheme(filetypes2icons[ftype]))
                flag = 0
            else:
                if(ftype in image_types):
                    button.setIcon(QtGui.QIcon(self.active_folder_path + i))
                    flag = 0
                elif(ftype == "pdf"):
                    pdffile = self.active_folder_path + i
                    doc = fitz.open(pdffile)
                    page = doc.load_page(0)  # number of page
                    pix = page.get_pixmap()
                    pix.save("tmp.png")
                    button.setIcon(QtGui.QIcon("./tmp.png"))
                    os.remove("./tmp.png")
                    doc.close()
                    flag = 0
            if(not flag):
                button.double_clicked.connect(self.open_file(self.active_folder_path + i))
            if(fileInfo.isDir() and flag):
                button.setIcon(QtGui.QIcon.fromTheme("folder"))
                button.double_clicked.connect(self.open_folder(layout, self.active_folder_path + i))
            elif flag:
                button.setIcon(QtGui.QIcon("custom_icons/question-mark.svg"))
                button.double_clicked.connect(self.open_file(self.active_folder_path + i))
            button.right_clicked.connect(self.file_menu_glitch(button))
            button.setIconSize(QtCore.QSize(50, 50))
            button.setFixedWidth(75)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet("QToolButton {padding-left : 5px; font-size: 16px; border-radius: 10px;}")
            layout.addWidget(button)

    def open_folder(self, layout, path):
        #print(path)
        return lambda: self.open_folder_func(layout, path)

    def folder_menu(self):
        qmenu = QtWidgets.QMenu(self)

        new_folder_action = QtGui.QAction()
        new_folder_action.setText("New Folder")
        new_folder_action.triggered.connect(self.create_folder)


        open_in_terminal = QtGui.QAction()
        open_in_terminal.setText("Open in terminal")

        qmenu.addAction(new_folder_action)
        qmenu.addAction(open_in_terminal)

        qmenu.move(self.leflow.x, self.leflow.y)
        qmenu.exec()

    def create_folder(self):
        new_folder_dialog = NewFolderDialog(parent = self, layout = self.leflow, path = self.active_folder_path)

    def file_menu(self, button):

        #print(button.text())
        qmenu = QtWidgets.QMenu(self)
        # qmenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # qmenu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # qmenu.setStyleSheet("""QMenu{radius: 10px;}""")

        rename_action = QtGui.QAction()
        rename_action.setText("Rename")
        rename_action.triggered.connect(lambda: self.rename(button))

        remove_action = QtGui.QAction()
        remove_action.setText("Remove")
        remove_action.triggered.connect(lambda: self.remove(button))

        qmenu.addAction(rename_action)
        qmenu.addAction(remove_action)

        qmenu.move(button.x, button.y)
        qmenu.exec()

    def file_menu_glitch(self, button):
        return lambda: self.file_menu(button)

    def rename(self, button):
        rename_dialog = RenameDialog(parent = self, layout = self.leflow, path =self.active_folder_path, current_name = button.text())

    def remove(self, button):
        remove_dialog = RemoveDialog(parent = self, layout = self.leflow, path = self.active_folder_path, current_name = button.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])


    qdarktheme.setup_theme()

    app.setFont(QtGui.QFont("Ubuntu Mono"))

    lefiles = LeFiles()
    lefiles.resize(800, 600)
    lefiles.show()

    sys.exit(app.exec())
