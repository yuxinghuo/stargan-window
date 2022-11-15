import sys

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *


class MainApplication(QMainWindow):
    def __init__(self):
        super(MainApplication, self).__init__()
        # 设置对象名称
        self.setObjectName("MainWindow")

        # 菜单栏
        # self.menubar = QtWidgets.QMenuBar(self)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))
        # self.menubar.setObjectName("menubar")
        # self.setMenuBar(self.menubar)
        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(image/background.jpg);}")
        self.setWindowTitle('StarGan图像生成')
        self.setGeometry(100, 100, 1000, 600)
        # 屏幕居中
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕坐标系
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2  # Left居中处理
        newTop = (screen.height() - size.height()) / 2  # Top居中处理
        self.move(newLeft, newTop)


        # 输入模块--label
        self.inputLabel = QLabel(self)
        self.inputLabel.setObjectName("inputLabel")
        self.inputLabel.setGeometry(50, 10, 75, 40)
        self.inputLabel.setText(" 输入图片：")

        # 输入模块--上传
        self.inputButton = QPushButton(self)
        self.inputButton.setGeometry(130, 16, 130, 30)
        self.inputButton.setObjectName('inputButton')
        self.inputButton.setText('上传')
        self.inputButton.clicked.connect(self.onClickInputButton)
        # 输入模块--显示图像
        self.inputTextbox = QLineEdit(self)
        # 不显示QLineEdit的边缘，设置位置，字体样式，不可编辑
        self.inputTextbox.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.inputTextbox.move(50, 60)
        self.inputTextbox.resize(300, 200)
        # self.textbox.setFocusPolicy(Qt.NoFocus)
        self.inputTextbox.setFont(QFont("Arial", 20))
        self.inputTextbox.setText("    NOP:")
        # 创建滚动条
        self.inputScrollAreaImages = QScrollArea(self)
        self.inputScrollAreaImages.setWidgetResizable(True)
        self.inputScrollAreaWidgetContents = QWidget(self)
        self.inputScrollAreaWidgetContents.setObjectName('inputScrollAreaWidgetContents')
        self.inputGridLayout = QGridLayout(self.inputScrollAreaWidgetContents)
        self.inputScrollAreaImages.setWidget(self.inputScrollAreaWidgetContents)
        self.inputScrollAreaImages.setGeometry(50, 60, 300, 200)
        self.inputVertocall = QVBoxLayout()
        self.inputVertocall.addWidget(self.inputScrollAreaImages)



        # 参考图模块--label
        self.refLabel = QLabel(self)
        self.refLabel.setObjectName("refLabel")
        self.refLabel.setGeometry(50, 310, 75, 40)
        self.refLabel.setText(" 参考图片：")
        # 参考图模块--上传
        self.refButton = QPushButton(self)
        self.refButton.setGeometry(130, 316, 130, 30)
        self.refButton.setObjectName('refButton')
        self.refButton.setText('上传')
        self.refButton.clicked.connect(self.onClickInputButton)

        self.refTextbox = QLineEdit(self)
        # 不显示QLineEdit的边缘，设置位置，字体样式，不可编辑
        self.refTextbox.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.refTextbox.move(50, 360)
        self.refTextbox.resize(300, 200)
        # self.textbox.setFocusPolicy(Qt.NoFocus)
        self.refTextbox.setFont(QFont("Arial", 20))
        self.refTextbox.setText("    NOP:")
        # 创建滚动条
        self.refScrollAreaImages = QScrollArea(self)
        self.refScrollAreaImages.setWidgetResizable(True)
        self.refScrollAreaWidgetContents = QWidget(self)
        self.refScrollAreaWidgetContents.setObjectName('scrollAreaWidgetContentsRef')
        self.refgridLayout = QGridLayout(self.refScrollAreaWidgetContents)
        self.refScrollAreaImages.setWidget(self.refScrollAreaWidgetContents)
        self.refScrollAreaImages.setGeometry(50, 360, 300, 200)
        self.refVertocall = QVBoxLayout()
        self.refVertocall.addWidget(self.refScrollAreaImages)

        # 生成模块--label
        self.geneLabel = QLabel(self)
        self.geneLabel.setObjectName("geneLabel")
        self.geneLabel.setGeometry(500, 10, 75, 40)
        self.geneLabel.setText(" 生成图片：")
        # 生成模块--生成
        self.geneButton = QPushButton(self)
        self.geneButton.setGeometry(580, 16, 130, 30)
        self.geneButton.setObjectName('geneButton')
        self.geneButton.setText('生成')
        self.geneButton.clicked.connect(self.onClickGeneButton)

        # 生成模块--保存
        self.geneButtonSave = QPushButton(self)
        self.geneButtonSave.setGeometry(740, 16, 100, 32)
        self.geneButtonSave.setObjectName('geneButtonSave')
        self.geneButtonSave.setText('保存')

        self.geneTextbox = QLineEdit(self)
        # 不显示QLineEdit的边缘，设置位置，字体样式，不可编辑
        self.geneTextbox.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.geneTextbox.move(500,60)
        self.geneTextbox.resize(450, 500)
        # self.textbox.setFocusPolicy(Qt.NoFocus)
        self.geneTextbox.setFont(QFont("Arial", 20))
        self.geneTextbox.setText("    NOP:")
        # 创建滚动条
        self.geneScrollAreaImages = QScrollArea(self)
        self.geneScrollAreaImages.setWidgetResizable(True)
        self.geneScrollAreaWidgetContents = QWidget(self)
        self.geneScrollAreaWidgetContents.setObjectName('scrollAreaWidgetContentsRef')
        self.genegridLayout = QGridLayout(self.geneScrollAreaWidgetContents)
        self.geneScrollAreaImages.setWidget(self.geneScrollAreaWidgetContents)
        self.geneScrollAreaImages.setGeometry(500, 60, 450,500)
        self.geneVertocall = QVBoxLayout()
        self.geneVertocall.addWidget(self.geneScrollAreaImages)

    def onClickInputButton(self, evt):
        print("输入图片按钮")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.png;*.jpg)')
        return super().mousePressEvent(evt)

    def onClickGeneButton(self, evt):
        print("生成图片")
        self.status = self.statusBar()  # 实例化一个状态控件
        self.status.showMessage('生成图片中···', 5000)  # 设置存在时间为5秒



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('image/icon.png'))  # 设置窗体图标
    main = MainApplication()
    main.show()
    app.exec_()
    del app
