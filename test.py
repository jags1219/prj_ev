from PyQt5.QtWidgets import QApplication, QWidget 
from ui_output import Ui_Form

app = QApplication(sys.argv) 


class MainWindow(QWidget, Ui_Form):   
    def __init__(self, parent=None):     
        super(MainWindow, self).__init__(parent)     
        self.setupUi(self)     
        self.go_button.clicked.connect(self.pressed)   
    def pressed(self):     
        self.webView.setUrl(QUrl(self.lineEdit.displayText()))

view = MainWindow() 
view.show() 
view.showMaximized()
app.exec_()