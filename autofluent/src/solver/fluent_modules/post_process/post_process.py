from .contour import Contour
from .iso_surface import Iso_Surface

class Post_Process():
    def __init__(self) -> None:
        pass
    
    def setup(self, session,config):

        self.session = session
        #cleaning the config of unset variables
        for name, value in config.items(): 

            method = getattr(self,f"set_{name}",None)

            if method:
                method(self.session, value[name])
    
    def set_iso_surface(self,session,config):
        self.iso_surface = Iso_Surface(session, config)
        self.iso_surface.create()
        
    def set_contour(self,session,config):
        self.contour = Contour(session,config)
        self.contour.create()
    
