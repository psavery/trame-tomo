r"""
Define your classes and create the instances that you need to expose
"""
import logging

from paraview import simple

from .io import read_file
from .tk_utils import open_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine:
    def __init__(self, server):
        self._server = server

        self.sources = []

        # initialize state + controller
        ctrl = server.controller
        state = server.state
        state.change('opacities')(self.print_opacities)

        ctrl.open_file = self.open_file

    def print_opacities(self, opacities, **kwargs):
        print(f'{opacities=}')

    def clear_sources(self):
        while self.sources:
            simple.Delete(self.sources.pop(0))

    def open_file(self):
        selected_file = open_file()
        if not selected_file:
            # User cancelled
            return

        # Read the data file
        data = read_file(selected_file)

        # Clear all sources that have been created
        self.clear_sources()

        # Create the new source
        rep = simple.Show(data)
        self.sources.append(rep)

        # Render it as a volume
        rep.SetRepresentationType("Volume")

        ctrl = self._server.controller

        # Need to push the server change to the client
        ctrl.view_update()

        # Need to get the client to reset camera (otherwise,
        # center of rotation will be off)
        ctrl.reset_camera()
