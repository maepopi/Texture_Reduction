
import bpy
import os
import math
import shutil
import glob
import sys
import argparse

#Passage en Cycles
bpy.context.scene.render.engine = 'CYCLES'

#J'importe depuis "femme"
rootfolder=os.path.join(sys.argv[5])

#Je veux exporter selon femme.obj
exportname=sys.argv[6]


obj_list=[]
obj_list.extend(glob.glob(os.path.join(rootfolder, '**', '*.gltf'), recursive=True))

for item_path in obj_list:
    candidate_object=item_path
    bpy.ops.import_scene.gltf(filepath=candidate_object)

ma_scene = bpy.context.scene
for un_objet in ma_scene.objects:
    if un_objet.type == 'MESH':
        bpy.context.scene.objects.active = un_objet

curr_object = bpy.context.active_object

export_folderpath = rootfolder
export_filepath=os.path.join(export_folderpath, exportname)

bpy.ops.export_scene.obj(filepath=export_filepath, use_selection=True)

# print("HEYYYYYYYYYYYYY")
#
# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
# print(sys.argv[4])
# print(sys.argv[5])
# print(sys.argv[6])
# print(sys.argv[7])


# shutil.rmtree(os.path.join(rootfolder,exportname,"*.gltf"))
# shutil.rmtree(os.path.join(rootfolder,exportname,"*.bin"))