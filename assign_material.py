"""Example script to automate Blender rendering for rectangular channel with ."""
import bpy
from math import radians
from mathutils import Matrix, Euler, Quaternion
import os

# Input parameters
t_0 = 0000
t_f = 0000
timestep = 2000

x3dpath = "../../examples/oneCellShear/tmp/x3d/"
renderpath = "../../examples/oneCellShear/tmp/renders/"
final_render_filename = "oneCellShear_render"
render_engine = "CYCLES"  # also try 'BLENDER_EEVEE'

def importx3d(filename, objectname):

    #import the x3d scene
    bpy.ops.import_scene.x3d(filepath=filename,
                             filter_glob="*.x3d;*.wrl",
                             axis_forward='Z',
                             axis_up='Y')
def scale_all(factor=0.5):
    for i in range(len(bpy.data.objects)):
        bpy.data.objects[i].scale[0] *= factor
        bpy.data.objects[i].scale[1] *= factor
        bpy.data.objects[i].scale[2] *= factor

def select_name( name = "", extend = True ):
    if extend == False:
        bpy.ops.object.select_all(action='DESELECT')
    ob = bpy.data.objects.get(name)
    ob.select = True
    bpy.context.scene.objects.active = ob

objectname1 = "platelet"
objectname2 = "BloodCell"


collection_names = ["platelets","rbcs"]

collections = [col for col in bpy.data.collections if col.name in collection_names]

# deselect all
for obj in bpy.data.objects:    
    obj.select_set(False)
    
    
# function to change name

def change_name (objectname):    
    for col in collections:
        #rename mesh and object
        for obj in col.all_objects:
            if "PLT" in obj.name:
                obj.name = objectname
                obj.data.name = objectname

# assign material
for col in collections:    
    print(col.name)
    #
    for obj in col.all_objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        if (col.name == "platelets") and (objectname1 in obj.name):                 
            platelet_material = bpy.data.materials.new( name = "PLT_mat")
            platelet_material.use_nodes = True            
            bpy.context.object.active_material = platelet_material
            nodes = platelet_material.node_tree.nodes
            # links        
            links = platelet_material.node_tree.links
                                
        if (col.name == "rbcs") and (objectname2 in obj.name):            
            rbc_material = bpy.data.materials.new( name = "RBC_mat")
            rbc_material.use_nodes = True            
            bpy.context.object.active_material = rbc_material
            nodes = rbc_material.node_tree.nodes
            # links        
            links = rbc_material.node_tree.links
# nodes used     
        principled_node = nodes.get("Principled BSDF")
        principled_node.location = (-35,500)
        material_output= nodes.get("Material Output")
        material_output.location = (660,360)
        emission_shader = nodes.new(type = 'ShaderNodeEmission')
        emission_shader.location = (240,320)
        mix_shader1 = nodes.new(type = 'ShaderNodeMixShader')
        mix_shader1.location = (500,480)
        mix_shader2 = nodes.new(type = 'ShaderNodeMixShader')
        mix_shader2.location = (240,480)
        fresnel_shader = nodes.new(type = 'ShaderNodeFresnel')
        fresnel_shader.location = (240,600)
        transparant_shader = nodes.new(type="ShaderNodeBsdfTransparent")
        transparant_shader.location = (-35,650)
        displacement_node = nodes.new (type="ShaderNodeDisplacement")
        displacement_node.location = (240,175)
        noise_texture_node = nodes.new(type="ShaderNodeTexNoise")
        noise_texture_node.location = (-215,460)
        bump_node = nodes.new(type="ShaderNodeBump")
        bump_node.location = (-215,210)
        rgb_node = nodes.new(type="ShaderNodeRGB")
        rgb_node.location = (-215,650)
        
        if (col.name == "platelets") and (objectname1 in obj.name):
            rgb_node.outputs[0].default_value = (0.9,0.8,0.2,1)    

        if (col.name == "rbcs") and (objectname2 in obj.name):
            rgb_node.outputs[0].default_value = (0.8,0.02,0.0,1)

        
        principled_node.inputs[1].default_value =0.0
        principled_node.inputs[3].default_value = (1.0,1.0,1.0,1.01)
        principled_node.inputs[4].default_value = 1.4
        transparant_shader.inputs[0].default_value = (1.0,0.5,0.2,1.0)
        
        noise_texture_node.inputs[1].default_value = (5.)
        noise_texture_node.inputs[2].default_value = (6.)
        noise_texture_node.inputs[3].default_value = (1.5)
        
        emission_shader.inputs[0].default_value = (1.0,1.0,1.0,1.0)
        emission_shader.inputs[1].default_value = 1.0
        fresnel_shader.inputs[0].default_value = 1.1
        
        bump_node.inputs[0].default_value =0.1
        bump_node.inputs[1].default_value =0.04
        
        displacement_node.inputs[1].default_value =1.0
        displacement_node.inputs[2].default_value =0.005


        
        
        links1 = links.new(mix_shader1.outputs[0],material_output.inputs[0])
        links2 = links.new(displacement_node.outputs[0],material_output.inputs[2])        
        links3 = links.new(fresnel_shader.outputs[0],mix_shader1.inputs[0])
        links4 = links.new(mix_shader2.outputs[0],mix_shader1.inputs[1])
        links5 = links.new(emission_shader.outputs[0],mix_shader1.inputs[2])        
        links6 = links.new(principled_node.outputs[0],mix_shader2.inputs[1])
        links7 = links.new(transparant_shader.outputs[0],mix_shader2.inputs[2])        
        links8 = links.new(noise_texture_node.outputs[0],displacement_node.inputs[0])
        links9 = links.new(noise_texture_node.outputs[0],bump_node.inputs[2])        
        links10 = links.new(bump_node.outputs[0],principled_node.inputs[22])        
        links11 = links.new(rgb_node.outputs[0],principled_node.inputs[0])
        links12 = links.new(rgb_node.outputs[0],transparant_shader.inputs[0])
        
        




        
        






        
            