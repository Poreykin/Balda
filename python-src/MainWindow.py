from PySide import QtGui, QtCore
from interface.GraphicBoard import GraphicBoard
from external.SettingsDialog import SettingsDialog
from external.ProfileDialog import ProfileDialog

__author__ = 'akhtyamovpavel'

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__width_letters__ = 5
        self.__height_letters__ = 5

        self.create_actions()
        self.create_menus()
        self.rules()
        self.gb = None

        self.__login_dialog__ = ProfileDialog('Log in')
        self.__register_dialog__ = ProfileDialog('Register')

        self.__settings_dialog__ = SettingsDialog()
        self.__settings_dialog__.connect_to_main_window(self)

        self.resize(600, 400)

    def create_actions(self):
        self.new_game = QtGui.QAction('New game', self)
        self.new_game.triggered.connect(self.start_new_game)
        self.exit_game = QtGui.QAction('Exit', self)
        self.exit_game.triggered.connect(QtGui.qApp.quit)

        self.login = QtGui.QAction('Log in', self)
        self.login.triggered.connect(self.log_in_user)
        self.register = QtGui.QAction('Register', self)
        self.register.triggered.connect(self.register_user)
        self.logout = QtGui.QAction('Log out', self)
        self.logout.triggered.connect(self.log_out_user)

        self.settings_action = QtGui.QAction('Settings', self)
        self.settings_action.triggered.connect(self.run_settings)

    def create_menus(self):
        self.menu = QtGui.QMenu('Game', self)
        self.menu.addAction(self.new_game)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_game)
        self.menuBar().addMenu(self.menu)

        self.menu = QtGui.QMenu('Profile', self)
        self.menu.addAction(self.login)
        self.menu.addAction(self.register)
        self.menu.addSeparator()
        self.menu.addAction(self.logout)
        self.menuBar().addMenu(self.menu)

        self.menu = QtGui.QMenu('Settings', self)
        self.menu.addAction(self.settings_action)
        self.menuBar().addMenu(self.menu)

    def rules(self):
        self.label = QtGui.QLabel(self)
        self.label.setText("OK")
        self.setCentralWidget(self.label)

    def get_height(self):
        return self.__height_letters__

    def get_width(self):
        return self.__width_letters__

    @QtCore.Slot()
    def start_new_game(self):
        self.gb = GraphicBoard(width=self.__width_letters__, height=self.__height_letters__, parent=self)
        self.setCentralWidget(self.gb)

    @QtCore.Slot()
    def log_in_user(self):
        self.__login_dialog__.exec_()

    @QtCore.Slot()
    def register_user(self):
        self.__register_dialog__.exec_()

    @QtCore.Slot()
    def log_out_user(self):
        print("log_out")

    @QtCore.Slot()
    def run_settings(self):
        self.__settings_dialog__.exec_()

    def set_settings(self, coordinates):
        self.__width_letters__ = coordinates[0]
        self.__height_letters__ = coordinates[1]

    @QtCore.Slot()
    def reset_field(self):
        self.setCentralWidget(None)
        self.rules()


