import logging

from .engine import Engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------


def initialize(server):
    ctrl = server.controller

    def protocols_ready(**initial_state):
        logger.debug(f">>> ENGINE(b): Server is ready {initial_state}")

    ctrl.on_server_ready.add(protocols_ready)

    engine = Engine(server)
    return engine
