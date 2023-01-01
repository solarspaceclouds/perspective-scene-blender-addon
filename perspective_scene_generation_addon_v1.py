"""
# DO EMISSION SYSTEM TO AVOID COLLISIONS! 

ADDITIONAL: path option available for forest and field and desert

custom specification of num of particles for each object in the respective environment collection 

set up perspective options (dropdown list options)
if near & top left
if moderate & top left
... 
if far & bottom right

# ADDITIONAL CHALLENGE: 
perspective options: (continuous)
    distance specification (in metres) & top left
    ...
    distance specification (in metres) & bottom right)

# ADDITIONAL: 
CUSTOM ENVIRONMENT from CUSTOM objects you want to import to be included in the custom physical environment collection


# Available feature: variable camera angle + the rest of the params adjusted
"""

bl_info = {
    "name":"Perspective Scene addon",
    "author": "Solarspaceclouds",
    "version": (1,0),
    "blender": (3, 1,2),
    "location":"View3D > N",
    "description": "Creates Custom Scene with Subject in Camera Perspective",
    "warning": "",
    "doc_url":"",
    "category": "Add Mesh",
}

import bpy
from math import inf
from mathutils.geometry import intersect_line_plane as ilp

from mathutils import Vector
from mathutils.bvhtree import BVHTree

import bpy
from bpy import context, data, ops
from math import radians, pi, sin, cos, sqrt
import os
import random
import pickle
import sys
import json

from bpy_extras.object_utils import world_to_camera_view
from bpy_extras.view3d_utils import location_3d_to_region_2d
import random
from mathutils import Vector
import glob
import datetime, calendar

class generateScenePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Perspective Scene Generation"
    bl_idname = "persp_scene_gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Perspective Scene"

    def draw(self, context):
        layout = self.layout
 
        layout.operator("wm.template_operator")

         
class ADDONOPTIONS(bpy.types.Operator):
    """
    <subjejct> in a <env>
    """
    
    bl_label = "Generate Scene"
    bl_idname = "wm.template_operator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Perspective Scene"
    
    
    min_x_rotation = 30
    max_x_rotation = 60
    camera_x_rotation : bpy.props.IntProperty(
        name = "camera x rotation",
        description = "camera rotation from verticle downwards default state",
        min = min_x_rotation,
        max = max_x_rotation,
        default = 45,
    )

    particle_count : bpy.props.IntProperty(
        name = "particles count",
        description = "number of environment particles",
        min = 10,
        max = 500,
        default = 50,
    )
    
    particle_scale : bpy.props.FloatProperty(
        name = "particle scale",
        description = "size of environment particles",
        min = 0.2,
        max = 5.0,
        default = 0.2,
    )

    dist_enum : bpy.props.EnumProperty( 
        # further refine in future: let the scene take more than 1 subject object (i.e. duplicate the subject object? or make particle system) 
        
        name = "Dist From Camera",
        description = "Shortest distance from plane to Camera",
        items = [ # list of available objects to use as SUBJECT mesh
            ('NEAR', 'Near', 'Adjust camera to be near the plane'),
            ('MODERATE', 'Moderate', 'Adjust camera to be moderate distance from the plane'),
            ('FAR', 'Far', 'Adjust camera to be far from the plane')
        ]
    )
    
    min_subject_qty = 1
    max_subject_qty = 3
    subject_qty : bpy.props.IntProperty(
        name = "Subject Quantity",
        description = "Number of subject mesh object in scene",
        min = min_subject_qty,
        max = max_subject_qty,
        default = 1
    )
    
    quadrant_enum : bpy.props.EnumProperty(
        name = "Quadrant",
        description = "Select an option",
        items = [
            ('TL', 'top left', 'Shift camera view to position subject in top left quadrant (Q1)'),
            ('TM', 'top middle', 'Shift camera view to position subject in top middle quadrant (Q2)'),
            ('TR', 'top right', 'Shift camera view to position subject in top left quadrant (Q3)'),
            ('ML', 'middle left', 'Shift camera view to position subject in middle left quadrant (Q4)'),
            ('MM', 'middle middle', 'Shift camera view to position subject in middle middle quadrant (Q5)'),
            ('MR', 'middle right', 'Shift camera view to position subject in middle left quadrant (Q6)'),           
            ('BL', 'bottom left', 'Shift camera view to position subject in bottom left quadrant (Q4)'),
            ('BM', 'bottom middle', 'Shift camera view to position subject in bottom middle quadrant (Q5)'),
            ('BR', 'bottom right', 'Shift camera view to position subject in bottom left quadrant (Q6)'),            
        ]
    )
    
    generate_sample_coll : bpy.props.BoolProperty(
        name="Generate Example Collection",
        description="Generate an example collection",
        default = False
        ) 
    use_sample_coll : bpy.props.BoolProperty(
        name="Use Example Collection",
        description="Use the example collection",
        default = False
        ) 
    render_image : bpy.props.BoolProperty(
        name="Render image",
        description="Render an image of the generated camera view/scene",
        default = True
        ) 
    colour_1 : bpy.props.FloatVectorProperty(
        name = "Colour 1",
        description = "Colour of the ground",
        default = (0.0, 0.0313828,0.0) #dark green
#        (0,0.0313828,0,1) # dark green
#        (0.045,0,0,1) # dark brown
        )
    colour_2 : bpy.props.FloatVectorProperty(
        name = "Colour 2",
        description = "Colour of the ground",
        default = (0.045, 0.0,0.0)
        )
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context): # the UI of the panel
        scene = bpy.context.scene
        layout = self.layout
        layout.label(text=" Subject properties:")
        layout.prop_search(scene, "theChosenObject", scene, "objects")
        layout.prop(self, "quadrant_enum")
        layout.prop(self, "subject_qty")
        layout.prop(self, "dist_enum")
                        
        layout.label(text=" Environment properties:")
        layout.prop(context.scene, "env_coll")
        row = layout.row()
        row.prop(self, "particle_count") # SUBJECT distance from camera (in metres)
        row.prop(self, "particle_scale") # SUBJECT distance from camera (in metres)
        layout.prop(self, "generate_sample_coll")
        layout.prop(self, "use_sample_coll")
        
        layout.label(text=" Perspective properties:")
        layout.prop(self, "camera_x_rotation") # SUBJECT distance from camera (in metres)
        
        layout.label(text= " Render Image:")
        layout.prop(self, "render_image")

        layout.label(text= " Base Plane Colours:")
        layout.prop(self, "colour_1")
        layout.prop(self, "colour_2")

    def remove_camera_markers(self, torus_coll):
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        # deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

