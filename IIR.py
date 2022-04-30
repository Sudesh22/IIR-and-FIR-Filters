import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
from math import pi
import sys, os, getpass
from os.path import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import QCursor, QIcon

plt.close('all')

USER_NAME = getpass.getuser()
if getattr(sys, 'frozen', False):
        curr_path = os.path.dirname(sys.executable)
elif __file__:
        curr_path = os.path.dirname(__file__)
print(curr_path)

class IIR_UI(QMainWindow):
    def __init__(self):
        super(IIR_UI, self).__init__()
        loadUi(os.path.join(curr_path,'IIR_UI.ui'), self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        def GetGraph(task, desc, due):
            Fs = int(task);
            n = int(desc);
            fc = []
            for i in due.split(","):
                fc.append(int(i))
            fc = np.array(fc)
            print(type(fc))
            self.fs_text.setText("")
            self.n_text.setText("")
            self.fc_text.setText("")
            
            w_c = 2*fc/Fs;
            [b,a] = sig.butter(n, w_c,btype='bandpass')

            # Frequency response
            [w,h] = sig.freqz(b,a,worN = 2000)
            w = Fs*w/(2*pi)  

            h_db = 20*np.log10(abs(h))

            plt.figure()
            plt.plot(w, h_db); plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude(dB)');plt.title('IIR filter Response')
            plt.grid('on')
            plt.show()
            
            # self.close()

        def close_win():
            self.fs_text.setText("")
            self.n_text.setText("")
            self.close()
            plt.close('all')
        
        self.Show_Graph.setStyleSheet("QPushButton{font: 9pt 'SansSerif';color: black;text-align: center;background-color:rgba(0, 0, 0, 0.1); border-radius: 15px;}QPushButton:hover{border : 2px solid black;} QPushButton:focus{outline: 0;border: 2px solid black;}")
        self.discard.setStyleSheet("QPushButton{font: 9pt 'SansSerif';color: black;text-align: center;background-color:rgba(0, 0, 0, 0.1); border-radius: 15px;}QPushButton:hover {border : 2px solid black;} QPushButton:focus {outline: 0;border: 2px solid black;}")

        self.Show_Graph.clicked.connect(lambda: GetGraph(self.fs_text.text(), self.n_text.text(), self.fc_text.text()))
        self.discard.clicked.connect(close_win)
    
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor)) #Change the mouse icon
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#Change window position
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))  

# Design IIR butterworth filter



def main():
    global app
    app = QApplication(sys.argv)   
    s = IIR_UI()
    s.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()