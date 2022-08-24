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

        data = simple.OpenDataFile(selected_file)
        if data is None:
            raise Exception(f'Failed to find a reader for {selected_file}')

        # Delete the current active source
        simple.Delete()

        # Add the new source
        simple.Show(data)
        simple.ResetCamera()
        simple.Render()

        ctrl = self._server.controller

        ctrl.view_update()
        ctrl.reset_camera()