#        objects = bpy.data.objects
        for obj in torus_coll:
            if obj.name.startswith("Torus"):
                obj.select_set(True)
                bpy.ops.object.delete()
        return
                
    def set_camera(self):
        d=0
        d_near_range = random.randint(75,126)
        d_mid_range = random.randint(126,176)
        d_far_range = random.randint(176,226)
#                
        camera = bpy.context.scene.objects.get("Camera",None)
        if camera == None:
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(100, 0, 70), rotation=(0, 0, 90), scale=(1, 1, 1))
        camera = bpy.context.scene.camera
        camera.rotation_euler = (radians(self.camera_x_rotation),0,radians(90))
#        
        if self.dist_enum =='NEAR':
            d = d_near_range
            print("NEAR\n")

        elif self.dist_enum == "MODERATE":
            d = d_mid_range
            print("MODERATE\n")

        elif self.dist_enum=="FAR":
            d = d_far_range
            print("FAR\n")
       
        z_dist = d*cos(radians(self.camera_x_rotation))
        x_dist = sqrt(d**2 - z_dist**2)

        # Adjust camera x location
        camera.location[0] = x_dist
        # Adjust camera z location
        camera.location[2] = z_dist
        
        # set camera clipping values
        camera.data.clip_start = 0.001
        camera.data.clip_end = 10000
  
        return
    
    def mark_cam_edges(self, context):
        context = bpy.context    
        scene = context.scene
        # Global XY plane
        plane_co = (0, 0, 0)
        plane_no = (0, 0, 1)        

        cam = scene.camera
        mw = cam.matrix_world
        o = mw.translation

        camdata = cam.data

        tr, br, bl, tl = [
        mw @ f for f in camdata.view_frame(scene=scene)]
        # offset vectors from bl.
        # eg middle would be bl + 0.5 * (x + y) 
        x = tr - tl
        y = tr - br

        coords = []
        for image_coord in ((0, 0), (1, 0), (1, 1), (0, 1)):
            cx, cy = image_coord
            # vector pointing from cam origin thru image point (PERSP)
            v = (bl + (cx * x + cy * y)) - o

            pt = ilp(o, o +  v, plane_co, plane_no, True)
            if pt:
#                print("Adding cube at ", pt)
#                bpy.ops.mesh.primitive_cube_add(
#                        location=pt,
#                        )
                coords.append(pt)  

        print("cam_view_coords:", coords)
        
        x_set = set()
        y_set = set()
        for coord in coords:
            x_set.add(round(coord[0],3))
            y_set.add(round(coord[1],3))
            
        print("x_set:", x_set)
        print("y_set:", y_set)
        x_set = sorted(x_set)
        y_set = sorted(y_set)

        print("sorted x", x_set)
        print("sorted y", y_set)
        
