import bpy
import math
import mathutils

# This script removes objects that have origins very close to eachother.
# It was mostly used to duplicate objects on an import
# It first finds the overlapping items, selects them, than removes them

seen = set()
uniq = []
for obj in bpy.data.objects:
    obj_pos = obj.location.copy()
    x = math.floor(obj_pos.x)
    y = math.floor(obj_pos.y)
    z = math.floor(obj_pos.z)
    floor_pos = mathutils.Vector((x,y,z)).freeze()
    if floor_pos not in seen:
        uniq.append(obj)
    seen.add(floor_pos)

print(len(uniq))

removable = set(bpy.data.objects).difference(set(uniq))


if bpy.context.object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')

for r_obj in removable:
    r_obj.select_set(True)

bpy.ops.object.delete()