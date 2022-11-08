#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains helper functions used by ueGear Unreal commands.
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import json
import tempfile
from collections import OrderedDict

import unreal

if sys.version_info[0] == 2:
	string_types = basestring,
	text_type = unicode
else:
	string_types = str,
	text_type = str

# Dictionary containing all the default material sample types
MATERIAL_SAMPLER_TYPES = {
	'Color': unreal.MaterialSamplerType.SAMPLERTYPE_COLOR,
	'Grayscale': unreal.MaterialSamplerType.SAMPLERTYPE_GRAYSCALE,
	'Alpha': unreal.MaterialSamplerType.SAMPLERTYPE_ALPHA,
	'Normal': unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,
	'Masks': unreal.MaterialSamplerType.SAMPLERTYPE_MASKS,
	'DistanceFieldFont': unreal.MaterialSamplerType.SAMPLERTYPE_DISTANCE_FIELD_FONT,
	'LinearColor': unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR
}

# Dictionary containing all the default Unreal Material properties
MATERIAL_PROPERTIES = {
	'BaseColor': unreal.MaterialProperty.MP_BASE_COLOR,
	'Metallic': unreal.MaterialProperty.MP_METALLIC,
	'Specular': unreal.MaterialProperty.MP_SPECULAR,
	'Roughness': unreal.MaterialProperty.MP_ROUGHNESS,
	'EmissiveColor': unreal.MaterialProperty.MP_EMISSIVE_COLOR,
	'Normal': unreal.MaterialProperty.MP_NORMAL
}

# Dictionary containing default FBX import options
DEFAULT_FBX_IMPORT_OPTIONS = {
	'import_materials': True,
	'import_textures': True,
	'import_as_skeletal': False
}


def is_string(s):
	"""
	Returns True if the given object has None type or False otherwise.

	:param s: object
	:return: bool
	"""

	return isinstance(s, string_types)


def force_list(var):
	"""
	Returns the given variable as list.

	:param object var: object we want to convert to list
	:return: object as list.
	:rtype: list(object)
	"""

	if var is None:
		return list()

	if type(var) is not list:
		if type(var) in [tuple]:
			var = list(var)
		else:
			var = [var]

	return var


def get_index_in_list(list_arg, index, default=None):
	"""
	Returns the item at given index. If item does not exist, returns default value.

	:param list(any) list_arg: list of objects to get from.
	:param int index: index to get object at.
	:param any default: any value to return as default.
	:return: any
	"""

	return list_arg[index] if list_arg and len(list_arg) > abs(index) else default


def get_first_in_list(list_arg, default=None):
	"""
	Returns the first element of the list. If list is empty, returns default value.

	:param list(any) list_arg: An empty or not empty list.
	:param any default: If list is empty, something to return.
	:return: Returns the first element of the list.  If list is empty, returns default value.
	:rtype: any
	"""

	return get_index_in_list(list_arg, 0, default=default)


def create_temporary_directory(prefix='ueGear'):
	"""
	Creates a temporary directory.

	:param str prefix: optional temporal directory prefix.
	:return: absolute file path to temporary directory.
	:rtype: str
	"""

	return tempfile.mkdtemp(prefix='{}}_tmp_'.format(prefix))


def read_json_file(filename, maintain_order=False):
	"""
	Returns data from JSON file.

	:param str filename: name of JSON file we want to read data from.
	:param bool maintain_order: whether to maintain the order of the returned dictionary or not.
	:return: data readed from JSON file as dictionary.
	:return: dict
	"""

	if os.stat(filename).st_size == 0:
		return None
	else:
		try:
			with open(filename, 'r') as json_file:
				if maintain_order:
					data = json.load(json_file, object_pairs_hook=OrderedDict)
				else:
					data = json.load(json_file)
		except Exception as err:
			unreal.log_warning('Could not read {0}'.format(filename))
			raise err

	return data


def write_to_json_file(data, filename, **kwargs):
	"""
	Writes data to JSON file.

	:param dict, data: data to store into JSON file.
	:param str filename: name of the JSON file we want to store data into.
	:param dict, kwargs:
	:return: file name of the stored file.
	:rtype: str
	"""

	indent = kwargs.pop('indent', 4)

	try:
		with open(filename, 'w') as json_file:
			json.dump(data, json_file, indent=indent, **kwargs)
	except IOError:
		unreal.log_error('Data not saved to file {}'.format(filename))
		return None

	unreal.log('File correctly saved to: {}'.format(filename))

	return filename