#        return x_set, y_set, camera_viewer
        return x_set, y_set
    
    def create_camera_viewplane(self, coords):
        context = bpy.context
        cam = bpy.context.scene.camera
        name = f"{cam.name}_ViewPlane"
        me = bpy.data.meshes.new(name)
        faces = [range(len(coords))] if len(coords) > 2 else []
        me.from_pydata(coords, [], faces)
        ob = bpy.data.objects.new(name, me)
        context.collection.objects.link(ob)
                
        camera_viewer = ob
        return camera_viewer


    def create_subject_instances(self, subject_choice, subject_x_loc_min_lim, subject_x_loc_max_lim, subject_y_loc_min_lim, subject_y_loc_max_lim):
        objects = bpy.data.objects
        #CREATE SUBJECT INSTANCE COLLECTION
        si_coll = bpy.data.collections.new("Subject instance collection")
        bpy.context.scene.collection.children.link(si_coll)

        # note: duplicate subjects were instantiated in 'Subject choices' collection initially
        # want to move the duplicated subjects to 'Subject instance collection' collection

        bpy.ops.object.select_all(action='DESELECT')
       
        subject_instances = []
        for i in range(len(objects)): 
            if (objects[i].name.startswith(subject_choice.name) and objects[i].name!= subject_choice.name): # want a match but don't want the exact match
                objects[i].select_set(True)
#                sc_coll.objects.unlink(objects[i])
#                bpy.ops.object.move_to_collection(si_coll)

        for obj in bpy.context.selected_objects:
            for other_col in obj.users_collection:
                other_col.objects.unlink(obj)
            if obj.name not in si_coll.objects:
                si_coll.objects.link(obj)
                    
        return si_coll
    
    def prevent_subjects_collision(self, si_coll,subject_x_loc_min_lim, subject_x_loc_max_lim, subject_y_loc_min_lim, subject_y_loc_max_lim):
        # to instantiate all the subject choice instances in the same quadrant
        for sub in si_coll.objects:
            sub.location[0] = random.uniform(subject_x_loc_min_lim, subject_x_loc_max_lim)
            sub.location[1] = random.uniform(subject_y_loc_min_lim, subject_y_loc_max_lim) 
        
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7)]
        
        for i in range(len(si_coll.objects)):
            j = (i+1) % len(si_coll.objects)
            obj1 = si_coll.objects[i]
            obj2 = si_coll.objects[j]
              
            vert1 = [obj1.matrix_world @ Vector(corner) for corner in obj1.bound_box]
            vert2 = [obj2.matrix_world @ Vector(corner) for corner in obj2.bound_box]

            bvh1 = BVHTree.FromPolygons(vert1, faces)
            bvh2 = BVHTree.FromPolygons(vert2, faces)

            if bool(bvh1.overlap(bvh2)) == True: # if have at least 1 collision (i.e. 2 subject instances colliding with each other)
                self.prevent_subjects_collision(self, si_coll)
        return
    
    def rotate_subject_instances(self):
        """ rotate all subjects in scene about the z axis"""
        # angle to rotate tank about z axis
        col = bpy.data.collections["Subject instance collection"].objects
        for obj in col:
            deg = random.randrange(10,350,1)
            obj.rotation_euler[2] += deg
        return 

    def generate_sample_collection(self):
        bpy.ops.object.select_all(action='DESELECT')
        
        if self.generate_sample_coll == True:
            env_coll = bpy.data.collections.get("Environment Collection", None)
            if env_coll == None:
                env_coll = bpy.data.collections.new("Environment Collection")
                bpy.context.scene.collection.children.link(env_coll)
                bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-3.48966, -0.885505, 0.001297), scale=(1, 1, 1))
                bpy.context.selected_objects[-1].name = "EnvObj1" 
                bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(-3.48966, -0.885505, 0.001297), scale=(1, 1, 1))
                bpy.context.selected_objects[-1].name = "EnvObj2"
                
                for obj in bpy.data.objects:
                    if obj.name in ["EnvObj1", "EnvObj2"]:
                        for other_col in obj.users_collection:
                            other_col.objects.unlink(obj)
                        if obj.name not in env_coll.objects:
                            env_coll.objects.link(obj)
            
            # Use the generate sample collection as the environment collection:
            if self.use_sample_coll == True:
                bpy.data.scenes["Scene"].env_coll = env_coll
        bpy.ops.object.select_all(action='DESELECT')
        return 

            
            
    def execute(self, context): # here is what happens when the 'Generate Scene' button is pressed
        # INITIAL SET-UP : Clear default objects in blender3D (General Scene)
       
        ## set up render settings 
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'JPEG' # set output format to .jpg
        """ 
        START OF GENERATING BASE MODEL FOR THE FIRST TIME (3D MODEL INSTANTIATION)
        """ 
        
        hasGPU = bpy.context.preferences.addons["cycles"].preferences.has_active_device()
        if hasGPU == True:
            bpy.data.scenes["Scene"].render.engine = 'CYCLES'
            bpy.data.scenes["Scene"].cycles.device = 'GPU'
        else:
            bpy.data.scenes["Scene"].render.engine = "BLENDER_EEVEE"
            bpy.data.scenes["Scene"].eevee.use_ssr = True # enable screen space reflections for rendering
            bpy.context.scene.eevee.use_gtao = True
        # needed to rescale 2d pixel coordinates later


        render = bpy.context.scene.render
        render.resolution_x = 1920
        render.resolution_y = 1080

        # to change viewport clip end value
        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                for s in a.spaces:
                    if s.type == 'VIEW_3D':
                        s.clip_start = 0.01
                        s.clip_end =600
                        

        bpy.data.scenes["Scene"].cursor.rotation_mode = 'QUATERNION'

        # to remove all unused materials/particle systems
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        
        
        bpy.ops.object.select_all(action='DESELECT')
        
        sun = bpy.data.objects.get("Sun", None)
        if sun==None:
            bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 100), scale=(1, 1, 1))
        bpy.data.objects["Sun"].location[2] = 100

        # if have existing Camera_ViewPlane object, delete it
        for obj in bpy.data.objects:
            if obj.name == "Camera_ViewPlane":
                bpy.data.objects.remove(obj, do_unlink=True)
                
        # if have an existing 'Subject instances collection', delete it
        for col in bpy.data.collections:
            if col.name == "Subject instance collection":
                for obj in col.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    
                bpy.data.collections.remove(col)
        
        collection = bpy.data.collections["Collection"].objects

        self.set_camera()
            
        #subject instantiation
        subject_name = bpy.data.scenes["Scene"].theChosenObject
        subject_choice = bpy.data.objects[subject_name]
        
        x_set, y_set = self.mark_cam_edges(context)
