from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QAction, QInputDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys
import game_panel # call game panel
import CheckersStateMachine # call chessboard

"""
This is the main window to control the whole system.
It has a menu bar and a background only. All the overall system operations are in this window.
Menu bar consists of Game, Edit, Theme and Help.
Game menu can start the game, end the current game, change players' name, the colours of checkers and exit the system
Edit menu has redo and undo options which can undo or redo current movements
Theme menu can change the background of the application, it has Marble, Wood and Sand themes.
Help menu includes help contents of the game and About the application.

"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Checkers Application"

        # default setting for player names, game panel is not initialised (false)
        self.name1 = "Player 1"
        self.name2 = "Player 2"

        self.initPanel = False
        self.theme = ""
        self.imgLabel = QLabel(self)
        self.imgLabel.move(0, 20)

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./icons/checkersLogo.jpg"))
        self.setMenu()
        self.setWoodBackground()
        self.showMaximized()
        # maximize button is not allowed
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    # menu bar setting
    # menu bar has four menus -> game, edit, theme, help
    def setMenu(self):
        mainMenu = self.menuBar()
        game = mainMenu.addMenu("&Game")
        edit = mainMenu.addMenu("Edi&t")
        theme = mainMenu.addMenu("&Theme")
        help = mainMenu.addMenu("&Help")

        # game menu ------>
        # start new game
        # click this to start the game
        self.startAction = QAction(QIcon("./icons/checkersLogo.jpg"), "&Start New Game", self)
        self.startAction.setShortcut("Ctrl+N")
        game.addAction(self.startAction)
        self.startAction.triggered.connect(self.startGame)
        self.startAction.setEnabled(True)

        # to end the current game
        self.endAction = QAction(QIcon("./icons/end.png"), "&End This Game", self)
        self.endAction.setShortcut("Ctrl+E")
        game.addAction(self.endAction)
        self.endAction.triggered.connect(self.end_game)

        # menu separator
        game.addSeparator()

        # colour selection <not working yet>
        # you can choose the colour of pieces (only before the game is started)
        self.pieceAction = QAction(QIcon("./icons/bluecheck.png"), "&Piece Selection", self)
        self.pieceAction.setShortcut("Ctrl+P")
        game.addAction(self.pieceAction)
        self.pieceAction.triggered.connect(self.pieceSelect)

        # change player name
        # you can change the players' names (only before the game is started)
        self.nameAction = QAction(QIcon("./icons/name.png"), "Change Players' &Name", self)
        self.nameAction.setShortcut("F2")
        game.addAction(self.nameAction)
        self.nameAction.triggered.connect(self.changeName)

        # menu separator
        game.addSeparator()

        # exit the whole system
        exitAction = QAction(QIcon("./icons/exit.png"), "E&xit", self)
        exitAction.setShortcut("Alt+F4")
        game.addAction(exitAction)
        exitAction.triggered.connect(self.close)

        # edit menu ------>
        # undo the current move
        self.undoAction = QAction(QIcon("./icons/undo.png"), "&Undo Move", self)
        self.undoAction.setShortcut("Ctrl+Z")
        edit.addAction(self.undoAction)
        self.undoAction.triggered.connect(self.undo)

        # redo the current move
        self.redoAction = QAction(QIcon("./icons/redo.jpg"), "&Redo Move", self)
        self.redoAction.setShortcut("Ctrl+Y")
        edit.addAction(self.redoAction)
        self.redoAction.triggered.connect(self.redo)

        # theme menu ------>
        # change the theme (background of the window)
        # change theme to marble
        self.marbleAction = QAction(QIcon("./icons/marble.jpg"), "&Marble", self)
        self.marbleAction.setShortcut("Ctrl+M")
        theme.addAction(self.marbleAction)
        self.marbleAction.triggered.connect(self.setMarbleBackground)

        # change theme to wood
        self.woodAction = QAction(QIcon("./icons/wood.jpg"), "&Wood", self)
        self.woodAction.setShortcut("Ctrl+W")
        theme.addAction(self.woodAction)
        self.woodAction.triggered.connect(self.setWoodBackground)

        # change theme to sand
        self.sandAction = QAction(QIcon("./icons/sand.jpg"), "San&d", self)
        self.sandAction.setShortcut("Ctrl+D")
        theme.addAction(self.sandAction)
        self.sandAction.triggered.connect(self.setSandBackground)

        # help menu ------>
        # help contents for the game
        helpAction = QAction(QIcon("./icons/help.png"), "Help &Content", self)
        helpAction.setShortcut("F1")
        help.addAction(helpAction)
        helpAction.triggered.connect(self.helpDialog)

        # menu separator
        help.addSeparator()

        # about the program
        aboutAction = QAction(QIcon("./icons/about.png"), "&About", self)
        aboutAction.setShortcut("Alt+A")
        help.addAction(aboutAction)
        aboutAction.triggered.connect(self.aboutDialog)

    # ask confirmation on exit
    def closeEvent(self, event):
        msg = "Are you sure you want to exit?"
        msgBox = QMessageBox()
        reply = msgBox.question(self, "Confirm Exit", msg, msgBox.Yes, msgBox.No)
        if reply == msgBox.Yes:
            event.accept()
            # if game panel is loaded, close the panel and the board
            if self.initPanel == True:
                self.panel.close()
                self.board.close()
            else:
                pass

        else:
            event.ignore()

    # start the game: game board is loaded with pieces for both players and the panel is loaded as well
    def startGame(self):

        # game panel is loaded
        self.panel = game_panel.GamePanel()

        # once game is started, game menu items and theme items cannot be changed
        self.startAction.setEnabled(False)
        self.nameAction.setEnabled(False)
        self.pieceAction.setEnabled(False)
        self.marbleAction.setEnabled(False)
        self.sandAction.setEnabled(False)
        self.woodAction.setEnabled(False)

        # take name variables from change name function
        self.panel.setPlayerNameOne(self.name1)
        self.panel.setPlayerNameTwo(self.name2)

        # redraw the panel according to new data
        self.panel.redrawUI()
        self.panel.show()
        self.initPanel = True
        # load the board
        self.board = CheckersStateMachine.myWindow()

    # redo current move <not working yet>
    def redo(self):
        msgBox = QMessageBox(self)
        msgBox.setText("This is redo action")
        msgBox.showFullScreen()

    # undo current move <not working yet>
    def undo(self):
        msgBox = QMessageBox(self)
        msgBox.setText("This is undo action")
        msgBox.showFullScreen()

    # select colour of pieces <this is not working yet>
    def pieceSelect(self):
        myColour = QInputDialog()
        colours = ("Red", "Blue")
        myColour.getItem(self, "Your colour", "Choose your checkers' colour", colours)
        myColour.show()

    # set background image (marble)
    def setMarbleBackground(self):
        self.theme = "marble"
        pixMap = QPixmap("./icons/" + self.theme + ".jpg")
        self.imgLabel.setPixmap(pixMap)
        self.imgLabel.resize(pixMap.width(), pixMap.height())

    # set background image (sand)
    def setSandBackground(self):
        self.theme = "sand"
        pixMap = QPixmap("./icons/" + self.theme + ".jpg")
        self.imgLabel.setPixmap(pixMap)
        self.imgLabel.resize(pixMap.width(), pixMap.height())

    # set background image (wood)
    def setWoodBackground(self):
        self.theme = "wood"
        pixMap = QPixmap("./icons/" + self.theme + ".jpg")
        self.imgLabel.setPixmap(pixMap)
        self.imgLabel.resize(pixMap.width(), pixMap.height())

    # the game is ended, all the menu items are on again <this function is not done yet>
    # this function will reset every variable and control to be ready for the new game
    def end_game(self):
        pass
        """self.startAction.setEnabled(True)
        self.nameAction.setEnabled(True)
        self.pieceAction.setEnabled(True)"""

    # change new names of the players
    # request new names using Input Dialog boxes
    def changeName(self):
        # ref: https://www.tutorialspoint.com/pyqt/pyqt_qinputdialog_widget.htm
        # ref: https://stackoverflow.com/questions/15968974/how-to-give-output-of-a-file-as-input-
        # to-other-file-how-to-give-the-text-entered

        player1_Name = QInputDialog()
        text, OK = player1_Name.getText(self, "Your Name", "Type player 1 name")
        if OK:
            if str(text) == "":
                self.name1 = "Player 1"
            else:
                self.name1 = str(text)
        player2_Name = QInputDialog()
        text, OK = player2_Name.getText(self, "Your Name", "Type player 2 name")
        if OK:
            if str(text) == "":
                self.name2 = "Player 2"
            else:
                self.name2 = str(text)

    # about the application
    def aboutDialog(self):
        aboutWindow = QMainWindow(self)
        lblAbout = QLabel(aboutWindow)
        lblLogo = QLabel(aboutWindow)
        customClose = QPushButton("Close", aboutWindow)

        # logo ref: https://appadvice.com/app/checkers-royale/296302022
        # display game logo on the dialog
        logo = QPixmap("./icons/CheckersLogo.jpg")
        lblLogo.setPixmap(logo)
        lblLogo.resize(150, 200)
        lblLogo.move(15, 0)

        # style sheet for this window
        aboutWindow.setStyleSheet("color: rgb(0, 130, 10); background: rgb(220, 230, 250);")

        # about this application displayed on label
        lblAbout.setText("Checkers Application 1.0\n\n"
                "This is a simple checkers application created with PyQt5 GUI Engine.\n\n"
                "This program is created by Myo Thet Tun & John O'Halloran."
                "\n\nOfficial Release Date: 14.12.2018"
                "\n\nCopyright © 2018-2020 by Micromac Software Inc.\n"
                "All rights reserved.")

        lblAbout.resize(600, 200)
        lblAbout.move(170, 0)
        lblAbout.setStyleSheet("font-size: 13px;")

        # customised close button
        customClose.move(530, 170)
        customClose.resize(60, 40)
        customClose.setStyleSheet("border-radius: 15px; background: rgb(110, 131, 70); color: white; font: bold 14px")
        customClose.clicked.connect(aboutWindow.close)

        # the window setting
        aboutWindow.setGeometry(400, 300, 800, 220)
        aboutWindow.setFixedSize(600, 220)
        aboutWindow.setWindowTitle('About the Checkers program')
        aboutWindow.setWindowIcon(QIcon('./icons/about.png'))
        # hide the title bar
        aboutWindow.setWindowFlags(Qt.FramelessWindowHint)

        aboutWindow.show()

    # help content shows in another window
    # content ref: https://cardgames.io/checkers/

    def helpDialog(self):
        helpContent = QMainWindow(self)
        label = QLabel(helpContent)
        customClose = QPushButton("Close", helpContent)

        # display help content on label
        label.setText("Checkers Rules\n\n"

              "\n\nOverview\n\n"
              
              "Pieces can only move diagonally.\n"
              "To capture an enemy piece, you must jump over it with one of your own pieces\n"
              "Red pieces move up the board, and blue pieces move down the board\n"
              "If a piece reaches the opposite side of the board, it is promoted to a king\n"
              "A promoted piece can move up and down the board.\n"
              
              "\n\nGame Play\n\n"
              
              "1) Select the piece you would like to move\n"
              "2) The game will highlight any available moves\n"
              "3) Select a highlighted tile to complete your move\n"
              "4) Click on end turn when you are done.\n"
              "5) If a player takes more than 5 minutes to complete a turn, they lose\n")

        label.resize(550, 360)
        label.move(10, 0)

        # customised close button
        customClose.move(420, 350)
        customClose.resize(60, 40)
        customClose.setStyleSheet("border-radius: 15px; background: rgb(110, 131, 70); color: white; font: bold 14px")
        customClose.clicked.connect(helpContent.close)

        # help content window setting
        helpContent.setGeometry(650, 250, 500, 400)
        helpContent.setFixedSize(500, 400)
        helpContent.setWindowTitle('Help Content')
        helpContent.setStyleSheet("background: white; font-size: 13px")
        helpContent.setWindowIcon(QIcon('./icons/help.png'))
        helpContent.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mnuTest = MainWindow()
    mnuTest.show()
    app.exec()