def get_unreal_version_name():
	"""
	Returns the version name of Unreal engine.

	:return: Unreal engine version name.
	:rtype: str
	"""

	return unreal.SystemLibrary.get_engine_version()


def get_unreal_version():
	"""
	Returns current version of Unreal engine.

	:return: Unreal engine version list.
	:rtype: list(int)
	"""

	version_name = get_unreal_version_name()
	version_split = version_name.split('+++')[0]
	versions = version_split.split('-')
	main_version = versions[0].split('.')
	extra_version = versions[-1]
	version_int = [int(version) for version in main_version]
	version_int.append(int(extra_version))

	return version_int


def get_current_unreal_project_path():
	"""
	Returns the current Unreal project absolute file path.

	:return: Absolute path to current .uproject file.
	:rtype: str
	"""

	return unreal.Paths.get_project_file_path()


def save_current_level():
	"""
	Saves current Unreal level.
	"""

	unreal.EditorLevelLibrary.save_current_level()


def get_editor_world():
	"""
	Returns the world in the editor world. It can then be used as WorldContext by other libraries like GameplayStatics.

	:return: world used by the editor world.
	:rtype: unreal.World
	"""

	return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def get_game_world():
	"""
	Returns the game world.

	:return: game world.
	:rtype: unreal.World
	"""

	return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()


def get_all_actors_in_current_level():
	"""
	Returns all current actors in the current opened level.

	:return: list of actors within level.
	:rtype: list(unreal.Actor)
	"""

	return unreal.EditorActorSubsystem().get_all_level_actors()


def get_selected_actors_in_current_level():
	"""
	Returns all current selected actors in the current opened level.

	:return: list of selected actors within level.
	:rtype: list(unreal.Actor)
	"""

	return unreal.EditorActorSubsystem().get_selected_level_actors()


def get_all_actors_and_labels_in_current_level():
	"""
	Returns a tuple with all current actors and their labels in the current opened level.

	:return: tuple with a list of actors and their labels within level.
	:rtype: tuple(list(unreal.Actor), list(str))
	"""

	actors = get_all_actors_in_current_level()
	actor_names = [actor.get_actor_label() for actor in actors]

	return actors, actor_names


def get_selected_actors_and_labels_in_current_level():
	"""
	Returns a tuple with all current selected actors and their labels in the current opened level.

	:return: tuple with a list of selected actors and their labels within level.
	:rtype: tuple(list(unreal.Actor), list(str))
	"""

	actors = get_selected_actors_in_current_level()
	actor_names = [actor.get_actor_label() for actor in actors]

	return actors, actor_names


def get_all_actors_and_names_in_current_level():
	"""
	Returns a tuple with all current actors and their names in the current opened level.

	:return: tuple with a list of actors and their names within level.
	:rtype: tuple(list(unreal.Actor), list(str))
	"""

	actors = get_all_actors_in_current_level()
	actor_names = [actor.get_name() for actor in actors]

	return actors, actor_names


def get_selected_actors_and_names_in_current_level():
	"""
	Returns a tuple with all current selected actors and their names in the current opened level.

	:return: tuple with a list of selected actors and their names within level.
	:rtype: tuple(list(unreal.Actor), list(str))
	"""

	actors = get_selected_actors_in_current_level()
	actor_names = [actor.get_name() for actor in actors]

	return actors, actor_names


def get_actor_by_label_in_current_level(actor_label):
	"""
	Return actor within current level with the given actor label.

	:param str actor_label: actor label.
	:return: found actor with given label in current level.
	:rtype: unreal.Actor or None

	..warning:: Actor labels within a level are not unique, so if multiple actors have the same label we may return
		the undesired one.
	"""

	found_actor = None
	all_actors = get_all_actors_in_current_level()
	for actor in all_actors:
		if actor.get_actor_label() == actor_label:
			found_actor = actor
			break

	return found_actor


def delete_actor(actor):
	"""
	Deletes given actor from current scene.

	:param unreal.Actor actor: actor instance to delete.
	"""

	unreal.EditorLevelLibrary.destroy_actor(actor)


def create_folder(root, name):
	"""
	Creates new folder.

	:param str root: root path.
	:param str name: folder name.
	:return: newly created folder.
	:rtype: str
	"""

	index = 1
	while True:
		if not unreal.EditorAssetLibrary.does_directory_exist('{}/{}'.format(root, name)):
			unreal.EditorAssetLibrary.make_directory('{}/{}'.format(root, name))
			break
		name = '{}{}'.format(name, index)
		index += 1

	return '{}/{}'.format(root, name)


