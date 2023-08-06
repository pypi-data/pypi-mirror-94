
from napari_arnheim.widgets import ArnheimWidget
import napari
from qasync import QEventLoop, QThreadExecutor
from napari_arnheim.widgets import ArnheimWidget
from bergen import Bergen
import napari
import asyncio
import sys
from skimage import data

def main():

    with napari.gui_qt() as app:
        viewer = napari.Viewer()
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)
        viewer.window.add_dock_widget(ArnheimWidget(), area="right")

        with loop:
            sys.exit(loop.run_forever())

