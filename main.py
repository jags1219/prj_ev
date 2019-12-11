#!/usr/bin/env python
# from PyQt4 import QtGui, QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QPlainTextEdit)
import json

class WidgetGallery(QDialog):
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

        #    self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        # self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        # self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        #    disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topRightGroupBox, 5, 0, 1, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 1, 0, 1, 0)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 1)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setRowStretch(0, 0)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("EagleVoice")
        #    self.setMinimumSize(QSize(440, 240))
        #    self.windowIcon(QtGui.QIcon())
        self.changeStyle('Windows')

        with open('result.json', 'r') as fp:
            self.ques_dict = json.load( fp)
        # self.ques_dict = {"what is your name?": "My name is XY", 
        #                   "good morning": "Good Morning",
        #                   "bye": "Good Bye",
        #                   "hi": "Hello",
        #                   "how are you?": "I am fine, How about you ?",
        #                   }

        self.msg_lst = []
        self.master_lst = []

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Please type here...")
        # self.topRightGroupBox.setGeometry(QtCore.QRect(100, 100, 251, 141))

        global submit_btn
        submit_btn = QPushButton()
        submit_btn.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Submit_Btn.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        submit_btn.setIconSize(QSize(50, 50))
        submit_btn.setIcon(icon)
        submit_btn.setFixedWidth(50)
        submit_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        submit_btn.setDefault(True)

        submit_btn.clicked.connect(self.on_click)

        # Record Button
        record_btn = QPushButton()
        record_btn.setCheckable(True)
        record_icon = QtGui.QIcon()
        record_icon.addPixmap(QtGui.QPixmap("Record_Btn.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        record_btn.setIconSize(QSize(55, 50))
        record_btn.setIcon(record_icon)
        record_btn.setFixedWidth(55)
        record_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        record_btn.setDefault(True)

        # All Recording Button
        all_record_btn = QPushButton()
        all_record_btn.setCheckable(True)
        all_record_icon = QtGui.QIcon()
        all_record_icon.addPixmap(QtGui.QPixmap("all_record.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        all_record_btn.setIconSize(QSize(55, 50))
        all_record_btn.setIcon(all_record_icon)
        all_record_btn.setFixedWidth(55)
        all_record_btn.setStyleSheet('QPushButton{border: 1px solid;}')
        all_record_btn.setDefault(True)

        global multi_line_txt
        multi_line_txt = QPlainTextEdit()
        # multi_line_txt.insertPlainText("You can write text here.\n")
        multi_line_txt.move(20, 10)
        multi_line_txt.resize(100, 100)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(multi_line_txt, 2,0, 1, 5)
        grid.addWidget(all_record_btn, 3, 1)
        grid.addWidget(record_btn, 3, 2)
        grid.addWidget(submit_btn, 3, 3)
        self.topRightGroupBox.setLayout(grid)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Chat Window")

        global multi_line_txt_1
        multi_line_txt_1 = QPlainTextEdit()
        # multi_line_txt_1.insertPlainText("You can write text here down.\n")
        multi_line_txt_1.move(20, 10)
        multi_line_txt_1.resize(100, 100)
        # multi_line_txt_1.mouseMoveEvent(multi_line_txt_1.clear())

        layout = QGridLayout()
        # layout.addWidget(lineEdit, 0, 0, 1, 2)
        # layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(multi_line_txt_1, 1, 0, 1, 2)
        # layout.addWidget(slider, 3, 0)
        # layout.addWidget(scrollBar, 4, 0)
        # layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(1, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def on_click(self):
        text = multi_line_txt.toPlainText()
        self.answer = ""
        text1 = text.replace('\n', '').lower()   
        if text1 in self.ques_dict.keys():
            self.answer = self.ques_dict[text1]
            print(self.answer)
            self.msg_lst.append("You: "+text + '\n'+ "    Bot: " + self.answer)
            multi_line_txt.clear()
        else:
            self.answer = "Give a Try Once more!! :)"
            self.msg_lst.append("You: "+text + '\n'+ "    Bot: " + self.answer)
            multi_line_txt.clear()


        # multi_line_txt = QtGui.QTextCursor.atEnd()
        # self.msg_lst.append("Bot: " + self.answer)
        # self.master_lst.append(self.msg_lst)
        counter = 0
        print(self.msg_lst)
        multi_line_txt_1.clear()
        for val in self.msg_lst:
            # print(type(val))
            # print(val[counter])
            # counter += 1
            multi_line_txt_1.appendPlainText(str(val))

            # multi_line_txt.setPlainText(str(val))
        # multi_line_txt.setPlainText(self.answer)
        # multi_line_txt.clear()
        # print(text)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.resize(700, 700)
    gallery.show()
    sys.exit(app.exec_())