def list_asset_paths(directory='/Game', recursive=True, include_folder=False):
	"""
	Returns a list of all asset paths within Content Browser.

	:param str directory: directory path of the asset we want the list from.
	:param bool recursive: whether will be recursive and will look in sub folders.
	:param bool include_folder: whether result will include folders name.
	:param list(str) or str or None extra_paths: asset path of the asset.
	:return: list of all asset paths found.
	:rtype: list(str)
	"""

	return unreal.EditorAssetLibrary.list_assets(directory, recursive=recursive, include_folder=include_folder)


def asset_exists(asset_path):
	"""
	Returns whether given asset path exists.

	:param str asset_path: asset path of the asset.
	:return: True if asset exist; False otherwise.
	:rtype: bool
	"""

	return unreal.EditorAssetLibrary.does_asset_exist(asset_path)


def get_asset_unique_name(asset_path, suffix=''):
	"""
	Returns a unique name for an asset in the given path.

	:param str asset_path: path of the asset
	:param str suffix: suffix to use to generate the unique asset name.
	:return: tuple containing asset path and name.
	:rtype: tuple(str, str)
	"""

	return unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(
		base_package_name=asset_path, suffix=suffix)


def rename_asset(asset_path, new_name):
	"""
	Renames asset with new given name.

	:param str asset_path: path of the asset to rename.
	:param str new_name: new asset name.
	:return: new asset name.
	:rtype: str
	"""

	dirname = os.path.dirname(asset_path)
	new_name = dirname + '/' + new_name
	unreal.EditorAssetLibrary.rename_asset(asset_path, new_name)
	return new_name


def move_assets_to_path(root, name, asset_paths):
	"""
	Moves/Rename the given list of assets to given destination directory.

	:param str root: root of the path (eg. '/Game')
	:param str name: name of the destination directory (eg. 'Target')
	:param list(str) asset_paths: list of asset paths.
	:return: new assets directory.
	:rtype: str
	"""

	created_folder = create_folder(root, name)

	for asset_path in asset_paths:
		loaded = unreal.EditorAssetLibrary.load_asset(asset_path)
		unreal.EditorAssetLibrary.rename_asset(asset_path, '{}/{}'.format(created_folder, loaded.get_name()))

	return created_folder


def get_assets(assets_path, recursive=False, only_on_disk=False):
	"""
	Returns all assets located in the given path.

	:param str assets_path: path to get assets from.
	:param bool recursive: whether to recursively find assets located in given path children folders.
	:param bool only_on_disk: whether memory-objects will be ignored. If True, this function will be faster.
	:return: assets data for all assets in the given path.
	:rtype: list(unreal.AssetData)
	"""

	asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

	return asset_registry.get_assets_by_path(
		assets_path, recursive=recursive, include_only_on_disk_assets=only_on_disk) or list()


def get_asset_data(asset_path, only_on_disk=False):
	"""
	Returns AssetData of the asset located in the given path.

	:param str asset_path: path of the asset we want to retrieve data of.
	:param bool only_on_disk: whether memory-objects will be ignored. If True, this function will be faster.
	:return: data of the asset located in the given path.
	:rtype: unreal.AssetData or None
	"""

	asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

	return asset_registry.get_asset_by_object_path(asset_path, include_only_on_disk_assets=only_on_disk)


def get_asset(asset_path, only_on_disk=False):
	"""
	Returns instance of an existent asset.

	:param str asset_path: path of the asset instance we want to get.
	:param bool only_on_disk: whether memory-objects will be ignored. If True, this function will be faster.
	:return: instance of the asset located in the given path.
	:rtype: object or None
	"""

	asset_data = get_asset_data(asset_path, only_on_disk=only_on_disk)
	if not asset_data:
		return None

	full_name = asset_data.get_full_name()
	path = full_name.split(' ')[-1]

	return unreal.load_asset(path)


def get_selected_asset_data():
	"""
	Returns current selected AssetData in Content Browser.

	:return: list of selected asset data in Content Browser.
	:rtype: list(AssetData)
	"""

	return unreal.EditorUtilityLibrary.get_selected_asset_data()


