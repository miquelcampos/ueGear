import os

import unreal

from . import helpers

# Dictionary containing default FBX import options
DEFAULT_ASSETS_FBX_IMPORT_OPTIONS = {
	'import_materials': True,
	'import_textures': True,
	'import_as_skeletal': False
}

# Dictionary containing default FBX export options
DEFAULT_ASSETS_FBX_EXPORT_OPTIONS = {
	'ascii': False,
	'collision': False,
	'level_of_detail': False,
	'vertex_color': True
}


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


def get_export_path(asset_path):
	"""
	Returns path where asset was originally exported.

	:param str asset_path: path of the asset
	:return: export path.
	:rtype: str
	"""

	return get_asset_data(asset_path).get_asset().get_editor_property('asset_import_data').get_first_filename()


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

	created_folder = helpers.create_folder(root, name)

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


def selected_assets():
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


def generate_fbx_import_task(
		filename, destination_path, destination_name=None, replace_existing=True, automated=True, save=True,
		fbx_options=None):
	"""
	Creates and configures an Unreal AssetImportTask to import a FBX file.

	:param str filename: FBX file to import.
	:param str destination_path: Content Browser path where the asset will be placed.
	:param str or None destination_name: optional name of the imported asset. If not given, the name will be the
		filename without the extension.
	:param bool replace_existing: whether to replace existing assets.
	:param bool automated: unattended import.
	:param bool save: whether to save the file after importing it.
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
	fbx_options = fbx_options or DEFAULT_ASSETS_FBX_IMPORT_OPTIONS

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


def generate_asset_fbx_export_task(asset, filename, replace_identical=True, automated=True, fbx_options=None):
	"""
	Creates and configures an Unreal AssetExportTask to export a FBX file.

	:param str asset: asset we want to export with the task.
	:param str filename: FBX file to export.
	:param bool replace_identical: whether to replace identical files.
	:param bool automated: unattended export.
	:param fbx_options: dictionary containing all the FBX settings to use.
	:return: Unreal AssetExportTask that handles the export of the FBX file.
	:rtype: unreal.AssetExportTask
	"""

	task = unreal.AssetExportTask()
	task.filename = filename
	task.replace_identical = replace_identical
	task.automated = automated
	task.object = asset

	task.options = unreal.FbxExportOption()
	fbx_options = fbx_options or DEFAULT_ASSETS_FBX_EXPORT_OPTIONS
	for name, value in fbx_options.items():
		try:
			task.options.set_editor_property(name, value)
		except Exception:
			unreal.log_warning('Was not possible to set FBX Export property: {}: {}'.format(name, value))

	asset_class = asset.get_class()
	exporter = None
	if asset_class == unreal.StaticMesh.static_class():
		exporter = unreal.StaticMeshExporterFBX()
	elif asset_class == unreal.SkeletalMesh.static_class():
		exporter = unreal.SkeletalMeshExporterFBX()
	if not exporter:
		unreal.log_warning('Asset Type "{}" has not a compatible exporter!'.format(asset_class))
		return None
	task.exporter = exporter

	return task


def import_fbx_asset(filename, destination_path, destination_name=None, save=True, import_options=None):
	"""
	Imports a FBX into Unreal Content Browser.

	:param str filename: FBX file to import.
	:param str destination_path: Content Browser path where the asset will be placed.
	:param str or None destination_name: optional name of the imported asset. If not given, the name will be the
		filename without the extension.
	:param bool save: whether to save the file after importing it.
	:param dict import_options: dictionary containing all the FBX import settings to use.
	:return: path of the imported object.
	:rtype: str
	"""

	tasks = list()
	tasks.append(generate_fbx_import_task(
		filename, destination_path, destination_name=destination_name, fbx_options=import_options, save=save))

	return helpers.get_first_in_list(import_assets(tasks), default='')


def export_fbx_asset(asset, directory, fbx_filename='', export_options=None):
	"""
	Exports a FBX from Unreal Content Browser.

	:param unreal.Object asset: asset to export.
	:param str directory: directory where FBX asset will be exported.
	:param dict export_options: dictionary containing all the FBX export settings to use.
	:return: exported FBX file path.
	:rtype: str
	"""

	fbx_path = helpers.clean_path(os.path.join(directory, '{}.fbx'.format(fbx_filename or asset.get_name())))
	unreal.log('Exporting Asset "{}" in following path: "{}"'.format(asset, fbx_path))
	export_task = generate_asset_fbx_export_task(asset, fbx_path, fbx_options=export_options)
	if not export_task:
		unreal.log_warning('Was not possible to generate asset FBX export task')
		return None

	result = unreal.ExporterFBX.run_asset_export_task(export_task)

	return fbx_path if result else ''


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
