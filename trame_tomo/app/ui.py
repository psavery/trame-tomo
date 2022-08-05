from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, vtk


# Create single page layout type
# (FullScreenPage, SinglePage, SinglePageWithDrawer)
def initialize(server):
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
            vuetify.VSlider(                    # Add slider
                v_model=("resolution", 6),      # bind variable with an initial value of 6
                min=3, max=60,                  # slider range
                dense=True, hide_details=True,  # presentation setup
            )
            with vuetify.VBtn(icon=True, click=ctrl.reset_camera):
                vuetify.VIcon("mdi-crop-free")
            with vuetify.VBtn(icon=True, click=ctrl.reset_resolution):
                vuetify.VIcon("mdi-undo")

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with vtk.VtkView() as vtk_view:                # vtk.js view for local rendering
                    ctrl.reset_camera = vtk_view.reset_camera  # Bind method to controller
                    with vtk.VtkGeometryRepresentation():      # Add representation to vtk.js view
                        vtk.VtkAlgorithm(                      # Add ConeSource to representation
                            vtkClass="vtkConeSource",          # Set attribute value with no JS eval
                            state=("{ resolution }",)          # Set attribute value with JS eval
                        )

        # Footer
        # layout.footer.hide()
