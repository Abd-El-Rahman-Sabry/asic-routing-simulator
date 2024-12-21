from PyQt5.QtWidgets import * 



class ControlWindow (QWidget): 

    _NumberOfButtons = 0

    def __init__(self, parent = None):
        self.app = QApplication([]) 
        super().__init__(parent)

        self.setWindowTitle("Router Control")
        self.setLayout(QVBoxLayout())
        self.setFixedWidth(400)






    def addButton(self , title , slot): 
        button = QPushButton(title , self)
        button.clicked.connect(slot)
        self.layout().addWidget(button)
        ControlWindow._NumberOfButtons += 1 
        self.setFixedHeight(ControlWindow._NumberOfButtons * (button.height()  + 10) )


    def show_controller(self):
        self.show() 
        self.app.exec_()


        






if __name__ == "__main__": 

    win = ControlWindow() 
    win.addButton("Remove Data" , lambda : print("remove data"))
    win.addButton("Test Data" , lambda : print("Test"))
    win.addButton("Run" , lambda : print("Hello"))
    win.addButton("Hello" , lambda : print("remove"))
    win.show_controller() 