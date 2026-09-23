from .contour import Contour
from .iso_surface import Iso_Surface


class Post_Process:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        if not config.get("enabled", False):
            return True

        iso_surfaces = config.get("iso_surfaces", {}) or {}
        if iso_surfaces:
            Iso_Surface(session, iso_surfaces).create()

        contours = config.get("contours", {}) or {}
        if contours:
            Contour(session, contours).create()

        return True
