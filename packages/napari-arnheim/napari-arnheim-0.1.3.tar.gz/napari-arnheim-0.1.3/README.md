# Napari - Arnheim

### Idea

Napari Arnheim bundles Napari with the Arnheim Framework Client and its Grunnlag-Provider

 
### Prerequisites

Napari Arnheim only works with a running Arnheim Instance (in your network or locally for debugging) and a Grunnlag-Provider. (see Grunnlag)

### Usage

In order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance

```python

bergen = Bergen(host="HOST_NAME",
    port=8000,
  client_id="APPLICATION_ID_FROM_ARNHEIM", 
  client_secret="APPLICATION_SECRET_FROM_ARNHEIM",
  name="karl",
)


with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.window.add_dock_widget(ArnheimWidget(bergen=bergen), area="right")


```

### Testing and Documentation

So far Bergen does only provide limitedunit-tests and is in desperate need of documentation,
please beware that you are using an Alpha-Version


### Build with

- [Arnheim](https://github.com/jhnnsrs/arnheim)
- [Bergen](https://github.com/jhnnsrs/bergen)
- [Grunnlag](https://github.com/jhnnsrs/grunnlag)
- [Napari](https://github.com/napari/napari)



## Roadmap

This is considered pre-Alpha so pretty much everything is still on the roadmap


## Deployment

Contact the Developer before you plan to deploy this App, it is NOT ready for public release

## Versioning

There is not yet a working versioning profile in place, consider non-stable for every release 

## Authors

* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) 

## Acknowledgments

* EVERY single open-source project this library used (the list is too extensive so far)