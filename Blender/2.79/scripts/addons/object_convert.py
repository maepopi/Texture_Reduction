import bpy
import os
import shutil
import sys

bpy.context.scene.render.engine = "CYCLES"

rootfolder = os.path.join(sys.argv[5])
obj_extension = os.path.join(sys.argv[6])
outputFolderPath = os.path.join(sys.argv[7])
gltf_output_path = os.path.join(sys.argv[13])
diffuse_path = os.path.join(sys.argv[8])
obj_name = os.path.join(sys.argv[12])

if sys.argv[9] == "None":
	normal_path = None
	isNormal=False
	normal_resolution=None

else:

	normal_path = os.path.join( sys.argv[9])
	isNormal=True
	normal_resolution = sys.argv[11]

diffuse_resolution = sys.argv[10]

obj_list = []
obj_list.append(rootfolder)

# TestArgs()


def TestArgs():
	print(sys.argv[0])
	print( sys.argv[1] )
	print( sys.argv[2] )
	print( sys.argv[3] )
	print( sys.argv[4] )
	print( sys.argv[5] )
	print( sys.argv[6] )
	print( sys.argv[7] )
	print( sys.argv[8] )
	print( sys.argv[9] )
	print( sys.argv[10] )
	print( sys.argv[11] )


def Import(obj_list, obj_extension):
	for item_path in obj_list:
		candidate_object = item_path

		if obj_extension == "obj":
			bpy.ops.import_scene.obj( filepath=candidate_object )

		elif obj_extension == "fbx":
			bpy.ops.import_scene.fbx( filepath=candidate_object )

		elif obj_extension == "gltf" or obj_extension == "glb":
			bpy.ops.import_scene.gltf( filepath=candidate_object )

		elif obj_extension == "stl":
			bpy.ops.import_scene.stl( filepath=candidate_object )

		elif obj_extension == "ply":
			bpy.ops.import_scene.ply( filepath=candidate_object )

		elif obj_extension == "3ds":
			bpy.ops.import_scene.autodesk_3ds( filepath=candidate_object )

		elif obj_extension == "dae":
			bpy.ops.wm.collada_import( filepath=candidate_object )

	ma_scene = bpy.context.scene

	for un_objet in ma_scene.objects:
		if un_objet.type == 'MESH':
			bpy.context.scene.objects.active = un_objet


	active_object = bpy.context.active_object

	active_object.name=obj_name

	curr_object=bpy.data.objects[obj_name]

	return curr_object



def CreateMaterial(diffuse_path, normal_path):

	reduced_normal_path = None
	reduced_diffuse_path = None

	mat = bpy.data.materials.new( "NewMat" )


	mat.use_nodes = True

	tree = mat.node_tree
	nodes = tree.nodes
	links = tree.links

	BSDF = nodes.new( "ShaderNodeBsdfPrincipled" )
	Output = nodes.get( "Material Output" )
	Diffuse = nodes.get( "Diffuse BSDF" )

	# Removing the default diffuse bsdf
	diffnodes = mat.node_tree.nodes
	node = nodes["Diffuse BSDF"]
	nodes.remove( node )

	links.new( BSDF.outputs[0], Output.inputs[0] )


	loaded_diffuse = bpy.data.images.load(diffuse_path)
	diff_texture_node = nodes.new('ShaderNodeTexImage')
	diff_texture_node.image=loaded_diffuse

	diffuse_fullname = loaded_diffuse.name
	diffuse_splitname = os.path.splitext( diffuse_fullname )
	loaded_diffuse.name = diffuse_splitname[0]

	link_diffuse = links.new(diff_texture_node.outputs[0], BSDF.inputs[0])

	if normal_path is not None:
		loaded_normal = bpy.data.images.load(normal_path)
		norm_texture_node = nodes.new( "ShaderNodeTexImage" )
		norm_texture_node.image = loaded_normal
		norm_texture_node.color_space = 'NONE'

		normal_fullname = loaded_normal.name
		normal_splitname = os.path.splitext( normal_fullname )
		loaded_normal.name = normal_splitname[0]

		link_normal = links.new( norm_texture_node.outputs[0], BSDF.inputs[17])

	return mat



def Export(outputFolderPath, obj_name, diffuse_resolution, normal_resolution):
	if normal_resolution is not None:
		export_filepath=os.path.join(outputFolderPath, obj_name + "_" + diffuse_resolution + "-" +  normal_resolution + ".glb" )

	else:
		export_filepath = os.path.join( outputFolderPath, obj_name + "_" + diffuse_resolution + "-" + ".glb" )
	bpy.ops.export_scene.gltf(filepath=export_filepath,export_format="GLB", export_selected=True)

	#bpy.ops.object.delete()

def Run():

	curr_object= Import(obj_list, obj_extension)

	print( "HEYYYYYYYYYYYYYY " + str(curr_object) )

	curr_object.data.materials[0]= CreateMaterial(diffuse_path,  normal_path)

	Export(outputFolderPath, obj_name, diffuse_resolution, normal_resolution)





Run()

		
			


		