#        # get relevant ranges for subject instantiation

        x_top_lim = x_set[0]
        x_bot_lim = x_set[1]
        x_range = x_bot_lim - x_top_lim
        x_one_third = x_top_lim + x_range/3
        x_two_thirds = x_top_lim + 2 * x_range/3
        
        y_left_top_lim = y_set[0]
        y_left_bot_lim = y_set[1]
        y_right_bot_lim = y_set[2]
        y_right_top_lim = y_set[3]              
        
        # continue x and y definitions for relevant ranges (9-section grid) 
        y_left_range = y_left_bot_lim - y_left_top_lim
        y_right_range = y_right_bot_lim - y_right_top_lim # note this is -ve

        y_left_one_third = y_left_top_lim + y_left_range/3
        y_left_two_thirds = y_left_top_lim + 2 * y_left_range/3
        y_right_one_third = y_right_top_lim + y_right_range/3
        y_right_two_thirds = y_right_top_lim + 2 * y_right_range/3
        y_right_bot_lim = y_right_top_lim + y_right_range
        y_left_bot_lim = y_left_top_lim + y_left_range
        
        top_x_min = x_top_lim
        top_x_max = x_one_third
        mid_x_min = x_one_third
        mid_x_max = x_two_thirds
        bot_x_min = x_two_thirds
        bot_x_max = x_bot_lim
        
        y_top_range = y_right_top_lim - y_left_top_lim
        y_one_third_range = y_right_one_third - y_left_one_third
        y_two_thirds_range = y_right_two_thirds - y_left_two_thirds
        y_bot_range = y_right_bot_lim - y_left_bot_lim
        
        tl_y_min = y_left_one_third
        tl_y_max = y_left_top_lim + y_top_range/3
        tm_y_min = y_one_third_range/3 + y_left_one_third
        tm_y_max = 2 * y_one_third_range/3 + y_left_one_third
        tr_y_min = 2 * y_top_range/3 + y_left_top_lim
        tr_y_max = y_right_one_third
        
        ml_y_min = y_left_two_thirds
        ml_y_max = y_one_third_range/3 + y_left_one_third
        mm_y_min = y_two_thirds_range/3 + y_left_two_thirds
        mm_y_max = 2 * y_two_thirds_range /3 + y_left_two_thirds
        mr_y_min = 2 * y_one_third_range/3 + y_left_one_third
        mr_y_max = y_right_two_thirds
        
        bl_y_min = y_left_bot_lim
        bl_y_max = y_two_thirds_range/3 + y_left_two_thirds
        bm_y_min = y_bot_range/3 + y_left_bot_lim
        bm_y_max = 2 * y_bot_range/3 + y_left_bot_lim
        br_y_min = 2 * y_two_thirds_range /3 + y_left_two_thirds
        br_y_max = y_right_bot_lim
        
        # rescale the main plane
        subject_x_loc_min_lim = 0
        subject_x_loc_max_lim = 0
        subject_y_loc_min_lim = 0
        subject_y_loc_max_lim = 0
        
        # subject instantiation position
        if self.quadrant_enum == "TL":
            # TOP LEFT
            # subject is on top left
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tl_y_min
            subject_y_loc_max_lim = tl_y_max
                        
        if self.quadrant_enum == "TM":
            # TOP MIDDLE
            # subject is on top middle
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tm_y_min
            subject_y_loc_max_lim = tm_y_max
            
        if self.quadrant_enum == "TR":
            # TOP RIGHT
            # subject is on top right
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tr_y_min
            subject_y_loc_max_lim = tr_y_max
            
        if self.quadrant_enum == "ML":
            # MIDDLE LEFT
            # subject is on middle left
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = ml_y_min
            subject_y_loc_max_lim = ml_y_max
            
        if self.quadrant_enum == "MM":
            # MIDDLE MIDDLE
            # subject is on middle middle
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = mm_y_min
            subject_y_loc_max_lim = mm_y_max
            
        if self.quadrant_enum == "MR":
            # MIDDLE RIGHT
            # subject is on middle right
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = mr_y_min
            subject_y_loc_max_lim = mr_y_max
            
        if self.quadrant_enum == "BL":
            # BOTTOM LEFT
            # subject is on bottom left
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = bl_y_min
            subject_y_loc_max_lim = bl_y_max
            
        if self.quadrant_enum == "BM":
            # BOTTOM MIDDLE
            # subject is on bottom middle
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = bm_y_min
            subject_y_loc_max_lim = bm_y_max
            
        if self.quadrant_enum == "BR":
            # BOTTOM RIGHT
            # subject is on bottom right
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = br_y_min
            subject_y_loc_max_lim = br_y_max
            
        objects = bpy.data.objects
       
        # deselect all objects
        for i in range(len(bpy.data.objects)):
            bpy.data.objects[i].select_set(False)    
 
        # to select the object in the 3D viewport/outliner,
        bpy.data.objects[subject_choice.name].select_set(True)
        # to make plane as active object
        bpy.context.view_layer.objects.active = bpy.data.objects[subject_choice.name]
        
        for i in range(self.subject_qty):
               bpy.ops.object.duplicate_move()    
        
        context = bpy.context    
        scene = context.scene
        # Global XY plane
        plane_co = (0, 0, 0)
        plane_no = (0, 0, 1)        
        cam = scene.camera
        mw = cam.matrix_world
        o = mw.translation
        camdata = cam.data
        tr, br, bl, tl = [
        mw @ f for f in camdata.view_frame(scene=scene)]
        # offset vectors from bl.
        # eg middle would be bl + 0.5 * (x + y) 
        x = tr - tl
        y = tr - br
        #        # roll around in CCW direction
        coords_2 = []
        counter = 0
        torus_coll = []
        for image_coord in ((0, 0), (0, 1), (1, 0), (1, 1)):
            counter+=1
            cx, cy = image_coord
            # vector pointing from cam origin thru image point (PERSP)
            v = (bl + (cx * x + cy * y)) - o
            pt = ilp(o, o +  v, plane_co, plane_no, True)               
            if pt and (pt - o).dot(v) > 0:
                print("Adding torus at ", pt)
                bpy.ops.mesh.primitive_torus_add(
                        location=pt,
                        )
                torus = bpy.context.view_layer.objects.active
                torus_coll.append(torus)
                coords_2.append(pt)
            elif pt and (pt - o).dot(v) < 0:
                print("BEHIND THE CAMERA")
            else:
                print("NOT POSSIBLE")       
        print("COORDS_2:", coords_2)
        
        x_set_2 = set()
        y_set_2 = set()
        for coord in coords_2:
            x_set_2.add(round(coord[0],3))
            y_set_2.add(round(coord[1],3))
            
        print("x_set:", x_set_2)
        print("y_set:", y_set_2)
        x_set_2 = sorted(x_set_2)
        y_set_2 = sorted(y_set_2)

        print("sorted x", x_set_2)
        print("sorted y", y_set_2)
        
        x_set = x_set_2
        y_set = y_set_2
        
        # instantiate subjects within the context of/using the camera view! 
        x_top_lim = x_set[0]
        x_bot_lim = x_set[1]
        x_range = x_bot_lim - x_top_lim
        x_one_third = x_top_lim + x_range/3
        x_two_thirds = x_top_lim + 2 * x_range/3
        
        y_left_top_lim = y_set[0]
        y_left_bot_lim = y_set[1]
        y_right_bot_lim = y_set[2]
        y_right_top_lim = y_set[3]              
        
        # continue x and y definitions for relevant ranges (9-section grid) 
        y_left_range = y_left_bot_lim - y_left_top_lim
        y_right_range = y_right_bot_lim - y_right_top_lim # note this is -ve

        y_left_one_third = y_left_top_lim + y_left_range/3
        y_left_two_thirds = y_left_top_lim + 2 * y_left_range/3
        y_right_one_third = y_right_top_lim + y_right_range/3
        y_right_two_thirds = y_right_top_lim + 2 * y_right_range/3
        y_right_bot_lim = y_right_top_lim + y_right_range
        y_left_bot_lim = y_left_top_lim + y_left_range
        
        top_x_min = x_top_lim
        top_x_max = x_one_third
        mid_x_min = x_one_third
        mid_x_max = x_two_thirds
        bot_x_min = x_two_thirds
        bot_x_max = x_bot_lim
        
        y_top_range = y_right_top_lim - y_left_top_lim
        y_one_third_range = y_right_one_third - y_left_one_third
        y_two_thirds_range = y_right_two_thirds - y_left_two_thirds
        y_bot_range = y_right_bot_lim - y_left_bot_lim
        
        tl_y_min = y_left_one_third
        tl_y_max = y_left_top_lim + y_top_range/3
        tm_y_min = y_one_third_range/3 + y_left_one_third
        tm_y_max = 2 * y_one_third_range/3 + y_left_one_third
        tr_y_min = 2 * y_top_range/3 + y_left_top_lim
        tr_y_max = y_right_one_third
        
        ml_y_min = y_left_two_thirds
        ml_y_max = y_one_third_range/3 + y_left_one_third
        mm_y_min = y_two_thirds_range/3 + y_left_two_thirds
        mm_y_max = 2 * y_two_thirds_range /3 + y_left_two_thirds
        mr_y_min = 2 * y_one_third_range/3 + y_left_one_third
        mr_y_max = y_right_two_thirds
        
        bl_y_min = y_left_bot_lim
        bl_y_max = y_two_thirds_range/3 + y_left_two_thirds
        bm_y_min = y_bot_range/3 + y_left_bot_lim
        bm_y_max = 2 * y_bot_range/3 + y_left_bot_lim
        br_y_min = 2 * y_two_thirds_range /3 + y_left_two_thirds
        br_y_max = y_right_bot_lim
                
        subject_x_loc_min_lim = 0
        subject_x_loc_max_lim = 0
        subject_y_loc_min_lim = 0
        subject_y_loc_max_lim = 0
        
        # subject instantiation position
        if self.quadrant_enum == "TL":
            # TOP LEFT
            # subject is on top left
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tl_y_min
            subject_y_loc_max_lim = tl_y_max
                        
        if self.quadrant_enum == "TM":
            # TOP MIDDLE
            # subject is on top middle
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tm_y_min
            subject_y_loc_max_lim = tm_y_max
            
        if self.quadrant_enum == "TR":
            # TOP RIGHT
            # subject is on top right
            subject_x_loc_min_lim = top_x_min
            subject_x_loc_max_lim = top_x_max
            subject_y_loc_min_lim = tr_y_min
            subject_y_loc_max_lim = tr_y_max
            
        if self.quadrant_enum == "ML":
            # MIDDLE LEFT
            # subject is on middle left
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = ml_y_min
            subject_y_loc_max_lim = ml_y_max
            
        if self.quadrant_enum == "MM":
            # MIDDLE MIDDLE
            # subject is on middle middle
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = mm_y_min
            subject_y_loc_max_lim = mm_y_max
            
        if self.quadrant_enum == "MR":
            # MIDDLE RIGHT
            # subject is on middle right
            subject_x_loc_min_lim = mid_x_min
            subject_x_loc_max_lim = mid_x_max
            subject_y_loc_min_lim = mr_y_min
            subject_y_loc_max_lim = mr_y_max
            
        if self.quadrant_enum == "BL":
            # BOTTOM LEFT
            # subject is on bottom left
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = bl_y_min
            subject_y_loc_max_lim = bl_y_max
            
        if self.quadrant_enum == "BM":
            # BOTTOM MIDDLE
            # subject is on bottom middle
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = bm_y_min
            subject_y_loc_max_lim = bm_y_max
            
        if self.quadrant_enum == "BR":
            # BOTTOM RIGHT
            # subject is on bottom right
            subject_x_loc_min_lim = bot_x_min
            subject_x_loc_max_lim = bot_x_max
            subject_y_loc_min_lim = br_y_min
            subject_y_loc_max_lim = br_y_max
            
        objects = bpy.data.objects

        # deselect all objects
        for i in range(len(bpy.data.objects)):
            bpy.data.objects[i].select_set(False)    
 
        # to select the object in the 3D viewport/outliner,
        bpy.data.objects[subject_choice.name].select_set(True)
        # to make plane as active object
        bpy.context.view_layer.objects.active = bpy.data.objects[subject_choice.name]
               
        si_coll = self.create_subject_instances(subject_choice, subject_x_loc_min_lim, subject_x_loc_max_lim, subject_y_loc_min_lim, subject_y_loc_max_lim )
        self.prevent_subjects_collision(si_coll, subject_x_loc_min_lim, subject_x_loc_max_lim, subject_y_loc_min_lim, subject_y_loc_max_lim)
        
        self.rotate_subject_instances()
        
        
        self.generate_sample_collection()

        # choose environment template for background objects collection instantiation
        
        col = bpy.data.scenes["Scene"].env_coll

        
        # deselect all objects
        for i in range(len(bpy.data.objects)):
            bpy.data.objects[i].select_set(False)
            
     
        coords_2 = [coords_2[0], coords_2[1], coords_2[3], coords_2[2]]
        
        
        camera_viewer = self.create_camera_viewplane(coords_2)
        
        camera_viewer.select_set(True)
        bpy.context.view_layer.objects.active = camera_viewer
                
        """ 
        TO MAKE MATERIAL SHADER FOR FOREST BASE
        """
        forest_base_colorramp_pos_0 = random.uniform(0.2,0.91) # has to be < pos1
        forest_base_colorramp_pos_1 = forest_base_colorramp_pos_0 + random.uniform(0.1,1-forest_base_colorramp_pos_0)

        forest_base_noise_scale = 7.0 # TO MAKE RANGES for this section
        forest_base_noise_detail = 4.0
        forest_base_noise_roughness = 1.0
        forest_base_noise_distortion = 0.0
        
        # (not recommended to vary much)
        forest_base_specular = 0.08
        col1  =self.colour_1
        col2 = self.colour_2
        forest_base_colorramp_col_0 = (col1[0],col1[1],col1[2],1.0) # dark green
        forest_base_colorramp_col_1 = (col2[0],col2[1],col2[2],1.0) # dark brown


        material_basic = bpy.data.materials.new(name="Basic")
        material_basic.use_nodes = True

        bpy.context.object.active_material = material_basic

        # Access default shader node
        principled_node = material_basic.node_tree.nodes.get("Principled BSDF")
        principled_node.inputs[0].default_value = (0,0,1,1)
        principled_node.inputs[7].default_value = forest_base_specular

        # Create colorramp node
        colorramp_node = material_basic.node_tree.nodes.new("ShaderNodeValToRGB")
        colorramp_node.location = (-250,0) # left of principledBSDF node

        # Create noise texture node
        noise_node = material_basic.node_tree.nodes.new("ShaderNodeTexNoise")
        noise_node.location = (-500, 0) # left of principledBSDF and ColorRamp nodes

        # shortcut to make links between nodes :D
        link = material_basic.node_tree.links.new

        # make links between nodes
        link(colorramp_node.outputs[0], principled_node.inputs[0])
        link(colorramp_node.outputs[0], principled_node.inputs[0])
        link(noise_node.outputs[1], colorramp_node.inputs[0])

        # Set color
        colorramp_node.color_ramp.elements[0].color = forest_base_colorramp_col_0 # dark green
        colorramp_node.color_ramp.elements[1].color = forest_base_colorramp_col_1 # dark brown

        # Set relative proportion of colors (amount)
        colorramp_node.color_ramp.elements[0].position = forest_base_colorramp_pos_0 # value approach pos of elem[1] for more green
        colorramp_node.color_ramp.elements[1].position = forest_base_colorramp_pos_1 # value approach pos of elem[0] for more brown

        # Set shape of color distribution 
        material_basic.node_tree.nodes["Noise Texture"].inputs[2].default_value = forest_base_noise_scale  # scale
        material_basic.node_tree.nodes["Noise Texture"].inputs[3].default_value = forest_base_noise_detail # detail
        material_basic.node_tree.nodes["Noise Texture"].inputs[4].default_value = forest_base_noise_roughness # roughness
        material_basic.node_tree.nodes["Noise Texture"].inputs[5].default_value = forest_base_noise_distortion # distortion

        material_basic.node_tree.nodes["Noise Texture"].noise_dimensions = '2D'
            
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        bpy.ops.object.particle_system_add()
        
        particle_count = self.particle_count
        particle_scale = self.particle_scale
 
        #ps_name = "ps1"
        bpy.data.particles[-1].type = "HAIR"
        bpy.data.particles[-1].use_advanced_hair = True
        # EMISSION
        bpy.data.particles[-1].count = particle_count # param
        camera_viewer.particle_systems[-1].seed = random.randint(0,10000)  # param(?) # seed to change random locations of particles
        
        bpy.data.particles[-1].use_scale_instance = True
        bpy.data.particles[-1].use_rotation_instance = True
