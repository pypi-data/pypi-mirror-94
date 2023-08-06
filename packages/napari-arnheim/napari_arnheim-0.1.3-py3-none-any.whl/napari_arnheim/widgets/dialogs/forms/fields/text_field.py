from napari_arnheim.widgets.dialogs.forms.fields.base import FieldMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout, QWidget
import namegenerator

class TextField(QLineEdit):

    def __init__(self, base=None, **kwargs):
        super().__init__(namegenerator.gen(), **kwargs)

    def getValue(self):
        return str(self.text())