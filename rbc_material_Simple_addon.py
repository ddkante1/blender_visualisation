import bpy


class ADDONNAME_PT_main_panel(bpy.types.Panel):
    
    """Creates a Panel in the Object properties window"""
    bl_label = "Add shader panel"
    bl_idname = "ADDONNAME_PT_main_panel"    
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "cell materials"

    def draw(self, context):
        layout = self.layout

        layout.operator("addonname.basic_operator")


class ADDONNAME_OT_add_basic(bpy.types.Operator):
    
    """Add basic Shader"""
    
    bl_label = "Add RBC Shader"
    bl_idname = "addonname.basic_operator"
    
    col = bpy.props.FloatVectorProperty(name = "Color",subtype='COLOR_GAMMA', size=4, default = (0.8,0.02,0.0,1.0))
    
    def execute (self,context):
    
        rbc_material = bpy.data.materials.new( name = "RBC")
        rbc_material.use_nodes = True
        
    
        bpy.context.object.active_material = rbc_material

    
        nodes = rbc_material.node_tree.nodes
        
        principled_node = nodes.get("Principled BSDF")
        material_output= nodes.get("Material Output")
        emission_shader = nodes.new(type = 'ShaderNodeEmission')
        mix_shader1 = nodes.new(type = 'ShaderNodeMixShader')
        mix_shader2 = nodes.new(type = 'ShaderNodeMixShader')
        fresnel_shader = nodes.new(type = 'ShaderNodeFresnel')
        transparant_shader = nodes.new(type="ShaderNodeBsdfTransparent")
        displacement_node = nodes.new (type="ShaderNodeDisplacement")
        noise_texture_node = nodes.new(type="ShaderNodeTexNoise")
        bump_node = nodes.new(type="ShaderNodeBump")
        rgb_node = nodes.new(type="ShaderNodeRGB")

        
        material_output.location = (660,360)
        mix_shader1.location = (500,480)
        mix_shader2.location = (240,480)
        displacement_node.location = (240,175)
        fresnel_shader.location = (240,600)
        emission_shader.location = (240,320)
        bump_node.location = (-215,210)
        noise_texture_node.location = (-215,460)
        principled_node.location = (-35,500)
        transparant_shader.location = (-35,650)
        rgb_node.location = (-215,650)
        
        rgb_node.outputs[0].default_value = (0.8,0.02,0.0,1)
        principled_node.inputs[1].default_value =0.0
        principled_node.inputs[3].default_value = (1.0,1.0,1.0,1.01)
        principled_node.inputs[4].default_value = 1.4
        transparant_shader.inputs[0].default_value = (1.0,0.5,0.2,1.0)
#        rgb_node.outputs[0].default_value = self.col
        
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
        
        links = rbc_material.node_tree.links

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
        
                
        return {'FINISHED'}
    
    ## create pop-up menu
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

classes = [ADDONNAME_PT_main_panel, ADDONNAME_OT_add_basic]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()                    

