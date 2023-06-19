import sys

import qdarktheme
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets
import os
import magic


class LeFiles(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LeFiles")
        QtGui.QIcon.setThemeName("candy-icons")

        self.mygroupbox = QtWidgets.QGroupBox()



        self.layout = qfluentwidgets.FlowLayout(needAni=True)

        self.mygroupbox.setLayout(self.layout)

        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)



        self.layout.setAnimation(500, QtCore.QEasingCurve.OutQuad)

        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(20)

        self.curr_path = os.path.expanduser('~') + "/Downloads/"
        self.curr_files = os.listdir(self.curr_path)
        sorted(self.curr_path)


        for i in self.curr_files:
            button = QtWidgets.QToolButton(self)
            button.setText(i)
            # ftype = magic.from_file(os.path.expanduser('~') + "/Downloads/" + i, mime=1)
            # if ftype == "application/zip":
            #     button.setIcon(QtGui.QIcon.fromTheme("file-archiver"))
            fileInfo = QtCore.QFileInfo(self.curr_path + i)
            print(fileInfo)
            iconProvider = QtWidgets.QFileIconProvider()
            print(iconProvider)
            icon = iconProvider.icon(fileInfo)
            print(icon)
            button.setIcon(icon)
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
