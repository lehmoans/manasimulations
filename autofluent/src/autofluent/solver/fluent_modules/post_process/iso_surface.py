class Iso_Surface():
    def __init__(self, session, sub_config) -> None:
        self.session = session
        self.sub_config = sub_config

    def create(self):
        for surf in self.sub_config:
            surf_name=surf["name"]
            self.session.results.surfaces.iso_surface.create(surf_name)
            self.session.results.surfaces.iso_surface[surf_name].field = surf["field"]
            self.session.results.surfaces.iso_surface[surf_name] = {"iso_values": [surf["value"]]}
