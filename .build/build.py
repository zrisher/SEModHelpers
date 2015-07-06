# run.py
#
# This script combines the individual module folders into a single structure
# for Space Engineers to load (and a bunch of other useful deploy tasks)
#
# We expect SEModHelpers to live one level below the top-level source folder
#
# It will create two mods,
#   "%AppData%\SpaceEngineers\Mods\ModName" and
#   "%AppData%\SpaceEngineers\Mods\ModName Dev".
#
# The Dev version has logging enabled

import os
import os.path
import sys

from enum import Enum
import yaml

import lib

class Animals(Enum):
    ant = 1
    bee = 2
    cat = 3
    dog = 4


def build_distro():
    print("\n\n------- SEModHelpers Python Build Script  -------\n")

    # === Get Build Script paths

    build_script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print("Running from " + build_script_dir)
    build_model_path = os.path.join(build_script_dir, 'build_model.py')

    build_config_path = lib.paths.find_file_up(
        "build_config.yml", build_script_dir, 4
    )
    if build_config_path:
        print("Config file found at " + build_config_path)
    else:
        print("build_config.yml is missing. Aborting script.")
        return

    # === Load config

    config = yaml.load(open(build_config_path, 'r'))


    # source
    source_dir = config.get('source_dir')
    source_dir = source_dir if source_dir else os.path.dirname(build_config_path)

    mod_name = config.get('mod_name')
    mod_name = mod_name if mod_name else os.path.basename(source_dir)

    has_modules = not not config.get('has_modules')
    if has_modules:
        source_modules = lib.paths.modules(source_dir)
    else:
        source_modules = {}
        source_modules[mod_name] = source_dir

    # destination
    se_mods_dir = config.get('se_mods_dir')
    if not se_mods_dir:
        appData = os.getenv('APPDATA')
        se_mods_dir = os.path.join(appData, "SpaceEngineers", "Mods")

    dist_path = os.path.join(se_mods_dir, mod_name)

    if build_dev_version:



    build_dev_version = not not config.get('build_dev_version')
    dist_dirs = {}
    dist_dirs[mod_name] = os.path.join(se_mods_dir, mod_name)
    if build_dev_version:
        dist_dirs[mod_name] = os.path.join(se_mods_dir, mod_name + " Dev")




    dev_comp_vars = config.get('dev_compilation_variables')
    if not dev_comp_vars:
        dev_comp_vars = []

    # tools
    mwm_builder_path = "{0}".format(config.get('mwm_builder_path'))

    print("\n----- Config -----\n")
    print("Mod Name: " + mod_name)
    print("Source directory: " + source_dir)
    #print("Multiple Source Modules: {0}".format(has_modules))
    #print("")
    print("Source Modules: ")
    for module_name, module_path in source_modules.items():
        print(" - " + module_name + ": " + module_path)
    print("")
    print("SE Mods Directory: " + se_mods_dir)
    print("Distribute Mods to: ")
    print(" - " + dist_path)
    print("Build the Dev version? {0}".format(build_dev_version))
    if build_dev_version:
        print("Mod Dev Dist Dir " + dist_path_dev)
    print("Compilation variables to remove from .cs files: {0}".format(dev_comp_vars))
    print("")
    print("MWM Builder Path: " + mwm_builder_path)
    print("")

    # === Run Build
    print("----- Running Build ----- \n")


    # Start MWM Builder, which runs in parallel
    print("--- Starting MWM Model Builder Threads --- ")
    mwm_processes = lib.build.process_models(
        source_modules, build_model_path, mwm_builder_path
    )
    mwm_processes_count = mwm_processes.__len__()
    if mwm_processes_count > 0:
        print("Running {0} mwm_processes.".format(mwm_processes.__len__()))
    else:
        print("no mwm_processes running")
    print("")

    if build_dev_version:
        dist_paths = [dist_path, dist_path_dev]
    else:
        dist_paths = [dist_path]

    # Clean Destinations
    print("--- Cleaning Dist Dirs ---")
    lib.build.clean_dist_dirs(dist_paths)
    print("")

    # Copy Data
    print("--- Copying Data ---")
    lib.build.distribute(source_modules, dist_paths, [["Data"]], ".sbc")
    print("")

    """
    # Copy Scripts
    print("--- Copying Scripts ---")
    lib.build.distribute(source_modules, dist_paths,
                         [["Scripts"],["Data", "Scripts"]],
                         ".cs", remove_comp_vars=True
    )
    print("")


    # Copy Textures
    print(" --- Copying Textures --- ")
    lib.build.distribute_textures_to_dirs(source_module_paths, [dist_path, dist_path_dev])
    print("\n")

    # Copy Models once they're built
    if mwm_processes_count > 0:
        print("waiting for our mwm processes to finish")
        for mwm_process in mwm_processes:
            mwm_process.wait()

    print(" --- Distributing Models --- ")
    lib.build.distribute_models(source_module_paths, [dist_path, dist_path_dev])
    print("\n")
    """

    print("------- SEModHelpers Python Build Complete  ------- \n")


if __name__ == '__main__':
    build_distro()