#        bpy.data.particles[-1].use_global_instance = True
        bpy.data.particles[-1].use_global_instance=False
        
        #RENDER
        bpy.data.particles[-1].render_type = "COLLECTION"
        bpy.data.particles[-1].instance_collection = col
        bpy.data.particles[-1].use_collection_count = True
        
#                bpy.data.particles[-1].render_type = "OBJECT"
#                bpy.data.objects["Plane"].show_instancer_for_render = True # show emitter i.e. forest base plane
#                bpy.data.particles[-1].instance_object = obj #"tree1.001" #obj name will be the foilage object
        bpy.data.particles[-1].particle_size = particle_scale # param (0.1 to 0.5?)
#                bpy.data.particles[-1].size_random = 0.5 # param (0 to 0.5)
        # ROTATION
        bpy.data.particles[-1].use_rotations = True # param
        bpy.data.particles[-1].rotation_mode = "GLOB_Z"
        bpy.data.particles[-1].phase_factor_random = 2.0 # param (0 to 2.0)
        
    
        self.remove_camera_markers(torus_coll) # remove Torus corner markers
    
        # code to render image
        
        if self.render_image:
            
            # to create folder, named by current timestamp, to store labelsjson & rendered images
            current_datetime = datetime.datetime.utcnow()
            current_timetuple = current_datetime.utctimetuple()
            current_timestamp = str(calendar.timegm(current_timetuple))
            
            fp = bpy.data.scenes["Scene"].render.filepath
    #        path = fp + current_timestamp + "/" 
    #        imgs_folder_path = path + "data/"
            imgs_folder_path = fp + "render_images/"
            
    #        scene.render.filepath = imgs_folder_path + str(i+1) + ".jpg"
            scene.render.filepath = imgs_folder_path + current_timestamp+".jpg"
            filepath = scene.render.filepath
            # image files are saved for each frame specified
            bpy.ops.render.render(write_still=True) 
            
            # restore the filepath # NOT SURE IF NECESSARY
            bpy.data.scenes["Scene"].render.filepath = fp
        
        return {"FINISHED"}

