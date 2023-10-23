import bpy
import math
import mathutils
import os
import bmesh
from mathutils.kdtree import KDTree

def assign_material(material_name, collection):
    material = bpy.data.materials.get(material_name)

    for obj in collection.objects:
        # Check if the object can have materials
        if obj.type == 'MESH':
            # If object doesn't have any materials, add a slot
            if len(obj.data.materials) == 0:
                obj.data.materials.append(None)
            # Assign the material to the first slot
            obj.data.materials[0] = material


def remove_collection(collection_name):
    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    # Remove the collection if it exists
    if collection:
        # Unlink the collection from the scene
        for scene in bpy.context.blend_data.scenes:
            if collection.name in scene.collection.children:
                scene.collection.children.unlink(collection)
        # Remove the collection from the data-blocks
        bpy.data.collections.remove(collection)
        print(f"Collection '{collection_name}' removed.")
    else:
        print(f"Collection '{collection_name}' not found.")


def remove_active_collections():
    print("Removing Collections: ")
    remove_collection("RBC_Collection")
    remove_collection("PLT_Collection")
    remove_collection("PLT_PRE_Collection")
    remove_collection("RBC_PRE_Collection")


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

def remove_duplicates_kd_tree(objects):
    # Build a KDTree
    size = len(objects)
    kd = KDTree(size)

    for i, obj in enumerate(objects):
        kd.insert(obj.location, i)
    kd.balance()

    # Find close objects
    to_remove_pairs = set()
    for i, obj in enumerate(objects):
        # search for close objects, 1.1 ensures you get objects slightly further than just the exact point.
        for _, index, _ in kd.find_range(obj.location, 1.1):
            if i != index:  # Don't remove the object being checked
                # Create a tuple of the pair (i, index) such that the smaller index comes first
                pair = (i, index) if i < index else (index, i)
                to_remove_pairs.add(pair)

    # Convert pairs to the objects you want to remove (the ones with larger indices)
    to_remove = {objects[pair[1]] for pair in to_remove_pairs}

    print(f"KD Tree Removing {len(to_remove)} objects")

    # Select and remove
    bpy.ops.object.select_all(action='DESELECT')
    for obj in to_remove:
        obj.select_set(True)

    # Uncomment this line to actually delete the objects from the scene
    bpy.ops.object.delete()

    return {'FINISHED'}

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


remove_active_collections()

print("Start Full Import")

scale_factor = 1000000.0

directory_path = "/home/jkaaij/tmp_samepress_50um_Re075/x3d"
win_directory_path = "D:/UserProjects/Joey/CGI/BloodCells/PuncturedVesselAllTimesteps/tmp_samepress_50um_Re075/x3d"

curr_path = directory_path

files = os.listdir(curr_path)

material_tuples = [("RBC", "RBC_Mat"), ("RBC_PRE", "RBC_Mat"), ("PLT", "PLT_mat"), ("PLT_PRE", "PLT_mat")]

for file_name in files:

    file_path = os.path.join(curr_path, file_name)

    print(f"Importing {file_path}")

    prefix = file_name.split('.')

    print(f"Prefix: {prefix[0]}")

    collection_name = f"{prefix[0]}_Collection"

    create_collection(collection_name)

    collection = select_collection(collection_name)

    object = load_file(file_path)

    print("Object Loaded")

    scale_objects(collection.objects, scale_factor)

    print("Scaled Data")

    remove_lights_and_cameras(collection.objects)

    print("Removing Lights")

    seperate_by_loose_parts(collection.objects)

    print("Seperated By Loose Parts")

    set_origin_to_center(collection.objects)

    print("Done Setting Origin To Center")

    remove_duplicates_kd_tree(collection.objects)

    print("Removed Duplicates")

    # Find the tuple with the key
    found_mat_tuple = next((material_tuple for material_tuple in material_tuples if material_tuple[0] == prefix[0]), None)

    print(f"Assigning Material: {found_mat_tuple[1]} to collection {collection_name}")

    assign_material(found_mat_tuple[1], collection)

    print("Assigned Materials")

print("DONE!")

bpy.ops.wm.save_mainfile()
