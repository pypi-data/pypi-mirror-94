from PyQt5.QtGui import QStandardItem, QStandardItemModel
from bergen.query import QueryList
from napari_arnheim.widgets.dialogs.forms.fields.selectors.base import BaseSelector
from napari_arnheim.widgets.base import BaseMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class ArnheimModelSelector(BaseSelector):
    list_query = None
    model = None
    new_form = None
    # can stay not used

    def __init__(self, *args, base, variables=None, **kwargs):
        super().__init__(*args, base=base, **kwargs)
        self.selected_model = None
        self.variables = variables
        self.selector = None
        self.model_selector = None

        self.loadModels()

        self.layout = QHBoxLayout()

        self.setLayout(self.layout)

        self.buildOrReplaceSelector()
        self.buildButton()


    def loadModels(self):
        self.models = QueryList(
            self.list_query,
            self.model).run(
                variables=self.variables
        )

    def requestNewModel(self):
        form = self.new_form(base=self.base)
        model = form.getModel()
        if model:
            self.models = [model] + self.models # We are adding it to the first list
            self.buildOrReplaceSelector()

    def buildOrReplaceSelector(self):
        assert self.models is not None, "Please load Models beforee"
 
        model_selector = QComboBox()

        for model in self.models:
            model_selector.addItem(model.name)

        model_selector.currentIndexChanged.connect(self.indexChanged)

        if len(self.models) > 0:
            self.selected_model = self.models[0] # We automatically select the first item once rebuilding

        if not self.model_selector:
            self.layout.addWidget(model_selector)
            self.model_selector = model_selector
        
        else:
            self.layout.removeWidget(self.model_selector)
            self.model_selector.close()
            self.model_selector = model_selector
            self.layout.addWidget(self.model_selector)

        self.layout.update()

        return self.model_selector

    def buildButton(self):
        new_model_button = QPushButton("+")
        new_model_button.clicked.connect(self.requestNewModel)
        self.layout.addWidget(new_model_button)
        self.layout.update()


    def indexChanged(self, index):
        self.selected_model = self.models[index]

    def getValue(self):
        return str(self.selected_model.id)

