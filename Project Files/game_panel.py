from PyQt5.QtWidgets import QApplication, QGroupBox, QVBoxLayout, QWidget, QPushButton, QLabel, QLCDNumber, QGridLayout, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import QBasicTimer, Qt
import sys
"""
This is the game panel window which displays all the game data (Remaining pieces, Captured, player's names and
countdown timers) Each user needs to press the "End Turn" button every time he finished each move. Maximum
time allowed per move is 5 minutes, or otherwise, the player will lose the game. 
"""
class GamePanel(QWidget):
    def __init__(self):
        super().__init__()

        title = "Game Panel"
        top = 200
        left = 1200
        width = 300
        height = 450

        self.lblTitle = QLabel("Game Panel", self)
        self.lblTitle.setStyleSheet("font: bold 14px")

        # palette is to allocate the digital display
        self.myPalette = self.palette()
        self.myPalette.setColor(self.myPalette.WindowText, QColor(0, 0, 0))
        self.myPalette.setColor(self.myPalette.Light, QColor(0, 0, 115))
        self.setPalette(self.myPalette)

        self.initialise()

        # pass all the statistics of the game here
        self.player1 = 1
        self.playerName1 = "Player One"

        self.remain1 = 12
        self.capture1 = 0

        self.player2 = 2
        self.playerName2 = "Player Two"

        self.remain2 = 12
        self.capture2 = 0

        # when end turn button has clicked, pass the player number to the function
        self.btnEnd1.clicked.connect(lambda: self.activateTimer(self.num))
        self.btnEnd2.clicked.connect(lambda: self.activateTimer(self.num))

        # settings for this window
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./icons/checkersLogo.jpg"))
        self.setGeometry(left, top, width, height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(width, height)

    # reload all the data in the two group boxes (update with new data)
    def redrawUI(self):

        # main vertical layout consists of two group boxes for players' statistics
        vBox = QVBoxLayout()
        vBox.addWidget(self.lblTitle)

        # update the values in the game panel

        vBox.addWidget(self.createGroupBox(self.playerName1, self.player1, self.remain1, self.capture1))
        vBox.addWidget(self.createGroupBox(self.playerName2, self.player2, self.remain2, self.capture2))
        vBox.setSpacing(30)

        vBox.addStretch()
        self.setLayout(vBox)

    # take player one's new name
    def setPlayerNameOne(self, player_name):
        self.playerName1 = player_name

    # take player two's new name
    def setPlayerNameTwo(self, player_name):
        self.playerName2 = player_name

    # pass all the game's data to this function
    # player's name, number (1 or 2???), remain and capture
    def createGroupBox(self, playerName, player, remain, capture):

        lblColour = QLabel()
        groupBox = QGroupBox()
        gridLayout = QGridLayout()

        if player == 1:
            # pass player 1 data
            groupBox.setTitle(playerName) # title with player one's name
            gridLayout.addWidget(self.btnEnd1, 0, 1)
            checker = "redcheck" # checker is red colour
            lblRemain = QLabel(str(remain))
            lblCapture = QLabel(str(capture))
            gridLayout.addWidget(self.lblLcd1, 3, 1) # timer

        else:
            # pass player 2 data
            groupBox.setTitle(playerName) # title with player's two name
            gridLayout.addWidget(self.btnEnd2, 0, 1)
            checker = "bluecheck" # checker is blue colour
            lblRemain = QLabel(str(remain))
            lblCapture = QLabel(str(capture))
            gridLayout.addWidget(self.lblLcd2, 3, 1) # timer

        # show the colours of the player
        # pictures of checkers
        pixmap = QPixmap("./icons/" + checker + ".png")
        small_pixmap = pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.FastTransformation)
        lblColour.setPixmap(small_pixmap)

        # labels for the form
        lblTimer = QLabel("Elapsed Time : ")
        lblRemainText = QLabel("Remaining : ")
        lblCaptureText = QLabel("Captured :")

        # arrange the group box form in grid layout
        gridLayout.addWidget(lblColour, 0, 0)
        gridLayout.addWidget(lblTimer, 3, 0)

        gridLayout.addWidget(lblRemainText, 4, 0)
        gridLayout.addWidget(lblRemain, 4, 1)
        gridLayout.addWidget(lblCaptureText, 5, 0)
        gridLayout.addWidget(lblCapture, 5, 1)

        groupBox.setLayout(gridLayout)

        return groupBox

    # initialise the buttons, LCD number and timer
    def initialise(self):

        # initialise LCD display
        self.lblLcd1 = QLCDNumber()
        self.lblLcd1.display("05:00")
        self.lblLcd2 = QLCDNumber()
        self.lblLcd2.display("05:00")

        # initialise buttons
        self.btnEnd1 = QPushButton("End Turn")
        self.btnEnd2 = QPushButton("End Turn")
        self.btnEnd1.setStyleSheet("background-color: rgb(109, 173, 67); border-radius: 6px; "
                                   "border: 0.5px solid black; font: bold 12px")
        self.btnEnd2.setStyleSheet("background-color: rgb(109, 173, 67); border-radius: 6px; "
                                   "border: 0.5px solid black; font: bold 12px")

        # enable player 1 to start the game
        # only player one's button is appeared
        self.btnEnd1.setVisible(True)
        self.btnEnd2.setVisible(False)

        # initialise timer
        self.timer = QBasicTimer()
        self.second = 60
        self.min = 4
        self.num = 1 # player one to start first move
        self.timer.start(1000, self)

    # starting the timer by turn
    # countdown timer will start running and only one button appear each turn
    # e.g. button for player one is active on player one's turn and so on
    def activateTimer(self, num):
        self.second = 60
        self.min = 4

        if num == 1:
            # display the timer for player one
            self.lblLcd1.display("0" + str(self.min) + ":" + str(self.second))

            # player two's button is active
            self.btnEnd2.setVisible(True)
            self.btnEnd1.setVisible(False)

            # player one's timer is active
            # self.num holds the value whose turn will be the next one
            self.num = 2
            self.timer.start(1000, self)
        else:
            # timer for player two

            self.lblLcd2.display("0" + str(self.min) + ":" + str(self.second))

            # player one's button is active
            self.btnEnd1.setVisible(True)
            self.btnEnd2.setVisible(False)

            # player two's timer is active
            # self.num holds the value whose turn will be the next one
            self.num = 1
            self.timer.start(1000, self)

    # display the countdown timer on the LCD digital board of each player
    def timerEvent(self, event):
        msgBox = QMessageBox()
        # if it is player one, show the time in LCD 1
        if self.num == 1:
            self.second -= 1
            # second is more than 10, LCD shows 04:10
            if self.second >= 10:

                self.lblLcd1.display("0" + str(self.min) + ":" + str(self.second))
            # second is less than 10, LCD shows 04:09, 04:08, etc
            elif self.second < 10 and self.second > 0:

                self.lblLcd1.display("0" + str(self.min) + ":0" + str(self.second))
            # second is 0, restart from 60 and decrease 1 minute
            elif self.second == 0:

                self.second = 60
                self.min -= 1

                self.lblLcd1.display("0" + str(self.min) + ":" + str(self.second))

                # last minute has passed, time is up
                if self.min == -1:
                    self.second = 0
                    self.timer.stop()

                    # display player one has lost
                    self.lblLcd1.display("00" + ":0" + str(self.second))
                    msgBox.about(self, "Game Over", "Time is up!\n\n" + self.playerName1 + " cannot make any move in 5 minutes\n\n"
                                 + self.playerName1 + " lost!")
                    # hide the button
                    self.btnEnd1.setVisible(False)
                else:
                    pass
            else:
                pass
        # if it is player two, show the time in LCD 2
        else:
            self.second -= 1
            # second is more than 10, LCD shows 04:10
            if self.second >= 10:

                self.lblLcd2.display("0" + str(self.min) + ":" + str(self.second))
            # second is less than 10, LCD shows 04:09, 04:08, etc
            elif self.second < 10 and self.second > 0:

                self.lblLcd2.display("0" + str(self.min) + ":0" + str(self.second))
            # second is 0, restart from 60 and decrease 1 minute
            elif self.second == 0:

                self.second = 60
                self.min -= 1

                self.lblLcd2.display("0" + str(self.min) + ":" + str(self.second))
                # last minute has passed, time is up
                if self.min == -1:
                    self.second = 0
                    self.timer.stop()

                    # display player two has lost
                    self.lblLcd2.display("00" + ":0" + str(self.second))
                    msgBox.about(self, "Game Over", "Time is up!\n\n" + self.playerName2 + " cannot make any move in 5 minutes\n\n"
                                 + self.playerName2 + " lost!")
                    # hide the button
                    self.btnEnd2.setVisible(False)
                else:
                    pass
            else:
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gamePanel = GamePanel()
    gamePanel.show()
    app.exec()