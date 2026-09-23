class Iso_Surface:
    def __init__(self, session, config):
        self.session = session
        self.sub_config = config or {}

    def create(self):
        for name, surf in self.sub_config.items():
            if not surf:
                continue
            self.session.results.surfaces.iso_surface.create(name)
            self.session.results.surfaces.iso_surface[name].field = surf.get("field")
            self.session.results.surfaces.iso_surface[name] = {
                "iso_values": [surf.get("value")]
            }
        return True
