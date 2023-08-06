from napari import Viewer
from grunnlag.schema import Representation

class Helper:

    def __init__(self, viewer: Viewer) -> None:
        self.viewer = viewer
        pass

    def openRepresentationAsLayer(self, rep: Representation):
        if "mask" in rep.tags:
            self.viewer.add_labels(rep.data.sel(c=0).data, name=rep.name, metadata={"rep":rep})
        else:    
            self.viewer.add_image(rep.data.sel(c=0).data, name=rep.name, metadata={"rep":rep})

