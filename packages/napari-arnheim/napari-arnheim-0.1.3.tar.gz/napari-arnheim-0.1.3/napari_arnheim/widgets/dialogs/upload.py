from napari_arnheim.widgets.dialogs.forms.fields.selectors.models.sample_selector import SampleSelector
from re import A

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from napari_arnheim.widgets.base import BaseMixin, BaseWidget
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSpinBox, QVBoxLayout, QWidget
from bergen.query import AsyncQuery, QueryList
from grunnlag.schema import Experiment, Representation, Sample
import namegenerator
from qasync import asyncSlot
import xarray as xr
import numpy as np

def createDataArrayFromLayer(layer):

    data = layer.data
    ndim = layer.ndim

    if layer.ndim == 2:
        # first two dimensions is x,y and then channel
        shape = np.ones((5,))
        shape[:len(data.shape)] = data.shape
        return xr.DataArray(data.reshape(shape.astype(int)), dims=list("xyctz"))

    if layer.ndim == 3:
        # first three dimensios is z,x,y and then channel?
        shape = np.ones((5,))
        shape[:len(data.shape)] = data.shape
        return xr.DataArray(data.reshape(shape.astype(int)), dims=list("zxytc"))



class UploadFileDialog(BaseMixin, QDialog):


    def __init__(self, *args, layer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer


        self.representation_name = QLineEdit(namegenerator.gen())
        self.tags = QLineEdit("")

        self.sample_selector = SampleSelector(self, base=self.base)



        self.formGroupBox = QGroupBox("New Representation")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.representation_name)
        layout.addRow(QLabel("Tags:"), self.tags)
        layout.addRow(QLabel("Sample:"), self.sample_selector)
        self.formGroupBox.setLayout(layout)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.create)
        buttonBox.rejected.connect(self.reject)
        

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Create a new Representation")

              

    @asyncSlot()
    async def create(self):
        sampleid = self.sample_selector.getValue()
        tags = [ tag.strip() for tag in self.tags.text().split(",")]

        newarray = createDataArrayFromLayer(self.layer)
        self.created_rep = await Representation.asyncs.from_xarray(newarray, name=namegenerator.gen(), sample=sampleid, tags=tags)

        self.accept()

    
        




