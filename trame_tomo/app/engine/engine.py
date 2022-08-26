r"""
Define your classes and create the instances that you need to expose
"""
import logging

from paraview import simple

from .tk_utils import open_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine:
    def __init__(self, server):
        self._server = server

        # initialize state + controller
        state, ctrl = server.state, server.controller
        ctrl.open_file = self.open_file
        state.resolution = 6
        ctrl.reset_resolution = self.reset_resolution
        state.change("resolution")(self.on_resolution_change)

    def reset_resolution(self):
        self._server.state.resolution = 6

    def on_resolution_change(self, resolution, **kwargs):
        logger.info(f">>> ENGINE(a): Slider updating resolution to {resolution}")

    def open_file(self):
        selected_file = open_file()
        if not selected_file:
            # User cancelled
            return

        # Save the current source
        current_source = simple.GetActiveSource()

        # FIXME: for a .tif file, this uses a GDAL reader. Why? Why doesn't it
        # just use a TIFFSeriesReader?
        # data = simple.OpenDataFile(selected_file)
        # if data is None:
        #     raise Exception(f'Failed to find a reader for {selected_file}')

        # For now, hard-code the TIFFSeriesReader
        data = simple.TIFFSeriesReader(FileNames=[selected_file])

        # FIXME: this is not working anymore
        # Delete the current active source
        simple.Delete(current_source)

        # Add the new source
        rep = simple.Show(data)

        # Render it as a volume
        rep.SetRepresentationType('Volume')

        ctrl = self._server.controller

        # Need to push the server change to the client
        ctrl.view_update()

        # Need to get the client to reset camera (otherwise,
        # center of rotation will be off)
        ctrl.reset_camera()
