from PySide import QtGui, QtCore

REGISTER_DIALOG_WIDTH = 300
REGISTER_DIALOG_HEIGHT = 200

class ProfileDialog(QtGui.QDialog):

    def __init__(self, mode):
        super(ProfileDialog, self).__init__()

        self.__login_line_edit__ = QtGui.QLineEdit(self)
        self.__login_label__ = QtGui.QLabel()
        self.__password_line_edit__ = QtGui.QLineEdit(self)
        self.__password_label__ = QtGui.QLabel()

        self.__login_label__.setText('Username:')
        self.__password_label__.setText('Password:')

        self.__login_layout__ = QtGui.QHBoxLayout()
        self.__login_layout__.addWidget(self.__login_label__)
        self.__login_layout__.addWidget(self.__login_line_edit__)

        self.__password_layout__ = QtGui.QHBoxLayout()
        self.__password_layout__.addWidget(self.__password_label__)
        self.__password_layout__.addWidget(self.__password_line_edit__)

        self.__register_button__ = QtGui.QPushButton()
        self.__register_button__.setText(mode)
        if mode == 'Login':
            self.__register_button__.released.connect(self.login)
        elif mode == 'Register':
            self.__register_button__.released.connect(self.register)

        self.__panel_layout__ = QtGui.QVBoxLayout()
        self.__panel_layout__.addLayout(self.__login_layout__)
        self.__panel_layout__.addLayout(self.__password_layout__)
        self.__panel_layout__.addWidget(self.__register_button__)

        self.setLayout(self.__panel_layout__)
        self.resize(REGISTER_DIALOG_WIDTH, REGISTER_DIALOG_HEIGHT)

    def login(self):
        print("login")

    def register(self):
        print("register")