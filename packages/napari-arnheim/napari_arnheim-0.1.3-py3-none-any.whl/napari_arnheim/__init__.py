



if __name__ == "__main__":
    from napari_arnheim.widgets import ArnheimWidget
    from bergen import Bergen
    import napari

    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.window.add_dock_widget(ArnheimWidget(), area="right")