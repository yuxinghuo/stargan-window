import sys

from PyQt5 import QtGui

from element import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置对象名称
        self.setObjectName("MainWindow")
        # 设置窗口背景图片
        self.setStyleSheet("#MainWindow{border-image:url(image/background.jpg);}")
        self.setWindowTitle('StarGan图像生成')
        # self.resize(1000, 600)
        self.setGeometry(100, 100, 1000, 600)
        # self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    ModelChoice_Label(window)
    ModelChoice_Btn(window)

    InputPic_Label(window)
    InputPic_Btn(window)
    InputPic_Div(window)
    InputPic_Btn()
    RefPic_Label(window)
    RefPic_Btn(window)
    RefPic_Div(window)

    OutputPic_Label(window)
    OutputPic_Div(window)
    OutputPic_Btn(window)

    Generotor_Btn(window)
    # qt_view_close(window)
    # dialog = Dialog()
    # ui = Ui_Dialog()
    # ui.setupUi(dialog)
    # dialog.show()
    # main = SampleBar()
    # main.show()
    window.show()
    sys.exit(app.exec_())
