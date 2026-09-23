class Contour:
    def __init__(self, session, config):
        self.session = session
        self.sub_config = config or {}

    def create(self):
        graphics = self.session.settings.results.graphics
        for name, contour in self.sub_config.items():
            if not contour:
                continue
            file_type = contour.get("save_format", "png")
            graphics.picture.driver_options.hardcopy_format = file_type
            graphics.contour[name] = {
                "field": contour.get("field"),
                "surfaces_list": contour.get("surfaces", []),
            }
            graphics.views.auto_scale()
            graphics.picture.save_picture(
                file_name=f"{name}.{file_type}"
            )
        return True
