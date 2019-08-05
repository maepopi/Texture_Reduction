import bpy
import os
import shutil
import sys

# PREMIERE CHOSE A FAIRE: LES NON GLTF EXPORTENT TOUJOURS LA MAUVAISE TEXTURE CAR IL FAUT LA SAUVEGARDER ET LA REPLUGGUER. PEUT ETRE REPENSER L+CETTE PARTIE TEXTURE
# DEUXIEME CHOSE A FAIRE : FAIRE UN SCRIPT A PART DE CONVERSION DEPUIS OBJ A GLB

def run():

	# print(sys.argv[0])
	# print( sys.argv[1] )
	# print( sys.argv[2] )
	# print( sys.argv[3] )
	# print( sys.argv[4] )
	# print( sys.argv[5] )
	# print( sys.argv[6] )
	# print( sys.argv[7] )
	# print( sys.argv[8] )
	# print( sys.argv[9] )
	# print( sys.argv[10] )
	# print( sys.argv[11] )


	bpy.context.scene.render.engine = "CYCLES"

	rootfolder = os.path.join( sys.argv[5] )
	obj_extension = os.path.join( sys.argv[6] )
	outputFolderPath = os.path.join( sys.argv[7] )
	gltf_output_path = os.path.join(sys.argv[13])
	diffuse_path = os.path.join( sys.argv[8] )
	obj_name = os.path.join( sys.argv[12] )


	if sys.argv[9] == "None":
		normal_path = "None"
		isNormal=False



	else:

		normal_path = os.path.join( sys.argv[9] )
		isNormal=True



	diffuse_resolution = sys.argv[10]
	normal_resolution = sys.argv[11]



	obj_list = []
	obj_list.append( rootfolder )


	####################### IMPORT ###################
	for item_path in obj_list:
		candidate_object=item_path


		if obj_extension=="obj":
			bpy.ops.import_scene.obj(filepath=candidate_object)

		elif obj_extension=="fbx":
			bpy.ops.import_scene.fbx( filepath=candidate_object)

		elif obj_extension == "gltf" or obj_extension == "glb":
			bpy.ops.import_scene.gltf(filepath=candidate_object)

		elif obj_extension == "stl":
			bpy.ops.import_scene.stl( filepath=candidate_object)

		elif obj_extension == "ply":
			bpy.ops.import_scene.ply( filepath=candidate_object)

		elif obj_extension == "3ds":
			bpy.ops.import_scene.autodesk_3ds( filepath=candidate_object)

		elif obj_extension == "dae":
			bpy.ops.wm.collada_import( filepath=candidate_object)

	ma_scene=bpy.context.scene

	for un_objet in ma_scene.objects:
		if un_objet.type=='MESH':
			bpy.context.scene.objects.active=un_objet


	curr_object=bpy.context.active_object



	############## TEXTURES ################

	reduced_normal_path = None
	reduced_diffuse_path = None

	#On commence par récupérer les textures de l'objet, ce qui va différer selon l'extension
	if obj_extension == "gltf" or obj_extension == "glb":

		material=curr_object.data.materials[0]

		material.use_nodes=True
		tree=material.node_tree
		nodes=tree.nodes
		links=tree.links

		shader_node=nodes.get("Principled BSDF")
		normal_socket_index = 17


		if shader_node is None:
			shader_node=nodes.get('Diffuse BSDF')
			normal_socket_index = 1

		diffuse_socket=shader_node.inputs[0]

		link=next(link for link in links if link.to_node == shader_node and link.to_socket==diffuse_socket)

		image_diffuse_node=link.from_node
		image_diffuse=None
		image_diffuse_name=None

		if image_diffuse_node.type=='TEX_IMAGE':
			image_diffuse=image_diffuse_node.image
			image_diffuse_name=image_diffuse.name

		image_diffuse.filepath_raw=os.path.join(gltf_output_path, obj_name + "_diffuse" + "_" + diffuse_resolution +  ".png")
		image_diffuse.file_format='PNG'
		bpy.data.images[image_diffuse_name].scale(int(diffuse_resolution), int(diffuse_resolution))

		image_diffuse.save()

		reduced_diffuse_path = os.path.join(gltf_output_path, obj_name + "_diffuse" + "_" + diffuse_resolution +  ".png")


		#### CHECK IF NORMAL #####
		normal_socket=shader_node.inputs[normal_socket_index]

		reduced_normal_path = None

		link=next(link for link in links if link.to_node==shader_node and link.to_socket==normal_socket)

		image_normal_node=link.from_node

		image_normal = None
		image_normal_name = None

		if image_normal_node.type is not None:

			if image_normal_node.type=='TEX_IMAGE':
				image_normal=image_normal_node.image
				image_normal_name=image_normal.name

			# On va etre obligé de revenir un cran en arrière car le image texture est lui meme pluggué à un autre node, et c'est cette connexion là qu'il faut tester
			elif image_normal_node.type=='NORMAL_MAP':
				normal_node=image_normal_node
				image_normal_node=None
				socket=normal_node.inputs[1]
				link=next(link for link in links if link.to_node==normal_node and link.to_socket==socket)
				image_normal_node=link.from_node

				image_normal=image_normal_node.image
				image_normal_name=image_normal.name


				image_normal.filepath_raw=os.path.join(gltf_output_path, obj_name + "_normal" + "_" + normal_resolution +  ".png")
				image_normal.file_format='PNG'
				bpy.data.images[image_normal_name].scale(int(normal_resolution), int(normal_resolution))

				image_normal.save()

				reduced_normal_path = os.path.join(gltf_output_path, obj_name + "_normal" + "_" + normal_resolution +  ".png")

			### CREATE MATERIAL ###
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

			curr_object.data.materials[0] = mat

			loaded_diffuse = bpy.data.images.load(reduced_diffuse_path)
			diff_texture_node = nodes.new('ShaderNodeTexImage')
			diff_texture_node.image=loaded_diffuse

			diffuse_fullname = loaded_diffuse.name
			diffuse_splitname = os.path.splitext( diffuse_fullname )
			loaded_diffuse.name = diffuse_splitname[0]

			link_diffuse = links.new( diff_texture_node.outputs[0], BSDF.inputs[0] )

			if reduced_normal_path is not None:
				loaded_normal = bpy.data.images.load(reduced_normal_path)
				norm_texture_node = nodes.new( "ShaderNodeTexImage" )
				norm_texture_node.image = loaded_normal
				norm_texture_node.color_space = 'NONE'

				normal_fullname = loaded_normal.name
				normal_splitname = os.path.splitext( normal_fullname )
				loaded_normal.name = normal_splitname[0]

				link_normal = links.new( norm_texture_node.outputs[0], BSDF.inputs[17])

	else:
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

		curr_object.data.materials[0] = mat

		loaded_diffuse = bpy.data.images.load( diffuse_path )
		diff_texture_node = nodes.new( 'ShaderNodeTexImage' )
		diff_texture_node.image = loaded_diffuse

		diffuse_fullname = loaded_diffuse.name
		diffuse_splitname = os.path.splitext( diffuse_fullname )
		loaded_diffuse.name = diffuse_splitname[0]

		link_diffuse = links.new( diff_texture_node.outputs[0], BSDF.inputs[0] )



		if reduced_normal_path is not None:
			loaded_normal = bpy.data.images.load( diffuse_path )
			norm_texture_node = nodes.new( "ShaderNodeTexImage" )
			norm_texture_node.image = loaded_normal
			norm_texture_node.color_space = 'NONE'

			normal_fullname = loaded_normal.name
			normal_splitname = os.path.splitext( normal_fullname )
			loaded_normal.name = normal_splitname[0]

			link_normal = links.new( norm_texture_node.outputs[0], BSDF.inputs[17] )










	############  EXPORT  ############
	export_filepath=os.path.join(outputFolderPath, obj_name + "_" + diffuse_resolution + "-" +  normal_resolution + ".glb" )
	bpy.ops.export_scene.gltf(filepath=export_filepath,export_format="GLB", export_selected=True)

	# bpy.ops.object.delete()






run()

		
			


		


