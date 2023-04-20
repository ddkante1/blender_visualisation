import bpy
import math
import mathutils


def create_collection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)


def select_collection(name):
    target_collection = bpy.context.view_layer.layer_collection.children[name]
    bpy.context.view_layer.active_layer_collection = target_collection
    return target_collection.collection


def remove_lights_and_cameras(objects):
    for obj in objects:
        if obj.type == 'CAMERA' or obj.type == 'LIGHT':
            collection.objects.unlink(obj)
            bpy.data.objects.remove(obj)


def load_file(path):
    bpy.ops.import_scene.x3d(filepath=path)


def scale_objects(objects, factor):
    for obj in objects:
        obj.scale *= factor


def remove_duplicates(objects):
    seen = set()
    uniq = []
    for obj in objects:
        obj_pos = obj.location.copy()
        x = math.floor(obj_pos.x)
        y = math.floor(obj_pos.y)
        z = math.floor(obj_pos.z)
        floor_pos = mathutils.Vector((x, y, z)).freeze()
        if floor_pos not in seen:
            uniq.append(obj)
        seen.add(floor_pos)

    # Don't do this - just copy uniq to a new collection and remove existing collection, might be quicker
    removable = set(objects).difference(set(uniq))

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass

    bpy.ops.object.select_all(action='DESELECT')

    for r_obj in removable:
        r_obj.select_set(True)

    bpy.ops.object.delete()


def seperate_by_loose_parts(objects):
    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except:
        pass

    # Select every object
    for obj in objects:
        obj.select_set(True)

    # Separate by loose parts
    bpy.ops.mesh.separate(type='LOOSE')


def set_origin_to_center(objects):
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    # Select every object
    for obj in objects:
        obj.select_set(True)

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')


scale_factor = 1000000.0
collection_name = "PLT_Collection"
create_collection(collection_name)
collection = select_collection(collection_name)

print("Starting")

file_path = "D:/UserProjects/Joey/Rendering/BloodCells/Simulation_One/x3d/PLT.000002060000.x3d"
object = load_file(file_path)

print("Object Loaded")

scale_objects(collection.objects, scale_factor)

print("Scaled Data")

remove_lights_and_cameras(collection.objects)

print("Removing Lights")

seperate_by_loose_parts(collection.objects)

print("Seperated By Loose Parts")

set_origin_to_center(collection.objects)

print("Set Origin To Center")

remove_duplicates(collection.objects)

print("Remove Duplicates")