def get_selected_assets():
	"""
	Returns current selected asset instances in Content Browser.

	:return: list of selected asset instances in Content Browser.
	:rtype: list(object)
	"""

	return unreal.EditorUtilityLibrary.get_selected_assets()


def find_all_blueprints_data_assets_of_type(asset_type_name):
	"""
	Returns a list with all blueprint assets of the given type.

	:param str or type asset_type_name: blueprint asset type name.
	:return: list of blueprints assets with the given type.
	:rtype: list
	"""

	found_blueprint_data_assets = list()
	blueprints = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class('Blueprint', True)
	for blueprint in blueprints:
		blueprint_asset = blueprint.get_asset()
		bp = unreal.EditorAssetLibrary.load_blueprint_class(blueprint_asset.get_path_name())
		bp_type = unreal.get_type_from_class(bp)
		if bp_type == asset_type_name or bp_type.__name__ == asset_type_name:
			found_blueprint_data_assets.append(blueprint)

	return found_blueprint_data_assets


def create_asset(asset_path='', unique_name=True, asset_class=None, asset_factory=None, **kwargs):
	"""
	Creates a new Unreal asset.

	:param str asset_path: path where the asset will be created.
	:param bool unique_name: whether to automatically generate a unique name for the asset.
	:param class asset_class: class of the asset we want to create.
	:param class asset_factory: factory class to use for asset creation.
	:param dict kwargs: custom keyword arguments to use by the asset creation factory.
	:return: newly created asset instance.
	:rtype: object or None
	"""

	if unique_name:
		asset_path, asset_name = get_asset_unique_name(asset_path)
	if not asset_exists(asset_path):
		path = asset_path.rsplit('/', 1)[0]
		name = asset_path.rsplit('/', 1)[1]
		return unreal.AssetToolsHelpers.get_asset_tools().create_asset(
			asset_name=name, package_path=path, asset_class=asset_class, factory=asset_factory, **kwargs)

	return unreal.load_asset(asset_path)


def import_assets(asset_tasks):
	"""
	Imports assets from the given asset import tasks.

	:param list(unreal.AssetImportTask) asset_tasks: list of import tasks to run.
	:return: list of imported asset paths.
	:rtype: list(str)
	"""

	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(asset_tasks)

	imported_paths = list()
	for task in asset_tasks:
		unreal.log('Import Task for: {}'.format(task.filename))
		for object_path in task.imported_object_paths:
			unreal.log('Imported object: {}'.format(object_path))
			imported_paths.append(object_path)

	return imported_paths


def generate_fbx_import_task(
		filename, destination_path, destination_name=None, replace_existing=True, automated=True, save=True,
		fbx_options=None):
	"""
	Creates and configures an Unreal AssetImportTask to import a FBX file.

	:param str filename: FBX file to import.
	:param str destination_path: Content Browser path where the asset will be placed.
	:param str or None destination_name: optional name of the imported asset. If not given, the name will be the
		filename without the extension.
	:param bool replace_existing:
	:param bool automated:
	:param bool save:
	:param dict fbx_options: dictionary containing all the FBX settings to use.
	:return: Unreal AssetImportTask that handles the import of the FBX file.
	:rtype: unreal.AssetImportTask
	"""

	task = unreal.AssetImportTask()
	task.filename = filename
	task.destination_path = destination_path

	# By default, task.destination_name is the filename without the extension
	if destination_name:
		task.destination_name = destination_name

	task.replace_existing = replace_existing
	task.automated = automated
	task.save = save

	task.options = unreal.FbxImportUI()
	fbx_options = fbx_options or DEFAULT_FBX_IMPORT_OPTIONS

	# Skeletal Mesh related import options
	as_skeletal = fbx_options.pop('mesh_type_to_import', False)
	skeletal_mesh_import_data = fbx_options.pop('skeletal_mesh_import_data', dict())
	if skeletal_mesh_import_data:
		sk_import_data = unreal.FbxSkeletalMeshImportData()
		for name, value in skeletal_mesh_import_data.items():
			try:
				sk_import_data.set_editor_property(name, value)
			except Exception:
				unreal.log_warning('Was not possible to set Skeletal Mesh FBX Import property: {}: {}'.format(name, value))
		task.options.skeletal_mesh_import_data = sk_import_data

	# Base FBX import options
	for name, value in fbx_options.items():
		try:
			task.options.set_editor_property(name, value)
		except Exception:
			unreal.log_warning('Was not possible to set FBX Import property: {}: {}'.format(name, value))
	# task.options.static_mesh_import_data.combine_meshes = True

	task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
	if as_skeletal:
		task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH

	return task


