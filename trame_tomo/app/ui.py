from paraview import simple

from trame.ui.vuetify import SinglePageLayout
from trame.widgets import paraview, vuetify


def initialize(server):
    # Create our view
    view = simple.CreateView('RenderView')

    state, ctrl = server.state, server.controller
    state.trame__title = "Trame Tomo"

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("Trame / vtk.js")
        with layout.toolbar:
            with vuetify.VBtn(
                icon=True, click=ctrl.open_file, small=True, classes="mx-4"
            ):
                vuetify.VIcon("mdi-folder-file-outline")

            vuetify.VSpacer()
            with vuetify.VBtn(icon=True, click=ctrl.reset_camera):
                vuetify.VIcon("mdi-crop-free")

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = paraview.VtkRemoteView(view, ref="view")
                ctrl.reset_camera = html_view.reset_camera
                ctrl.view_update = html_view.update
