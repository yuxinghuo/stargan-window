import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import *

import shutil
from test import QClickableImage
# 模型选择
from core.generator import sample


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
        self.refLabel.setGeometry(50, 280, 75, 40)
        self.refLabel.setText(" 参考图片：")
        # 参考图模块--上传
        self.refButton = QPushButton(self)
        self.refButton.setGeometry(130, 286, 130, 30)
        self.refButton.setObjectName('refButton')
        self.refButton.setText('上传')
        # self.refButton.clicked.connect(self.onClickInputButton)
        self.refButton.clicked.connect(self.onClickRefButton)
        # 参考图模块--单选域
        self.radioButton_1 = QtWidgets.QRadioButton(self)
        self.radioButton_1.setGeometry(QtCore.QRect(50, 315, 89, 16))
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(150, 315, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self)
        self.radioButton_3.setGeometry(QtCore.QRect(250, 315, 89, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self)
        self.radioButton_4.setGeometry(QtCore.QRect(50, 335, 89, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self)
        self.radioButton_5.setGeometry(QtCore.QRect(150, 335, 89, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self)
        self.radioButton_6.setGeometry(QtCore.QRect(250, 335, 89, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        translate = QtCore.QCoreApplication.translate
        self.radioButton_1.setText(translate("Form", "female"))
        self.radioButton_2.setText(translate("Form", "male"))
        self.radioButton_3.setText(translate("Form", "cat"))
        self.radioButton_4.setText(translate("Form", "dog"))
        self.radioButton_5.setText(translate("Form", "wild"))
        self.radioButton_6.setText(translate("Form", "cartoon"))

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
        self.refGridLayout = QGridLayout(self.refScrollAreaWidgetContents)
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
        self.geneTextbox.move(500, 60)
        self.geneTextbox.resize(450, 500)
        # self.textbox.setFocusPolicy(Qt.NoFocus)
        self.geneTextbox.setFont(QFont("Arial", 20))
        self.geneTextbox.setText("    NOP:")
        # 创建滚动条
        self.geneScrollAreaImages = QScrollArea(self)
        self.geneScrollAreaImages.setWidgetResizable(True)
        self.geneScrollAreaWidgetContents = QWidget(self)
        self.geneScrollAreaWidgetContents.setObjectName('scrollAreaWidgetContentsRef')
        self.geneGridLayout = QGridLayout(self.geneScrollAreaWidgetContents)
        self.geneScrollAreaImages.setWidget(self.geneScrollAreaWidgetContents)
        self.geneScrollAreaImages.setGeometry(500, 60, 450, 500)
        self.geneVertocall = QVBoxLayout()
        self.geneVertocall.addWidget(self.geneScrollAreaImages)

        # 设置图片的预览尺寸；
        self.displayed_image_size = 150

    # 获取单选框的值
    def getValueRadioButton(self):
        domain = ''
        if self.radioButton_1.isChecked():
            domain = self.radioButton_1.text()
        elif self.radioButton_2.isChecked():
            domain = self.radioButton_2.text()
        elif self.radioButton_3.isChecked():
            domain = self.radioButton_3.text()
        elif self.radioButton_4.isChecked():
            domain = self.radioButton_4.text()
        elif self.radioButton_5.isChecked():
            domain = self.radioButton_5.text()
        elif self.radioButton_6.isChecked():
            domain = self.radioButton_6.text()
        return domain

    def onClickInputButton(self, evt):
        print("输入图片按钮")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'image Files (*.png;*.jpg)')
        shutil.copy(self.path, './src/img')
        self.input_img_viewer()
        # return super().mousePressEvent(evt)

    def onClickRefButton(self, evt):
        print("参考图片按钮")
        domain = self.getValueRadioButton()
        if domain=='':
            return QMessageBox.information(self, '错误', '参考图片未选择类型')
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'image Files (*.png;*.jpg)')
        if domain == 'female':
            file_path = './ref/celeba/female'
        elif domain == 'male':
            file_path = './ref/celeba/male'
        elif domain == 'cat':
            file_path = './ref/celeba/cat'
        elif domain == 'dog':
            file_path = './ref/celeba/dog'
        elif domain == 'wild':
            file_path = './ref/celeba/wild'
        else:
            file_path = './ref/cartoon'
        shutil.copy(self.path, file_path)
        print(self.path)
        self.ref_img_viewer(domain)
        # return super().mousePressEvent(evt)

    def onClickGeneButton(self, evt):
        print("生成图片中···")
        domain = self.getValueRadioButton()
        if domain=='':
            return QMessageBox.information(self, '错误', '参考图片未选择类型')
        self.status = self.statusBar()  # 实例化一个状态控件
        self.status.showMessage('生成图片中···', 5000)  # 设置存在时间为5秒
        sample(domain)
        self.gene_img_viewer()
        self.status = self.statusBar()  # 实例化一个状态控件
        self.status.showMessage('生成图片完成')  # 设置存在时间为5秒

    # 初始化滚动栏
    def clear_layout(self):
        for i in range(self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater()

    class QClickableImage(QWidget):
        image_id = ''

        def __init__(self, width=0, height=0, pixmap=None, image_id=''):
            QWidget.__init__(self)

            self.layout = QVBoxLayout(self)
            self.label1 = QLabel()
            self.label1.setObjectName('label1')
            self.lable2 = QLabel()
            self.lable2.setObjectName('label2')
            self.width = width
            self.height = height
            self.pixmap = pixmap

            if self.width and self.height:
                self.resize(self.width, self.height)
            if self.pixmap:
                pixmap = self.pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label1.setPixmap(pixmap)
                self.label1.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(self.label1)
            if image_id:
                self.image_id = image_id
                self.lable2.setText(image_id)
                self.lable2.setAlignment(Qt.AlignCenter)
                ###让文字自适应大小
                self.lable2.adjustSize()
                self.layout.addWidget(self.lable2)
            self.setLayout(self.layout)

        clicked = pyqtSignal(object)
        rightClicked = pyqtSignal(object)

        def mouseressevent(self, ev):
            print('55555555555555555')
            if ev.button() == Qt.RightButton:
                print('dasdasd')
                # 鼠标右击
                self.rightClicked.emit(self.image_id)
            else:
                self.clicked.emit(self.image_id)

        def imageId(self):
            return self.image_id
    # 输入图片预览
    def input_img_viewer(self):
        file_path = './src/img'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jepg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        if num != 0:
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = QClickableImage(self.displayed_image_size, self.displayed_image_size, pixmap,
                                                  image_id)
                self.inputGridLayout.addWidget(clickable_image, 1, i)
                # print(pixmap)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            # self.event(exit())

    # 参考图片预览
    def ref_img_viewer(self, domain):
        if domain == 'female':
            file_path = './ref/celeba/female'
        elif domain == 'male':
            file_path = './ref/celeba/male'
        elif domain == 'cat':
            file_path = './ref/celeba/cat'
        elif domain == 'dog':
            file_path = './ref/celeba/dog'
        elif domain == 'wild':
            file_path = './ref/celeba/wild'
        else:
            file_path = './ref/cartoon'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jepg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        if num != 0:
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = QClickableImage(self.displayed_image_size, self.displayed_image_size, pixmap,
                                                  image_id)
                self.refGridLayout.addWidget(clickable_image, 1, i)
                # print(pixmap)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            # self.event(exit())

    # 生成图片预览
    def gene_img_viewer(self):
        file_path = './result'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jepg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        displayed_image_size = 500
        if num != 0:
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = QClickableImage(displayed_image_size, displayed_image_size, pixmap,
                                                  image_id)
                self.geneGridLayout.addWidget(clickable_image, 1, i)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            # self.event(exit())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # QApplication.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon('image/icon.png'))  # 设置窗体图标
    main = MainApplication()
    main.show()
    app.exec_()
    del app