classes = (
    generateScenePanel,
    
#    ADDONNAME_PT_TemplatePanel,
#    InitMyPropOperator,
    ADDONOPTIONS,
#    CustomPanel,
)


def register():
#    bpy.utils.register_module(__name__)
    
    from bpy.utils import register_class
    
    # not sure if the next lines are necessary...
    bpy.types.Scene.theChosenObject = bpy.props.StringProperty()
    bpy.types.Scene.env_coll = bpy.props.PointerProperty(type=bpy.types.Collection)
    
    for cls in classes:
        register_class(cls)
    # Register QueryProps
#    bpy.types.Scene.QueryProps = bpy.props.PointerProperty(type=QueryProps)
#    bpy.utils.register_class(CustomPanel)
#    bpy.types.Scene.CustomPanel = bpy.props.PointerProperty(type = Panel)
#    bpy.types.Scene.CustomPanel = bpy.props.PointerProperty(type=CustomPanel)    
    
 
#    del bpy.types.Scene.my_prop
    bpy.types.Scene.my_prop = bpy.props.StringProperty(default="default value")


def unregister():
#    bpy.utils.unregister_module(__name__)
       
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
#    for cls in classes:
#        unregister_class(cls)
    # $ delete QueryProps on unregister
    # del(bpy.types.Scene.QueryProps)
 
    # not sure if the next lines are necessary
    del bpy.types.Object.theChosenObject

#    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register() 