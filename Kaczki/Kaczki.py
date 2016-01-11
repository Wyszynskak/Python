#!/home/kkk/anaconda3/bin/python3

"""
ZetCode PyQt4 tutorial 

In this example, we dispay an image
on the window. 

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtCore
import random

class MainWin(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()
        
    def initUI(self):     
        self.setWindowTitle('Kaczki')
        self.setWindowIcon(QtGui.QIcon('kaczor.png')) 
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        self.aboutWindow()
        self.tboard.start()
        self.statusBar()
        
        #Wyjscie        
        exitAction = QtGui.QAction(QtGui.QIcon('kaczor.png'), 'Exit', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        #Nowa gra
        newGameOption = QtGui.QAction(QtGui.QIcon('kaczor.png'), 'New Game', self)
        newGameOption.setShortcut('N')
        newGameOption.setStatusTip('New Game')
        newGameOption.triggered.connect(self.newGame)
        
        #Opcje
        optionsAction= QtGui.QAction(QtGui.QIcon('kaczor.png'), 'Options', self)
        optionsAction.setShortcut('O')
        optionsAction.setStatusTip('Options')
        optionsAction.triggered.connect(self.setOptions)
        
        #Help
        aboutOption = QtGui.QAction(QtGui.QIcon('kaczor.png'), 'About', self)
        aboutOption.setShortcut('A')
        aboutOption.setStatusTip('About')
        aboutOption.triggered.connect(self.aboutWindow)        
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newGameOption)
        fileMenu.addAction(optionsAction)
        fileMenu.addAction(exitAction)
        
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutOption)

        
        self.resize(960, 600)
        self.center()
        self.show() 
    
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def keyPressEvent(self, event):
        self.tboard.keyPressEvent(event)
    def keyReleaseEvent(self, event):
        if event.key()==QtCore.Qt.Key_N:
            self.newGame()
        else:    
            self.tboard.keyReleaseEvent(event)
            
    def newGame(self):
        self.pause()
        reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure you want to restart your game?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.unPause()
            self.tboard.newGame()
        else:
            self.unPause()
            return
            
    def aboutWindow(self):
        self.pause()
        QtGui.QMessageBox.about(self, "About", 
        """
        Witaj w grze KACZKI!

        Masz ochotę postrzelać? To świetnie!
        Ustrzel zatem tyle kaczek ile zdołasz!

        Cel gry:
        Zestrzelić jak najwięcej kaczek zachowując
        przynajmniej jedno życie.

        Sterowanie:
        Strzałki - ruch celownika 
        D - strzał
        N - nowa gra
        O - opcje
        A - opis gry
        Esc - Exit

        Uwaga!
        Ze względu na specyfikację biblioteki, 
        w której tworzona była gra celownik 
        porusza się tylko w jednym kierunku 
        jednocześnie - góra, dół,prawo, lewo - 
        nie ma możliwości poruszania się po 
        skosie, co dodatkowo utrudnia grę.
        Opis problemu:
            http://stackoverflow.com/questions/14159318/pyqt4-holding-down-a-
            key-detected-as-frequent-press-and-release
        """
        )
        self.unPause()
        
            
    def closeEvent(self, event):      
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
            
    def setOptions(self):
        self.pause()
        self.optWindow = Options(self)

        
    def pause(self):
        self.tboard.pause=True
        
    def unPause(self):
        self.tboard.pause=False
        
    def changeParameters(self, duck_speed, sigh_move):
        self.tboard.changeSpeed(duck_speed, sigh_move)
        self.tboard.newGame()
    def getParameters(self):
        return (self.tboard.duck_alive_speed, self.tboard.sigh_move)
            
class Options(QtGui.QDialog):
    duck_move=0
    sigh_move=0
    
    def __init__(self, parent = None):        
        super(Options, self).__init__(parent)
        self.initUI()
        
    def initUI(self):    
        #Przesuniecie celownika
        self.sigh_move_sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sigh_move_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sigh_move_sld.resize(100, 30)
        self.sigh_move_sld.valueChanged[int].connect(self.changeSighMove)
        self.sigh_move_sld.setMinimum(5)
        self.sigh_move_sld.setMaximum(50)
        self.sigh_move_sld.setValue(self.parent().getParameters()[1])
        
        self.sigh_move_lbl = QtGui.QLabel(self)
        self.sigh_move_lbl.setText("Przesuniecie celownika: " + str(
            self.sigh_move_sld.value()))
        
        #Przesunięcie kaczki
        self.duck_move_sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.duck_move_sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.duck_move_sld.resize(100, 30)
        self.duck_move_sld.valueChanged[int].connect(self.changeDuckMove)
        self.duck_move_sld.setMinimum(5)
        self.duck_move_sld.setMaximum(40)
        self.duck_move_sld.setValue(self.parent().getParameters()[0])
        
        self.duck_move_lbl = QtGui.QLabel(self)
        self.duck_move_lbl.setText("Przesuniecie kaczki: " + str(
            self.duck_move_sld.value()))
        
        #Przerwanie zmian
        cancel_button = QtGui.QPushButton('Cancel', self)
        cancel_button.setCheckable(True)
        cancel_button.move(10, 60)
        cancel_button.clicked[bool].connect(self.pressCancel)
        
        #Zatwierdzenie
        OK_button = QtGui.QPushButton('Restart game', self)
        OK_button.setCheckable(True)
        OK_button.move(10, 60)
        OK_button.clicked[bool].connect(self.pressOKButton)

        #Ulozenie elementow
        sigh_hbox = QtGui.QHBoxLayout()
        sigh_hbox.addWidget(self.sigh_move_lbl)
        sigh_hbox.addWidget(self.sigh_move_sld)
        
        duck_hbox = QtGui.QHBoxLayout()
        duck_hbox.addWidget(self.duck_move_lbl)
        duck_hbox.addWidget(self.duck_move_sld)
        
        button_hbox = QtGui.QHBoxLayout()
        button_hbox.addWidget(OK_button)
        button_hbox.addWidget(cancel_button)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(sigh_hbox)
        vbox.addLayout(duck_hbox)
        vbox.addLayout(button_hbox)
        
        self.setLayout(vbox)  
        
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('QtGui.QSlider')
        self.show()
        
    def changeSighMove(self, value):
        try:
           self.sigh_move_lbl.setText("Przesuniecie celownika: "+ str(value))
        except:
            pass
        
        self.sigh_move=value

    
    def changeDuckMove(self, value):
        self.duck_move_lbl.setText("Przesuniecie kaczki: " + str(value))
        self.duck_move=value

        
    def pressOKButton(self):
        print("Naciskam przycisk Ok i odpauzowuje gre")
        self.parent().unPause()
        print("Przekazuje parametry do rodzica:" +      str((self.duck_move,self.sigh_move)))
        self.parent().changeParameters(self.duck_move,
                                 self.sigh_move)
        print("Zamykam opcje")
        self.close()
    
    def pressCancel(self):
        self.parent().unPause()
        self.close()
            
            
class Board(QtGui.QFrame):
    
    def __init__(self, parent):
        super(Board, self).__init__(parent)
        
        self.initBoard()
        
        
    def initBoard(self): 
        self.timer = QtCore.QBasicTimer()
        self.GameOver=False
        self.pause=False
        self.life=5
        #Tło        
        pixmap = QtGui.QPixmap("2.png")
        self.lbl = QtGui.QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.move(0,0)
        self.WindowWidth=pixmap.width()
        self.WindowHeight=pixmap.height()
        
        #Dane
        QtGui.QFrame.setFont(self,QtGui.QFont('Fantasy', 15))
        self.points=QtGui.QLabel(self)
        self.points.setScaledContents(True)
        self.points.setText("Punkty:    0")
        self.points.move(550,0)
        
        self.lifes=QtGui.QLabel(self)
        self.lifes.setText("Życie:    5")
        self.lifes.move(700,0)
        
        #Kaczki
        self.max_number_ducks=5
        self.duck_label_list=[QtGui.QLabel(self) for i in 
                range(self.max_number_ducks)] #Kaczka jako obrazek
        duck_picture=QtGui.QPixmap("kaczor.png")
        self.duck_height=duck_picture.height()
        self.duck_width=duck_picture.width()
        
        self.duck_list=[] #Kaczka jako współrzędne w programie
        self.duck_alive_speed=5
        self.duck_dead_speed=70
        self.gone=0
        self.dead=0
        for i in range(self.max_number_ducks):
            self.newduck(self.duck_list)
            self.duck_label_list[i].setPixmap(duck_picture)
            self.duck_label_list[i].move(
                self.duck_list[i][0], self.duck_list[i][1])
                
                
        #Celownik
        self.sighX=self.WindowWidth/2
        self.sighY=self.WindowHeight/2
        self.sigh_move=30
        sigh_picture=QtGui.QPixmap("celownik.png")
        self.sigh_size=sigh_picture.height()
        self.sigh_lbl=QtGui.QLabel(self)
        self.sigh_lbl.setPixmap(sigh_picture)  
        self.sigh_lbl.move(self.sighX, self.sighY)
        
    def start(self):
        self.timer.start(50, self)
        
        
    def paintEvent(self, event):
        if self.pause:
            return
            
        if self.gone>=self.life:
            self.GameOver=True
            pixmap = QtGui.QPixmap("32.png")
            self.lbl.setPixmap(pixmap)
            
            score=QtGui.QLabel(self)
            score.setText("Twój wynik to:    " + str(self.dead))
            score.move(0.5*self.WindowWidth-30,0.75*self.WindowHeight)
            
            for i in range(self.max_number_ducks):
                self.duck_label_list[i].hide()
            self.sigh_lbl.hide()
            self.lifes.hide()
            
            QtGui.QFrame.setFont(self,QtGui.QFont('Fantasy', 30))
            self.points.resize(400,100)
            self.points.move(0.5*self.WindowWidth-100,
                             0.75*self.WindowHeight-10)
                
            return
            
        #Rysowanie kaczek
        for i in range(self.max_number_ducks):
            self.duck_label_list[i].move(
                self.duck_list[i][0], self.duck_list[i][1])
                
        #Kontrola czy celownik nie wyszedl poza ekran
        if self.sighX<0:
            self.sighX=0
        elif self.sighX>self.WindowWidth-self.sigh_size:
            self.sighX=self.WindowWidth-self.sigh_size
            
        if self.sighY<0:
            self.sighY=0;
        elif self.sighY>self.WindowHeight-self.sigh_size:
            self.sighY=self.WindowHeight-self.sigh_size
            
        self.sigh_lbl.move(self.sighX,self.sighY)
        self.points.setText("Punkty: "+ str(self.dead))
        self.lifes.setText("Życie: "+ str(5-self.gone))
        
    def timerEvent(self, event):
        if self.pause:
            return
            
        if event.timerId() == self.timer.timerId():
            
            #Duck movement
            for i,duck in enumerate(self.duck_list):
                if duck[0]>self.WindowWidth and duck[2]==True:
                    self.gone+=1
                    duck[2]=False
           
           #Alive
                if duck[2]:
                    duck[0]+=self.duck_alive_speed
                    duck[1]+=random.sample([2,-2],1)[0]*self.duck_alive_speed
                    if duck[0]<3*self.WindowWidth/8 and duck[1]<0:
                        duck[1]+=self.duck_alive_speed
                    elif (duck[0]<3*self.WindowWidth/8 and 
                        duck[1]>self.WindowHeight-self.duck_height):
                            duck[1]-=4*self.duck_alive_speed
                #Dead
                else:
                    duck[1]+=self.duck_dead_speed
                    if duck[1]>self.WindowHeight:
                        del self.duck_list[i]
                        self.newduck(self.duck_list)
                    
            self.update()               
        else:
            super(Board, self).timerEvent(event)
        
    def keyPressEvent(self, event):
        key = event.key()
            
        if key == QtCore.Qt.Key_P:
            self.pause= (not self.pause)
            return
            
        if self.pause:
            return
            
        if key == QtCore.Qt.Key_Left:
            self.sighX-=self.sigh_move
            self.update()
            
        elif key == QtCore.Qt.Key_Right:
            self.sighX+=self.sigh_move
            self.update()
            
        elif key == QtCore.Qt.Key_Down:
            self.sighY+=self.sigh_move
            self.update()
            
        elif key == QtCore.Qt.Key_Up:
            self.sighY-=self.sigh_move
            self.update()   
            
        elif key == QtCore.Qt.Key_D:
            sight_middle_x=self.sighX+self.sigh_size/2
            sight_middle_y=self.sighY+self.sigh_size/2
                
            for i,duck in enumerate(self.duck_list):               
                if (duck[0] < sight_middle_x < duck[0]+self.duck_width and
                    duck[1] < sight_middle_y < duck[1]+self.duck_height/2):
                        self.duck_list[i]=[duck[0],duck[1],False]
                        self.dead+=1
            
        else:
            super(Board, self).keyPressEvent(event)
        
    def newduck(self, duck_list):
        #duck=[x,y,is_alive]
        duck=[-1.5*self.duck_width*random.random()-self.duck_width/2,
              (self.WindowHeight-2*self.duck_height)*random.random(),
             True]
        duck_list.append(duck)
    
    def newGame(self):
        if self.GameOver:
            #Tło        
            pixmap = QtGui.QPixmap("2.png")
            self.lbl.setPixmap(pixmap)
            #Dane
            QtGui.QFrame.setFont(self,QtGui.QFont('Fantasy', 15))
            self.points.move(550,0)
            self.points.resize(150,20)
            self.sigh_lbl.show()
            self.lifes.show()
            
            
        self.pause=False
        self.sighX=self.WindowWidth/2
        self.sighY=self.WindowHeight/2 
        self.sigh_lbl.move(self.sighX, self.sighY)
        self.duck_list=[] #Kaczka jako współrzędne w programie
        self.gone=0
        self.dead=0
        for i in range(self.max_number_ducks):
            self.newduck(self.duck_list)
            if self.GameOver:
                self.duck_label_list[i].show()
            
        self.GameOver=False
        self.start()
        self.update()
                
    def changeSpeed(self, duck_movement, sigh_movement):
         self.duck_alive_speed=duck_movement
         self.sigh_move=sigh_movement
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  