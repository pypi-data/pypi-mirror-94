from PySide2.QtWidgets import QMessageBox
from PySide2.QtGui import QIcon
from pathlib import Path

class MsgBox(QMessageBox):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(text)
    
    def set_custom_icon(self, icon):
        self.setIconPixmap(icon)
        q_icon = QIcon(icon)
        self.setWindowIcon(q_icon)
    
    def set_yes_no_buttons(self):
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)


icons_path = Path(__file__).parent.absolute() / 'icons'

def successful_msgbox(title, text):
    icon = str(icons_path / 'correct.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.exec_()


def input_error_msgbox(title, text):
    icon = str(icons_path / 'input_error.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.exec_()


def warning_msgbox(title, text):
    icon = str(icons_path / 'warning.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.set_yes_no_buttons()
    resp = msg_box.exec_()
    return resp


def information_msgbox(title, text):
    icon = str(icons_path / 'information.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.exec_()


def database_error_msgbox(title, text):
    icon = str(icons_path / 'database-error.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.exec_()


def error_msgbox(title, text):
    icon = str(icons_path / 'database-error.png')
    msg_box = MsgBox(title, text)
    msg_box.set_custom_icon(icon)
    msg_box.exec_()
