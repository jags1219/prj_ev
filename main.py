#!/usr/bin/env python
# from PyQt4 import QtGui, QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QEvent
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QPlainTextEdit, QMainWindow)
import json


class WidgetGallery(QWidget):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.answer = ""
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use SP")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)

        disableWidgetsCheckBox.toggled.connect(
            self.topRightGroupBox.setDisabled)

        disableWidgetsCheckBox.toggled.connect(
            self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topRightGroupBox, 1, 0, 1, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 0, 1, 0)

        mainLayout.setRowStretch(1, 0)

        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("EagleVoice")
        self.changeStyle('Windows')

        with open('result.json', 'r') as fp:
            self.ques_dict = json.load(fp)

        self.ques_lst = []
        self.answer = []
        # self.master_lst = []
        style = '''
        QWidget {
        background-color: coral;
        }

        QPushButton {
        background-color: #006325;
        font-size: 20px;
        color: white;

        min-width:  100px;
        max-width:  100px;
        min-height: 100px;
        max-height: 100px;

        border-radius: 50px;        
        border-width: 1px;
        border-color: #ae32a0;
        border-style: solid;
        }
        QPushButton:hover {
        background-color: #328930;
        color: yellow;
        }
        QPushButton:pressed {
        background-color: #80c342;
        color: red;
        }    

        '''

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Please type here...")

        global submit_btn
        submit_btn = QPushButton()
        submit_btn.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Submit_Btn.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)

        submit_btn.setIconSize(QSize(50, 50))
        submit_btn.setIcon(icon)
        submit_btn.setFixedWidth(50)
        submit_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        submit_btn.setDefault(True)

        submit_btn.clicked.connect(self.on_submit_btn_click)

        # Record Button
        global record_btn
        global record_icon

        record_btn = QPushButton(parent=self)
        record_btn.setCheckable(True)
        record_icon = QtGui.QIcon()
        record_icon.addPixmap(QtGui.QPixmap(
            "Record_Btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        record_icon.addPixmap(QtGui.QPixmap(
            "unmute.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)            

        record_btn.setIconSize(QSize(50, 50))
        record_btn.setIcon(record_icon)
        record_btn.setFixedWidth(50)
        # record_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        record_btn.setDefault(False)

        # record_btn.clicked.connect(self.on_record_btn_click)

        # All Recording Button
        all_record_btn = QPushButton()
        all_record_btn.setCheckable(True)
        all_record_icon = QtGui.QIcon()
        all_record_icon.addPixmap(QtGui.QPixmap(
            "all_record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        all_record_btn.setIconSize(QSize(50, 50))
        all_record_btn.setIcon(all_record_icon)
        all_record_btn.setFixedWidth(50)
        all_record_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        all_record_btn.setDefault(True)

        global multi_line_txt
        multi_line_txt = QPlainTextEdit()
        multi_line_txt.move(20, 10)
        multi_line_txt.resize(50, 60)
        multi_line_txt.setFixedHeight(60)
        multi_line_txt.textChanged.connect(self.press_enter_event)
        font=QtGui.QFont('Arial',11)
        multi_line_txt.setFont(font)

        grid = QGridLayout()
        grid.addWidget(multi_line_txt, 0, 0, 1, 5)
        grid.addWidget(all_record_btn, 1, 1)
        grid.addWidget(record_btn, 1, 2)
        grid.addWidget(submit_btn, 1, 3)
        self.bottomRightGroupBox.setLayout(grid)

    def press_enter_event(self):
        if len(multi_line_txt.toPlainText()) > 0:
            last_value = multi_line_txt.toPlainText()[-1]
            if last_value == '\n':
                self.on_submit_btn_click()
            else:
                return
        else:
            return



    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Chat Window")

        global multi_line_txt_1
        multi_line_txt_1 = QPlainTextEdit()
        multi_line_txt_1.move(20, 10)
        multi_line_txt_1.resize(100, 100)
        multi_line_txt_1.setFixedHeight(300)
        multi_line_txt_1.setReadOnly(True)

        layout = QGridLayout()
        layout.addWidget(multi_line_txt_1, 1, 0, 1, 2)
        layout.setRowStretch(1, 1)
        self.topRightGroupBox.setLayout(layout)


    #def on_record_btn_click(self):

    # def on_record_btn_click(self):
    #     print(record_btn.isChecked())
    #     if record_btn.isChecked():
    #         record_icon.addPixmap(QtGui.QPixmap(
    #             "Record_Green_Btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #         record_btn.toggle()
    #     else:
    #         record_icon.addPixmap(QtGui.QPixmap(
    #             "Record_Btn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    #         record_btn.toggle()
    #     record_btn.setIcon(record_icon)





    def on_submit_btn_click(self):
        text = multi_line_txt.toPlainText()
        text1 = text.replace('\n', '').lower()
        if text1 in self.ques_dict.keys():
            self.answer.append(self.ques_dict[text1])
            print(self.answer)
            self.ques_lst.append(text)
            multi_line_txt.clear()
        else:
            self.ques_lst.append(text1)
            self.answer.append("Give a Try Once more!! :)")
            multi_line_txt.clear()

        counter = 0
        multi_line_txt_1.clear()
        for que, ans in zip(self.ques_lst, self.answer):
            multi_line_txt_1.appendHtml(f"""<span style="border: 2px solid #dedede;
            background-color:  #f8c471;        
            font-size: 24px;">
            <b>You: </b>{que}<br><br></p></span>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span
            style="background-color: skyblue;
            font-size: 24px;">
            <b></b>Bot: {ans}</p><br></span>
            """)


style = '''
QPushButton {
    background-color: #006325;
    font-size: 20px;
    color: white;

    min-width:  50px;
    max-width:  50px;
    min-height: 50px;
    max-height: 50px;

    border-radius: 25px;        
    border-width: 1px;
    border-color: #ae32a0;
    border-style: solid;
}
QPushButton:hover {
    background-color: #328930;
    color: yellow;
}
QPushButton:pressed {
    background-color: #80c342;
    color: red;
}    

'''
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    gallery = WidgetGallery()
    gallery.resize(400, 400)
    gallery.show()
    sys.exit(app.exec_())
