r"""
Define your classes and create the instances that you need to expose
"""
import logging

import numpy as np

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
        state.change('opacities')(self.opacities_modified)

        ctrl.open_file = self.open_file

    def opacities_modified(self, opacities, **kwargs):
        pwf = self.active_opacity_function
        if not pwf:
            return

        opacity_points = opacities['points']

        # Create the list of points we will be using
        points = [0, 0, 0.5, 0] * (len(opacity_points) // 2)

        # Get the scalar opacity ranges on the representation
        pwf_xrange = (pwf.Points[0], pwf.Points[-4])
        pwf_yrange = (pwf.Points[1], pwf.Points[-3])

        # Rescale the points to match
        for i in range(0, len(points), 4):
            points[i] = np.interp(opacity_points[i // 2], (0, 1),
                                  pwf_xrange)
            points[i + 1] = np.interp(opacity_points[i // 2 + 1], (0, 1),
                                      pwf_yrange)

        # Set the new points
        pwf.Points = points

        # Push the update to the client
        ctrl = self._server.controller
        ctrl.view_update()

    @property
    def active_opacity_function(self):
        if not self.sources:
            return None

        source = self.sources[0]
        return source.ScalarOpacityFunction

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
