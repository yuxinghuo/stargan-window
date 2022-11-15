from PyQt5 import QtGui
from PyQt5.Qt import *
import PyQt5.sip
import sys
import numpy as np
from numpy import *
import pandas as pd

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StarGan图像生成')
        self.resize(1000, 600)
        # 位置
        # self.move(300, 300)
# 模型选择
class ModelChoice_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 25)
        self.resize(75, 40)
        self.setText('选择模型：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)
class ModelChoice_Path(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(150, 25)
        self.resize(400, 40)
        self.setText('  请选择模型！')
        self.setStyleSheet('background-color:gray')
        self.setReadOnly(True)
        self.setDragEnabled(False)
# 参考图导入
class RefPic_Label(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 70)
        self.resize(75, 40)
        self.setText(' 选择参考图：')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)

class RefPic_Path(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(150, 70)
        self.resize(400, 40)
        self.setText('  请选择参考图片！')
        self.setStyleSheet('background-color:gray')
        self.setReadOnly(True)
        self.setDragEnabled(False)

class RefPic_Btn(QPushButton):
    path = ''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(600, 70)
        self.resize(60, 40)
        self.setText('浏览')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("浏览按钮按下")
        self.path, _ = QFileDialog.getOpenFileName(self, '请选择文件！', 'Excel Files (*.xlsx;*.xls)')
        # print(self.path)
        return super().mousePressEvent(evt)


class Btn_Predict(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(100, 108)
        self.resize(65, 35)
        self.setText('生成')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("预测按钮按下")
        return super().mousePressEvent(evt)

class Btn_Save(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(435, 108)
        self.resize(65, 35)
        self.setText('保存')
        self.setStyleSheet('background-color:gray')

    def mousePressEvent(self, evt):
        print("保存按钮按下")
        return super().mousePressEvent(evt)

class Label_ShowResult(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(50, 140)
        self.resize(100, 35)
        self.setText('实验结果显示')
        # self.setStyleSheet('background-color:gray')
        self.setAlignment(Qt.AlignCenter)

class LineEdit_Process(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(10, 558)
        self.resize(780, 26)
        self.setText(' 欢迎使用StarGan图像生成')
        # self.setStyleSheet('background-color:gray')
        self.setReadOnly(True)

class Table(QWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.move(30, 160)
        self.resize(540, 250)

        # self.model = QStandardItemModel(4, 4)
        # self.model.setHorizontalHeaderLabels(['1', '2', '3', '4'])
        # for row in range(4):
        #     for col in range(4):
        #         # print(data[row, col])
        #         self.model.setItem(row, col, QStandardItem(str(1)))
        # self.tableView = QTableView()
        # self.tableView.setModel(self.model)
        # layout = QVBoxLayout()
        # layout.addWidget(self.tableView)
        # self.setLayout(layout)


def load_dataset(path, postfix):
    if postfix == "csv":
        data = pd.read_csv(path, sep=',')
    elif postfix == "xlsx":
        data = pd.read_excel(path)
    x_data = data.iloc[:, 1:-1]
    y_data = data.iloc[:, -1:]
    x_key = x_data.keys().tolist()
    y_key = y_data.keys().tolist()
    return x_data, y_data, x_key, y_key

# 分类决策器决策结果
def stumpClassify(dataset, dimen, threshVal, threshIneq):
    resArray = ones(shape=(shape(dataset)[0], 1))
    if threshIneq == 'le':
        resArray[dataset[:, dimen] <= threshVal] = -1.0
    elif threshIneq == 're':
        resArray[dataset[:, dimen] > threshVal] = -1.0
    return resArray

def AdaboostClassify(x, y, weakClassArr):
    m = shape(x)[0]
    arrClassEst = mat(zeros(shape=(m, 1)))
    for i in range(len(weakClassArr)):
        resArray = stumpClassify(x, weakClassArr[i]['dimen'], weakClassArr[i]['threshVal'], weakClassArr[i]['threshIneq'])
        arrClassEst += weakClassArr[i]['alpha'] * resArray
    return arrClassEst

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    label_readdata = ModelChoice_Label(window)
    lineedit_path = ModelChoice_Path(window)
    label_readdata = ModelChoice_Label(window)
    lineedit_path = ModelChoice_Path(window)
    RefPic_Label(window)
    RefPic_Path(window)
    btn_scan = RefPic_Btn(window)
    btn_predict = Btn_Predict(window)
    btn_save = Btn_Save(window)
    label_showresult = Label_ShowResult(window)
    lineedit_process = LineEdit_Process(window)
    table_result = Table(window)

    def Path():
        global x_data, y_data, x_key, y_key, postfix
        path = btn_scan.path
        indx = path.rfind('.')
        postfix = path[indx+1:]
        if path == '':
            lineedit_process.setText('数据选择失败，请重新选择...')
            return
        lineedit_path.setText(path)
        x_data, y_data, x_key, y_key = load_dataset(btn_scan.path, postfix)
        lineedit_process.setText('数据加载完成...')
        # print(btn_scan.path)
    btn_scan.pressed.connect(Path)

    def Display(data, lst):
        if table_result.layout() is not None:
            PyQt5.sip.delete(table_result.layout())
        # if table_result.layout() is not None:
        #     print(table_result.layout().count())
        #     for i in range(table_result.layout().count()):
        #         # table_result.layout().removeItem(table_result.layout().itemAt(i))
        #         table_result.layout().removeWidget(table_result.layout().itemAt(i).widget())
        # if table_result.layout() is not None:
        #     print(table_result.layout().count())
        m, n = shape(data)
        table_result.model = QStandardItemModel(m, n)
        table_result.model.setHorizontalHeaderLabels(lst)
        for row in range(m):
            for col in range(n):
                # print(data[row, col])
                table_result.model.setItem(row, col, QStandardItem(str(data[row, col])))
        table_result.tableView = QTableView()
        table_result.tableView.setModel(table_result.model)
        layout = QVBoxLayout()
        layout.addWidget(table_result.tableView)
        table_result.setLayout(layout)

    def Load_DIC():
        global end_data, x_data, y_data, x_key, y_key, lst
        weakArray = np.load('./dataset/Adaboost/AKI_all_file.npy', allow_pickle=True)
        x_data = mat(x_data)
        y_data = mat(y_data)
        resArray = AdaboostClassify(x_data, y_data, weakArray)
        max_res = abs(resArray).max() + 0.01
        resArray = resArray / max_res
        resArray = np.around(resArray, decimals=5)
        end_data = np.append(x_data, y_data, axis=1)
        end_data = np.append(end_data, resArray, axis=1)
        lst = x_key + y_key + ['预测结果']
        Display(end_data, lst)
        lineedit_process.setText('数据已预测完成...')
    btn_predict.pressed.connect(Load_DIC)

    def save():
        global end_data, lst, postfix
        data = pd.DataFrame(end_data)
        if postfix == "csv":
            data.to_csv('./dataset/Adaboost/AKI_all_predict.csv', sep=',', header=lst)
        elif postfix == "xlsx":
            data.to_excel('./dataset/Adaboost/AKI_all_predict.xlsx', header=lst)
        lineedit_process.setText('预测结果已保存完成...')
    btn_save.pressed.connect(save)

    window.show()
    sys.exit(app.exec_())
