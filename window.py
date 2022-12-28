import os
import shutil
import sys

from PyQt5 import Qt
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication

from core.generator import sample


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("newStar.ui")
        # 上传源图片
        self.ui.uploadOriginalImg.clicked.connect(self.onClickInputButton)
        # 上传参考图片
        self.ui.uploadReferImg.clicked.connect(self.onClickRefButton)
        # 生出图片
        self.ui.generateResultImg.clicked.connect(self.onClickGeneButton)
        # 清除全部
        self.ui.clearAll.clicked.connect(self.onClickCleanButton)
        # logo
        self.ui.logoImg.setStyleSheet("border-image: url(image/background.png)");
        self.ui.setWindowTitle('StarGan图像生成')
        # 创建输入图片滚动条
        self.inputScrollAreaImages = QScrollArea(self.ui)
        self.inputScrollAreaImages.setWidgetResizable(True)
        self.inputScrollAreaWidgetContents = QWidget(self.ui)
        self.inputScrollAreaWidgetContents.setObjectName('inputScrollAreaWidgetContents')
        self.inputGridLayout = QGridLayout(self.inputScrollAreaWidgetContents)
        self.inputGridLayout.setAlignment(Qt.AlignLeft)
        self.inputScrollAreaImages.setWidget(self.inputScrollAreaWidgetContents)
        self.ui.inputBoxLayout.setAlignment(Qt.AlignLeft)
        self.ui.inputBoxLayout.addWidget(self.inputScrollAreaImages)
        # 创建参考图片位置滚动条
        self.refScrollAreaImages = QScrollArea(self.ui)
        self.refScrollAreaImages.setWidgetResizable(True)
        self.refScrollAreaWidgetContents = QWidget(self.ui)
        self.refScrollAreaWidgetContents.setObjectName('scrollAreaWidgetContentsRef')
        self.refGridLayout = QGridLayout(self.refScrollAreaWidgetContents)
        self.refGridLayout.setAlignment(Qt.AlignLeft)
        self.refScrollAreaImages.setWidget(self.refScrollAreaWidgetContents)
        self.ui.referBoxLayout.setAlignment(Qt.AlignLeft)
        self.ui.referBoxLayout.addWidget(self.refScrollAreaImages)
        # 创建生成图片滚动条
        self.geneScrollAreaImages = QScrollArea(self.ui)
        self.geneScrollAreaImages.setWidgetResizable(True)
        self.geneScrollAreaWidgetContents = QWidget(self.ui)
        self.geneScrollAreaWidgetContents.setObjectName('scrollAreaWidgetContentsRef')
        self.geneGridLayout = QGridLayout(self.geneScrollAreaWidgetContents)
        self.geneGridLayout.setAlignment(Qt.AlignLeft)
        self.geneScrollAreaImages.setWidget(self.geneScrollAreaWidgetContents)
        self.ui.geneBoxLayout.setAlignment(Qt.AlignLeft)
        self.ui.geneBoxLayout.addWidget(self.geneScrollAreaImages)
        # 设置图片的预览尺寸；
        self.displayed_image_size = 100
        # 初始化数据
        self.startLoad()

    # 初始化
    def startLoad(self):
        # 删除输入图片目录文件
        path_data = './src/img'
        for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = path_data + "/" + i  # 当前文件夹的下面的所有东西的绝对路径
            if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                os.remove(file_data)
        # 删除参考图片目录文件
        path_data = ['./ref/afhq/cat', './ref/afhq/dog', './ref/afhq/wild', './ref/celeba/female',
                     './ref/celeba/male',
                     './ref/cartoon/img']
        for j in path_data:
            for i in os.listdir(j):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
                file_data = j + "/" + i  # 当前文件夹的下面的所有东西的绝对路径
                if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                    os.remove(file_data)
        # 删除生成图片目录文件
        path_data = './result'
        for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = path_data + "/" + i  # 当前文件夹的下面的所有东西的绝对路径
            if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                os.remove(file_data)
        # 清除参考照片
        for i in range(self.refGridLayout.count()):
            self.refGridLayout.itemAt(i).widget().deleteLater()
        # 清除输入照片
        for i in range(self.inputGridLayout.count()):
            self.inputGridLayout.itemAt(i).widget().deleteLater()
        # 清除生成照片
        for i in range(self.geneGridLayout.count()):
            self.geneGridLayout.itemAt(i).widget().deleteLater()

    # 获取单选框的值
    def getValueRadioButton(self):
        domain = ''
        if self.ui.cat.isChecked():
            domain = 'cat'
        elif self.ui.dog.isChecked():
            domain = 'dog'
        elif self.ui.wild.isChecked():
            domain = 'wild'
        elif self.ui.female.isChecked():
            domain = 'female'
        elif self.ui.male.isChecked():
            domain = 'male'
        elif self.ui.cartoon.isChecked():
            domain = 'cartoon'
        return domain

    class QClickableImage(QWidget):
        image_id = ''

        def __init__(self, width=0, height=0, pixmap=None, image_id=''):
            QWidget.__init__(self)
            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignLeft)
            self.label1 = QLabel()
            self.label1.setObjectName('label1')
            self.width = width
            self.height = height
            self.pixmap = pixmap
            if self.width and self.height:
                self.resize(self.width, self.height)
            if self.pixmap:
                pixmap = self.pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label1.setPixmap(pixmap)
                self.label1.setAlignment(Qt.AlignLeft)
                self.layout.addWidget(self.label1)
            if image_id:
                self.image_id = image_id
            self.setLayout(self.layout)

        def imageId(self):
            return self.image_id

    # 输入图片上传
    def onClickInputButton(self):
        print("输入图片按钮")
        self.ui.path, _ = QFileDialog.getOpenFileName(self.ui, '请选择文件！', 'image Files (*.png;*.jpg;*.jepg)')
        if self.ui.path == '':
            return
        shutil.copy(self.ui.path, './src/img')
        self.input_img_viewer()
        QMessageBox.information(self.ui, '上传图片', '上传图片成功')

    # 清除按钮
    def onClickCleanButton(self):
        self.startLoad()
        QMessageBox.information(self.ui, '清除数据', '清除数据成功')

    # 参考图片上传
    def onClickRefButton(self):
        print("参考图片按钮")
        domain = self.getValueRadioButton()
        if domain == '':
            return QMessageBox.information(self.ui, '错误', '参考图片未选择类型')
        self.path, _ = QFileDialog.getOpenFileName(self.ui, '请选择文件！', 'image Files (*.png;*.jpg)')
        if self.path == '':
            return
        if domain == 'female':
            file_path = './ref/celeba/female'
        elif domain == 'male':
            file_path = './ref/celeba/male'
        elif domain == 'cat':
            file_path = './ref/afhq/cat'
        elif domain == 'dog':
            file_path = './ref/afhq/dog'
        elif domain == 'wild':
            file_path = './ref/afhq/wild'
        else:
            file_path = './ref/cartoon/img'
        shutil.copy(self.path, file_path)
        print(self.path)
        self.ref_img_viewer(domain)
        QMessageBox.information(self.ui, '上传图片', '上传图片成功')

    # 生成图片方法
    def onClickGeneButton(self):
        # 清除图片
        print("生成图片中···")
        domain = self.getValueRadioButton()
        if domain == '':
            return QMessageBox.information(self, '错误', '参考图片未选择类型')
        # 判断输入图片和参考图片是否都上传
        srcPath = './src/img'
        if len(os.listdir(srcPath)) == 0:
            return QMessageBox.information(self, '生成图片', '输入图片未上传，生成图片失败！')
        if domain == 'female':
            srcPath = './ref/celeba/female'
        elif domain == 'male':
            srcPath = './ref/celeba/male'
        elif domain == 'cat':
            srcPath = './ref/afhq/cat'
        elif domain == 'dog':
            srcPath = './ref/afhq/dog'
        elif domain == 'wild':
            srcPath = './ref/afhq/wild'
        else:
            srcPath = './ref/cartoon/img'
        if len(os.listdir(srcPath)) == 0:
            return QMessageBox.information(self, '生成图片', '选择类型中参考图片未上传，生成图片失败！')
        self.ui.statusbar.showMessage('生成图片中···', 5000)  # 设置存在时间为5秒
        sample(domain)
        self.gene_img_viewer()
        self.ui.statusbar.showMessage('生成图片完成')  # 设置存在时间为5秒
        QMessageBox.information(self.ui, '生成图片', '生成图片成功')

    # 输入图片预览
    def input_img_viewer(self):
        file_path = './src/img'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jpeg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        if num != 0:
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = self.QClickableImage(self.displayed_image_size, self.displayed_image_size, pixmap,
                                                       image_id)
                self.inputGridLayout.addWidget(clickable_image, 1, i)
                # print(pixmap)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            return

    # 参考图片预览
    def ref_img_viewer(self, domain):
        if domain == 'female':
            file_path = './ref/celeba/female'
        elif domain == 'male':
            file_path = './ref/celeba/male'
        elif domain == 'cat':
            file_path = './ref/afhq/cat'
        elif domain == 'dog':
            file_path = './ref/afhq/dog'
        elif domain == 'wild':
            file_path = './ref/afhq/wild'
        else:
            file_path = './ref/cartoon/img'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jpeg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        if num != 0:
            row = num
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = self.QClickableImage(self.displayed_image_size, self.displayed_image_size, pixmap,
                                                       image_id)
                self.refGridLayout.addWidget(clickable_image, i, 1)
                # print(pixmap)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            return

    # 生成图片预览
    def gene_img_viewer(self):
        # 清除生成照片
        for i in range(self.geneGridLayout.count()):
            self.geneGridLayout.itemAt(i).widget().deleteLater()
        file_path = './result'
        print('file_path为{}'.format(file_path))
        img_type = ('.jpg', '.png', '.jpeg')
        png_list = list(i for i in os.listdir(file_path) if str(i).endswith(img_type))
        print(png_list)
        num = len(png_list)
        displayed_image_size = 500
        if num != 0:
            for i in range(num):
                image_id = str(file_path + '/' + png_list[i])
                print(image_id)
                pixmap = QPixmap(image_id)
                clickable_image = self.QClickableImage(displayed_image_size, displayed_image_size, pixmap,
                                                       image_id)
                self.geneGridLayout.addWidget(clickable_image, 1, i)
                QApplication.processEvents()
        else:
            QMessageBox.warning(self, '错误', '生成图片文件为空')
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建QApplication对象，作为GUI主程序入口
    app.setWindowIcon(QIcon('image/icon.png'))  # 设置窗体图标
    stats = Stats()
    stats.ui.show()  # 显示主窗体
    sys.exit(app.exec_())  # 循环中等待退出程序