def import_fbx_asset(filename, destination_path, destination_name=None, import_options=None):
	"""
	Imports a FBX into Unreal Content Browser.

	:param str filename: FBX file to import.
	:param str destination_path: Content Browser path where the asset will be placed.
	:param str or None destination_name: optional name of the imported asset. If not given, the name will be the
		filename without the extension.
	:param dict import_options: dictionary containing all the FBX import settings to use.
	:return: path of the imported object.
	:rtype: str
	"""

	tasks = list()
	tasks.append(generate_fbx_import_task(
		filename, destination_path, destination_name=destination_name, fbx_options=import_options))

	return get_first_in_list(import_assets(tasks), default='')


def generate_texture_import_task(
		filename, destination_path, destination_name=None, replace_existing=True, automated=True, save=True,
		import_options=None):
	"""
	Creates and configures an Unreal AssetImportTask to import a texture file.

	:param str filename: texture file to import.
	:param str destination_path: Content Browser path where the asset will be placed.
	:param str or None destination_name: optional name of the imported texture. If not given, the name will be the
		filenanme without the extension.
	:param bool replace_existing:
	:param bool automated:
	:param bool save:
	:param dict import_options: dictionary containing all the texture settings to use.
	:return: Unreal AssetImportTask that handles the import of the texture file.
	:rtype: unreal.AssetImportTask
	"""

	task = unreal.AssetImportTask()
	task.filename = filename
	task.destination_path = destination_path

	# By default, task.destination_name is the filename without the extension
	if destination_name:
		task.destination_name = destination_name

	task.replace_existing = replace_existing
	task.automated = automated
	task.save = save

	texture_factory = unreal.TextureFactory()
	task.factory = texture_factory
	import_options = import_options or dict()
	for name, value in import_options.items():
		try:
			task.factory.set_editor_property(name, value)
		except Exception:
			unreal.log_warning('Was not possible to set FBX Import property: {}: {}'.format(name, value))

	return task


def import_texture_asset(filename, destination_path, destination_name=None, import_options=None):
	"""
	Imports a texture asset into Unreal Content Browser.

	:param str filename: texture file to import.
	:param str destination_path: Content Browser path where the texture will be placed.
	:param str or None destination_name: optional name of the imported texutre. If not given, the name will be the
		filename without the extension.
	:param dict import_options: dictionary containing all the textutre import settings to use.
	:return: path to the imported texture asset.
	:rtype: str
	"""

	tasks = list()
	tasks.append(generate_texture_import_task(
		filename, destination_path, destination_name=destination_name, import_options=import_options))

	return get_first_in_list(import_assets(tasks), default='')


def create_material(material_name, material_path, diffuse_color=None, roughness=None, specular=None):
	"""
	Creates a new Unreal material with given name.

	:param str material_name: name of the material to create.
	:param str material_path: path where material will be created project.
	:param tuple(int, int) or None diffuse_color: default diffuse color for the material.
	:param float or None roughness: default roughness for the material.
	:param float or None specular: default specular for the material.
	:return: newly created material.
	:rtype: unreal.Material
	"""

	new_material = unreal.AssetToolsHelpers().get_asset_tools().create_asset(
		material_name, material_path, unreal.Material, unreal.MaterialFactoryNew())

	if diffuse_color is not None:
		ts_node_diffuse = unreal.MaterialEditingLibrary.create_material_expression(
			new_material, unreal.MaterialExpressionTextureSample, 0, 0)
		for color_value, color_channel in zip(diffuse_color, 'RGB'):
			ts_node_diffuse.set_editor_property(color_channel, color_value)
		unreal.MaterialEditingLibrary.connect_material_property(
			ts_node_diffuse, 'RGB', unreal.MaterialProperty.MP_BASE_COLOR)

	if roughness is not None:
		ts_node_roughness = unreal.MaterialEditingLibrary.create_material_expression(
			new_material, unreal.MaterialExpressionConstant, 0, 0)
		ts_node_roughness.set_editor_property('R', roughness)
		unreal.MaterialEditingLibrary.connect_material_property(
			ts_node_roughness, '', unreal.MaterialProperty.MP_ROUGHNESS)

	if specular is not None:
		ts_node_specular = unreal.MaterialEditingLibrary.create_material_expression(
			new_material, unreal.MaterialExpressionConstant, 0, 0)
		ts_node_specular.set_editor_property('R', roughness)
		unreal.MaterialEditingLibrary.connect_material_property(
			ts_node_specular, '', unreal.MaterialProperty.MP_SPECULAR)

	return new_material


