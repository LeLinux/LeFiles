# import sys

# import qdarktheme
# from PySide6 import QtWidgets, QtGui, QtCore
# import qfluentwidgets  as qfw
# import os
# import magic
# import fitz

# import subprocess as sb

# class OnlyIcons(QtWidgets.QWidget):
#     def __init__(self, parent = None, item_size = None, item_icon_size = None):
#         super().__init__(parent = parent)
#         self.item_size = item_size
#         se lf.item_icon_size = item_icon_size
#         self.current_start_y = 0

#     def addButton(self, icon = None, function = None):
#         button = QtWidgets.QToolButton(self)
#         button.setIcon(icon)
#         button.setIconSize(QtCore.QSize(self.item_icon_size, self.item_icon_size))
#         button.setFixedSize(QtCore.QSize(self.item_size, self.item_size))
#         button.move(0, self.current_start_y)
#         button.clicked.connect(function)

#         self.current_start_y += self.item_size

# class IconsWithText(QtWidgets.QWidget):
#     def __init__(self, parent = None, item_width = None, item_height = None, item_icon_size = None, font_size = None):
#         super().__init__(parent = parent)
#         self.item_height = item_height
#         self.item_size = QtCore.QSize(item_width, item_height)
#         self.item_icon_size = item_icon_size
#         self.font_size = font_size
#         self.current_start_y = 0

#     def addButton(self, icon = None, text = "", function = None):
#         button = QtWidgets.QToolButton(self)
#         button.setText(text)
#         button.setIcon(icon)
#         button.setIconSize(QtCore.QSize(self.item_icon_size, self.item_icon_size))
#         button.setFixedSize(self.item_size)
#         button.move(0, self.current_start_y)
#         self.current_start_y += self.item_height
#         button.clicked.connect(function)
#         button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
#         button.setStyleSheet("""QPushButton{font-size: """ + str(self.font_size) + """px; padding: 50px;}""")

# class SideBar(QtWidgets.QWidget):
#     def __init__(self, parent = None, item_active_width = None, item_size = None, item_icon_size = None, font_size = None, show_menu_button = 1):
#         super().__init__(parent = parent)
#         self.only_icons = OnlyIcons(self, item_size, item_icon_size)
#         self.icons_with_text = None
#         self.currentMode = 0
#         if show_menu_button:
#             self.icons_with_text = IconsWithText(self, item_active_width, item_size, item_icon_size, font_size)
#             self.icons_with_text.hide()
#             self.addButton(QtGui.QIcon("./custom_icons/menu.svg"), "", lambda:self.switchMode())

#         #self.setStyleSheet("QPushButton{}")


#     def addButton(self, icon = None, text = "", function = None):
#         self.only_icons.addButton(icon, function)
#         try:
#             self.icons_with_text.addButton(icon, text, function)
#         except:
#             pass

#     def switchMode(self):
#         if self.currentMode:
#             self.icons_with_text.hide()
#             self.only_icons.show()
#         else:
#             self.icons_with_text.show()
#             self.only_icons.hide()
#         self.currentMode = not self.currentMode

# # class Window(QtWidgets.QMainWindow):
# #     def __init__(self):
# #         super().__init__()

# #         QtGui.QIcon.setThemeName("candy-icons")

# #         self.test = SideBar(self, item_active_width = 200, item_size = 100, item_icon_size = 50, font_size = 20, show_menu_button = 1)
# #         #self.test.setFixedSize(QtCore.QSize(300, 300))
# #         self.test.addButton(QtGui.QIcon.fromTheme("user-home"), "test", lambda: print(1))
# #         self.test.addButton(QtGui.QIcon.fromTheme("user-home"), "test", lambda: print(2))
# #         self.setCentralWidget(self.test)


# # if __name__ == '__main__':
# #     app = QtWidgets.QApplication([])
# #     w = Window()
# #     w.show()
# #     sys.exit(app.exec())


import sys

import qdarktheme
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets  as qfw
import os
import magic
import fitz

import subprocess as sb



class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.test_b = QtWidgets.QToolButton(self)
        self.test_b.clicked.connect(self.contextMenuEvent)

        # self.test = QtWidgets.QMenu(self)
        # self.test_acti = self.test.addAction("test")
        #self.test.exec()

    def contextMenuEvent(self):
        self.cursor = QtGui.QCursor.pos()
        print(self.cursor.x())
        self.test = QtWidgets.QMenu(self)
        self.test_acti = self.test.addAction("test")
        self.test.move(self.cursor.x(), self.cursor.y())
        self.test.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = Window()
    w.show()
    sys.exit(app.exec())