from PySide import QtGui, QtCore

MIN_WIDTH = 3
MAX_WIDTH = 10
MIN_HEIGHT = 3
MAX_HEIGHT = 10

SETTINGS_DIALOG_WIDTH = 150
SETTINGS_DIALOG_HEIGHT = 200

class SettingsDialog(QtGui.QDialog):
    save_data = QtCore.Signal(tuple)

    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.__width_spin_box__ = QtGui.QSpinBox()
        self.__width_label__ = QtGui.QLabel()
        self.__height_spin_box__ = QtGui.QSpinBox()
        self.__height_label__ = QtGui.QLabel()

        self.__width_label__.setText('Width')
        self.__height_label__.setText('Height')

        self.__width_spin_box__.setMinimum(MIN_WIDTH)
        self.__width_spin_box__.setMaximum(MAX_WIDTH)
        self.__height_spin_box__.setMinimum(MIN_HEIGHT)
        self.__height_spin_box__.setMaximum(MAX_HEIGHT)

        self.__width_layout__ = QtGui.QHBoxLayout()
        self.__width_layout__.addWidget(self.__width_label__)
        self.__width_layout__.addWidget(self.__width_spin_box__)

        self.__height_layout__ = QtGui.QHBoxLayout()
        self.__height_layout__.addWidget(self.__height_label__)
        self.__height_layout__.addWidget(self.__height_spin_box__)

        self.__save_button__ = QtGui.QPushButton()
        self.__save_button__.setText('Save')
        self.__close_button__ = QtGui.QPushButton()
        self.__close_button__.setText('Close')

        self.__save_button__.released.connect(self.send_data)
        self.__close_button__.released.connect(self.close)

        self.__panel_layout__ = QtGui.QVBoxLayout()
        self.__panel_layout__.addLayout(self.__width_layout__)
        self.__panel_layout__.addLayout(self.__height_layout__)
        self.__panel_layout__.addWidget(self.__save_button__)
        self.__panel_layout__.addWidget(self.__close_button__)

        self.setLayout(self.__panel_layout__)
        self.resize(SETTINGS_DIALOG_WIDTH, SETTINGS_DIALOG_HEIGHT)

    def connect_to_main_window(self, window):
        self.save_data.connect(window.set_settings)

    def send_data(self):
        packed_data = (self.__width_spin_box__.value(), self.__height_spin_box__.value())
        self.save_data.emit(packed_data)