def create_material_texture_sample(
		material, pos_x=0, pos_y=0, texture=None, sampler_type=None, connect=True, from_expression='RGB',
		property_to_connect=unreal.MaterialProperty.MP_BASE_COLOR):
	"""
	Creates a new material texture sample within the given material.

	:param unreal.Material material: material we want to create texture sample for.
	:param int pos_x:
	:param int  pos_y:
	:param texture:
	:param sampler_type:
	:param connect:
	:param from_expression:
	:param property_to_connect:
	:return:
	"""

	material_texture_sample = unreal.MaterialEditingLibrary.create_material_expression(
		material, unreal.MaterialExpressionTextureSample, pos_x, pos_y)
	if texture:
		material_texture_sample.set_editor_property('texture', texture)
		if sampler_type is not None and sampler_type != '':
			if is_string(sampler_type):
				sampler_type = MATERIAL_SAMPLER_TYPES.get(sampler_type, None)
			if sampler_type is not None:
				material_texture_sample.set_editor_property('sampler_type', sampler_type)
	if connect:
		if is_string(property_to_connect):
			property_to_connect = MATERIAL_PROPERTIES.get(property_to_connect, None)
		if property_to_connect is not None and property_to_connect != '':
			unreal.MaterialEditingLibrary.connect_material_property(
				material_texture_sample, from_expression, property_to_connect)

	return material_texture_sample


def convert_maya_transforms_into_unreal_transforms(translation, rotation, scale):
	"""
	Converts given Maya transforms into Unreal transforms.

	:param list(float, float, float) translation:
	:param list(float, float, float) rotation:
	:param list(float, float, float) scale:
	:return: Unreal transofrms.
	:rtype: tuple(unreal.Vector, unreal.Vector, unreal.Vector)
	"""

	maya_translation = translation or [0.0, 0.0, 0.0]
	maya_rotation = rotation or [0.0, 0.0, 0.0]
	maya_scale = scale or [1.0, 1.0, 1.0]

	unreal_translation = unreal.Vector(maya_translation[0], maya_translation[2], maya_translation[1])
	unreal_rotation = unreal.Rotator(maya_rotation[0], maya_rotation[2], maya_rotation[1] * -1)
	unreal_scale = unreal.Vector(maya_scale[0], maya_scale[2], maya_scale[1])

	return unreal_translation, unreal_rotation, unreal_scale


def remove_sequence_camera(level_sequence_name='', camera_name=''):
	"""
	Removes the camera from the given sequence with given name.

	:param str level_sequence_name: name of the sequence that contains the camera.
	:param str camera_name: name of the camera to remove.
	:return: True if the camera was removed successfully; False otherwise.
	:rtype: bool
	"""

	level_sequence_asset = unreal.load_asset(level_sequence_name)
	if not level_sequence_asset:
		return False

	sequence_bindings = level_sequence_asset.get_bindings()
	camera_bind = None
	for binding in sequence_bindings:
		if binding.get_name() or binding.get_display_name() == camera_name:
			camera_bind = binding
			break
	if not camera_bind:
		return False

	unreal.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
	children_component = camera_bind.get_child_possessables() or list()
	for child_component in children_component:
		child_component.remove()
	camera_tracks = camera_bind.get_tracks()
	for camera_track in camera_tracks:
		camera_bind.remove_track(camera_track)
	camera_bind.remove()

	unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
	unreal.EditorAssetLibrary.save_loaded_asset(level_sequence_asset)

	return True


def get_subsequences(level_sequence_name):
	"""
	Returns a list of sequences from the given sequence name.

	:param str level_sequence_name: name of the sequence whose subsequences we want to retrieve.
	:return: list of sequence subsequences.
	:rtype: list(unreal.LevelSequence)
	"""

	level_sequence_asset = unreal.load_asset(level_sequence_name)
	if not level_sequence_asset:
		return list()

	found_subscene_track = None
	tracks = level_sequence_asset.get_master_tracks()
	for track in tracks:
		if track.get_class() == unreal.MovieSceneSubTrack.static_class():
			found_subscene_track = track
			break

	return found_subscene_track.get_sections() if found_subscene_track else list()
