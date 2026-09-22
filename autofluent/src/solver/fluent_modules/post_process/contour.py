from iso_surface import Iso_Surface

class Contour():
    def __init__(self,session,config) -> None:
        self.session = session
        self.sub_config = config["contour"]
        
    def create(self):
        for contour in self.sub_config:

            contour_name = contour["name"]
            contour_field = contour_name["field"]
            contour_surf =contour["surface"]
            contour_save_file_type = self.sub_config["save_format"]
        
            
            graphics = self.session.settings.results.graphics
            graphics.picture.driver_options.hardcopy_format = contour_save_file_type

            graphics.contour[contour_name] = {
                "field":contour_field ,
                "surfaces_list": [contour_surf],
            }

            graphics.views.auto_scale()

            graphics.picture.save_picture(
                file_name=f"{contour_name}.{contour_save_file_type}"
            )
            
            


