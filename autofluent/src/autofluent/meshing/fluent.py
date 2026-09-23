from pathlib import Path
import os

from .base import Mesher

class Fluent_Mesher(Mesher):

    def __init__(self, session, config):
        super().__init__(session, config)
        self.save_dir = self.config.get("save_dir", {}).get("path")\n        self.meshing_config = self.config.get("meshing", {}) or {}
        self.scdoc_file_path = self.config["geometry"]["file"]
        self.file_name_noext = os.path.basename(self.scdoc_file_path)
        head, _ = os.path.split(self.scdoc_file_path)
        self.dir_name = head
        self.save_path = Path(self.save_dir) if self.save_dir else Path.cwd()
        self.processors = self.config.get("environment", {}).get("resources", {}).get("cpus") 
        self.verbose = self.config["verbose"]["enabled"]
        #self.updates = Updates(self.verbose)
        self.show_gui = self.meshing_config.get("show_gui", False)
        self.session = session

        
    def initialise_workflow(self):
        self.workflow = self.session.watertight()
        print("INIT: workflow initiated")
        return True

    def load_geometry(self):
        self.import_geom = self.workflow.import_geometry

        #params
        self.import_geom.file_name.set_state(self.scdoc_file_path) #scdocs only work for Windows machines
        #self.import_geom.file_format.set_state("CAD")
        self.import_geom.length_unit.set_state('mm')
        self.import_geom()

        print("LOAD GEOMETRY: complete")
        return True
    
    def setup(self):
        self.add_local_sizings()
        self.create_surface_mesh()
        self.describe_geom()
        self.invoke_share_topology()
        self.update_regions()
        self.update_boundaries()
        self.add_BL()

        print("MESH SETUP: complete")
        return True


    def add_local_sizings(self):
        # Add Local Face Sizing

        """ REFERENCE
        _datamodel.AddLocalSizingWTM
        or 
        self._add_local_sizing.Arguments.help()
        """
        
        self.add_local_sizing = self.workflow.add_local_sizing

        for i in range(len(self.config["meshing"]["local_sizing"])):

            curr_local_sizing = self.config["meshing"]["local_sizing"][i]
            #self.append_default_values(taskObject=self._add_local_sizing,variables= facesize)
            self.add_local_sizing.add_child = "yes"
            self.add_local_sizing.boi_execution = curr_local_sizing["type"]#'Face Size' wt.add_local_sizing.boi_execution.allowed_values() to get allowed values
            self.add_local_sizing.boi_zoneor_label = 'label'
            self.add_local_sizing.boi_control_name = curr_local_sizing["name"]
            self.add_local_sizing.boi_growth_rate =  curr_local_sizing["growth_rate"]
            self.add_local_sizing.boi_size =  curr_local_sizing["target_mesh_size"]
            self.add_local_sizing.boi_face_label_list =  curr_local_sizing["face_label_list"]
            self.add_local_sizing.add_child_and_update()

        print("local sizings added")
        return True


    def create_surface_mesh(self):
        # Add Surface Mesh Sizing

        """ REFERENCE
        _datamodel.AddLocalSizingWTM()
        """
        surface_mesh_params = self.config["meshing"]["surface_mesh"]

        self.generate_surface_mesh = self.workflow.create_surface_mesh
        self.surf_mesh_controls =  self.generate_surface_mesh.cfd_surface_mesh_controls
     
        self.surf_mesh_controls.min_size = surface_mesh_params["min_size"]
        self.surf_mesh_controls.max_size = surface_mesh_params["max_size"]
        self.surf_mesh_controls.growth_rate = surface_mesh_params["growth_rate"]                                                                          #check
        self.surf_mesh_controls.size_functions = surface_mesh_params["size_functions"]
        self.surf_mesh_controls.curvature_normal_angle =surface_mesh_params["curvature_normal_angle"]
        self.surf_mesh_controls.cells_per_gap = surface_mesh_params["cells_per_gap"]
        self.surf_mesh_controls.scope_proximity_to.default_value() #default values 
        self.generate_surface_mesh()

        print("surface mesh complete")
        return True

   
    def describe_geometry(self):
            """ REFERENCE
            _datamodel.GeometrySetup()
            """
            
            self.describe_geom=self.workflow.describe_geometry
            self.describe_geom.setup_type = "The geometry consists of only fluid regions with no voids"
            self.describe_geom.capping_required = "No"
            self.describe_geom.wall_to_internal = "Yes"
            self.describe_geom.invoke_share_topology = "No"
            self.describe_geom.multizone = "No"

            self.describe_geom()
            
            print("Describe Geometry Done")
            return True
            
            

    def invoke_share_topology(self):
        """
        _datamodel.ShareTopology()
             self.s_topology.Arguments = dict(
            "GapDistance": ,#float
            "GapDistanceConnect":,#float
            "STMinSize":,#float
            "InterfaceSelect":,#str
            "EdgeLabelslist":,#[str]
            "ShareTopologyPreferences":,#dict[str, Any]
            "SMImprovePreferences":,#dict[str, Any]
            "SurfaceMeshPreferences":,#dict[str, Any]
    """
        if not self.describe_geom.invoke_share_topology:
            return False
        
        self.share_topology = self.workflow.apply_share_topology
        self.share_topology.gap_distance.default_value()

        sim_params = self.share_topology.get_state() #get default values from here then adjust according to 
        self.share_topology()
        
        print("Share Topology activated")
        return True


    def update_boundaries_and_regions(self):
        #update boundaries
        """
        allowed boundary types: 
            velocity-inlet, pressure-outlet, pressure-inlet, pressure-far-field, mass-flow-inlet, mass-flow-outlet, 
            outflow, symmetry, wall, internal, interface, overset, outlet-vent, intake-fan, inlet-vent, exhaust-fan, 
            porous-jump, fan, radiator, multiple-types
        """
        self.update_boundaries = self.workflow.update_boundaries

        self.update_boundaries()
        self.update_boundaries.revert()

        boundaries_args = self.update_boundaries.arguments()

        boundary_list = self.update_boundaries.boundary_current_list()
        boundary_types = self.update_boundaries.boundary_current_type_list()

        new_boundary_types = boundary_types

        for i, (name, _) in enumerate(zip(boundary_list, boundary_types)):
            if name == "inlet":
                new_boundary_types[i] ='pressure-inlet'
            elif name == 'outlet':
                new_boundary_types[i] ='mass-flow-outlet'
        
        boundary_list = [i for i in boundary_list]
        boundary_types = [i for i in boundary_types]
        new_boundary_types = [i for i in new_boundary_types]

        """
        _datamodel.UpdateRegions()
        """

        self.update_regions = self.workflow.update_regions
        self.update_regions()

        self.update_regions.region_current_list.default_value()
        self.update_regions.region_current_type_list.default_value()

        region_list = self.update_regions.region_current_list()
        region_types = self.update_regions.region_current_type_list()
        
        print("Boundaries/Regions updated")
        return True

           
    def add_BL(self):
        # Add Boundary Layers

        BL_params = self.config.get("boundary_layer", {})
        self.add_boundary_layers = self.workflow.TaskObject["Add Boundary Layers"]
        self.add_boundary_layers.AddChildToTask()
        self.add_boundary_layers.InsertCompoundChildTask()
        self.workflow.TaskObject["smooth-transition_1"].Arguments.update_dict(
            {
                "BLControlName": "smooth-transition_1",
                "NumberOfLayers": BL_params["number_of_layers"],
                "Rate": BL_params["growth_rate"],
                "TransitionRatio": BL_params["transition_ratio"],
            }
        )
        self.add_boundary_layers.Execute()

        print("BL generated")
        return True


    def generate_mesh(self):
    # Generate the Volume Mesh
    
        self.generate_volume_mesh = self.workflow.TaskObject["Generate the Volume Mesh"]
        self.generate_volume_mesh.Arguments.update_dict({"VolumeFill": f"{self.config.get("cell_type")}"})
        self.generate_volume_mesh.Execute()
        
        print("GENERATE MESH: complete")
        return True
    
    def check_mesh(self):
        pass

    def save_mesh(self):
        pass
    
    
    def run(self):
        self.initialise_workflow()
        self.load_geometry()
        self.add_local_sizings()
        self.create_surface_mesh()
        self.describe_geometry()
        self.invoke_share_topology()
        self.update_regions()
        self.update_boundaries()
        self.add_BL()
        self.generate_mesh()
        self.save_mesh() 

        print("FLUENT: Mesh Generated")
        return True

    
            

