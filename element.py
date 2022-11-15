from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.Qt import *


# 模型选择
from core.generator import sample


class ModelChoice_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(380, 200)
        self.resize(75, 40)
        self.setText('选择模型：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)


class ModelChoice_Btn(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(380, 250)
        self.resize(75, 40)
        self.setText('选择模型')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)


# 输入图片导入
class InputPic_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 20)
        self.resize(75, 40)
        self.setText(' 输入图片：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)


class InputPic_Btn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(130, 20)
        self.resize(75, 40)
        self.setText('浏览')
        self.setStyleSheet("QPushButton{background:orange;color:white;box-shadow: 1px 1px 3px;font-size:16px;border-radius: 24px;font-family: 微软雅黑;}\n"
                                      "QPushButton:pressed{\n"
                                      "    background:black;\n"
                                      "}")


    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'image Files (*.jpg;*.jpeg;*.png)')

        return super().mousePressEvent(evt)

class qt_view(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(500, 500)
        self.resize(600, 250)
        self.setWindowTitle("圆点选择")
        self.radioButton_1 = QtWidgets.QRadioButton(self)
        self.radioButton_1.setGeometry(QtCore.QRect(230, 100, 89, 16))
        self.radioButton_1.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(310, 100, 89, 16))
        self.radioButton_2.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_2.setObjectName("radioButton_2")
        translate = QtCore.QCoreApplication.translate
        self.radioButton_1.setText(translate("Form", "选项1"))
        self.radioButton_2.setText(translate("Form", "选项2"))

class InputPic_Div(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 70)
        self.resize(300, 200)
        self.setText('浏览')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.png;*.jpg)')
        # print(self.path)
        return super().mousePressEvent(evt)


# 参考图导入
class RefPic_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 320)
        self.resize(75, 40)
        self.setText(' 参考图片：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)


class RefPic_Btn(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(130, 320)
        self.resize(75, 40)
        self.setText('浏览')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)


class RefPic_Div(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 370)
        self.resize(300, 200)
        self.setText('浏览')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)


# 生成图片
class OutputPic_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(500, 20)
        self.resize(75, 40)
        self.setText(' 生成图片：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)


class OutputPic_Div(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(500, 70)
        self.resize(450, 400)
        self.setText('浏览')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)

class Generotor_Btn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(435, 108)
        self.resize(65, 35)
        self.setText('生成')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("生成图像中...")
        sample()
        print("生成图像成功！")
        return

class OutputPic_Btn(QPushButton):
    path = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(500, 500)
        self.resize(75, 40)
        self.setText('保存图片')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)


class qt_view(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.move(500, 500)
        self.resize(600, 250)
        self.setWindowTitle("圆点选择")
        self.radioButton_1 = QtWidgets.QRadioButton(self)
        self.radioButton_1.setGeometry(QtCore.QRect(230, 100, 89, 16))
        self.radioButton_1.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(310, 100, 89, 16))
        self.radioButton_2.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_2.setObjectName("radioButton_2")
        translate = QtCore.QCoreApplication.translate
        self.radioButton_1.setText(translate("Form", "选项1"))
        self.radioButton_2.setText(translate("Form", "选项2"))

# 圆灰按钮
class qt_view_btn(QWidget):
    def __init__(self):
        super(qt_view, self).__init__()
        self.resize(600, 250)
        self.setWindowTitle("圆灰按钮")

        button_open_img = QPushButton(self)
        button_open_img.setText("打开图片")
        button_open_img.move(250, 100)
        button_open_img.setFixedSize(150, 50)
        button_open_img.setStyleSheet("QPushButton{\n"
                                      "    background:orange;\n"
                                      "    color:white;\n"
                                      "    box-shadow: 1px 1px 3px;font-size:18px;border-radius: 24px;font-family: 微软雅黑;\n"
                                      "}\n"
                                      "QPushButton:pressed{\n"
                                      "    background:black;\n"
                                      "}")

# 关闭弹窗
class qt_view_close(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("关闭弹窗")
        result = QMessageBox.question(self, "注意!", "您真的要关闭吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            QMessageBox.information(self, "消息", "谢谢使用！")
            quit()
        else:
            QMessageBox.information(self, "消息", "正在返回...")
            quit()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 320)


class Dialog(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# 下拉框
class ComboxDemo(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('下拉列表框')
        self.resize(700, 400)

        # 实例化QComBox对象
        self.cb = QComboBox(self)
        self.cb.move(100, 20)

        # 单个添加条目
        self.cb.addItem('选项1')
        self.cb.addItem('选项2')
        # 多个添加条目
        self.cb.addItems(['选项3', '选项4', '选项5'])

        self.cb.currentIndexChanged[str].connect(self.print_value)

    def print_value(self, value):
        print(value)
# 进度条
class SampleBar(QMainWindow):
    def __init__(self, parent=None):
        super(SampleBar, self).__init__(parent)
        self.setMinimumSize(400, 100)
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('QStatusBar::item {border: none;}')
        self.setStatusBar(self.statusBar)
        self.progressBar = QProgressBar()
        self.label = QLabel()
        self.label.setText("加载中，请稍后... ")
        self.statusBar.addPermanentWidget(self.label, stretch=2)
        self.statusBar.addPermanentWidget(self.progressBar, stretch=4)
        self.progressBar.setRange(0, 100)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
