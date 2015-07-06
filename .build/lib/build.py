# build.py
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


import datetime, errno, os, os.path, re, shutil, stat, subprocess, sys, time

from . import ops
from . import paths

cleanup_ignore_rgx = re.compile("^modinfo\.sbmi")


def clean_dist_dirs(dist_dirs):
    for dist_dir in dist_dirs:
        clean_dist_dir(dist_dir)


def clean_dist_dir(dist_dir):
    """
    Erase everything in the distribution dir besides modinfo.sbmi
    """
    print("cleaning dist dir " + dist_dir)
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            if not re.match(cleanup_ignore_rgx, file):
                full_path = os.path.join(root, file)
                print("removing file " + full_path)
                os.remove(full_path)

    ops.recursive_delete_if_empty(dist_dir)


def distribute(source_modules, dist_dirs, content_paths, extension,
               comp_vars_to_remove=[], squash_dirs=False):
    """
    Move files with extension `extension` from `content_paths` in `source_modules`
    to `dist_dir`
    """
    print("Distribute")

    for module_name, module_path in source_modules.items():
        print("Distribute '{0}' in {1}/{2} to {3}".format(
            extension, module_name, content_paths, dist_dirs))
        """
        for content_path in content_paths:
            module_content_path = os.path.join(module_path, *content_path)
            for dist_dir in dist_dirs:
                dist_content_path = os.path.join(dist_dir, *content_path)

                ops.deep_copy_files_with_extension(
                    module_content_path, dist_content_path, extension,
                    module_name + ".",
                    comp_vars_to_remove,
                    squash_dirs
                )
        """


def distribute_models(source_modules, dist_dirs):
	  """
    Move models from each module into the dist
    """


"""
    dist_cube_models_path = os.path.join(dist_dir, "Models", "Cube")

    model_dir_names = ["Model", "Models"]
		model_type_names = ["Cube"]
    cube_model_size_names = ["large", "small"]

    print("looking for model dirs to build from")
    for module_path in source_module_paths:
				for model_type_names
				module_cube_models_path = os.path.join(dist_dir, "Models")
        for model_dir_name in model_dir_names:
            for size_dir_name in size_dir_names:
                models_path = os.path.join(
                    module_path, model_dir_name, size_dir_name
                )
								ops.copy_files_with_extension(
										module_data_path, dist_data_path, ".mwm"
								)

    return mwm_processes


    destModel = endDir + r"\Models\Cubes"
    destModelDev = endDirDev + r"\Models\Cubes"


    # copy mwm files
    for module in modules[:]:
      # large models
      modelDir = source_dir + "\\" + module + "\\Model\\large"
      if os.path.exists(modelDir):
        copyWithExtension(modelDir, destModel + "\\large", ".mwm")
        copyWithExtension(modelDir, destModelDev + "\\large", ".mwm")
      # small models
      modelDir = source_dir + "\\" + module + "\\Model\\small"
      if os.path.exists(modelDir):
        copyWithExtension(modelDir, destModel + "\\small", ".mwm")
        copyWithExtension(modelDir, destModelDev + "\\small", ".mwm")
      # large models
      modelDir = source_dir + "\\" + module + "\\Models\\large"
      if os.path.exists(modelDir):
        copyWithExtension(modelDir, destModel + "\\large", ".mwm")
        copyWithExtension(modelDir, destModelDev + "\\large", ".mwm")
      # small models
      modelDir = source_dir + "\\" + module + "\\Models\\small"
      if os.path.exists(modelDir):
        copyWithExtension(modelDir, destModel + "\\small", ".mwm")
        copyWithExtension(modelDir, destModelDev + "\\small", ".mwm")

    print("\nfinished build\n")

"""


def distribute_scripts(source_modules, dist_dir):
    """
    Move all the scripts out of source_module_paths into dist_dir
    """
    dist_content_path = os.path.join(dist_dir, "Data", "Scripts")
    for module_name, module_path in source_modules.items():
        module_content_path = os.path.join(module_path, "Data")
        ops.copy_files_with_extension(
            module_content_path, dist_content_path, ".cs", module_name + "."
        )

    """
    createDir(distScript)
    createDir(distScriptDev)
    # copy scripts, data
    for module in modules[:]:
      copyFiles(module)


        # Move Scripts
    build.distribute_scripts(source_module_paths, dest_dir)
    build.distribute_scripts(source_module_paths, dest_dir_dev)


      # create Scripts
    createDir(destScript)
    createDir(destScriptDev)
    # copy scripts, data
    for module in modules[:]:

    # method that takes a module name and moves the files
    def copyFiles(l_source):
      print ("copying from "+l_source)
      l_sourceDir = startDir + "\\" + l_source + "\Scripts"
      l_dataDir = startDir + "\\" + l_source + "\Data"
      l_archiveDir = startDir + "\Archive\\" + l_source

      createDir(l_archiveDir)
      ignoreDirs = [ "bin", "obj", "Properties" ] # these are case-sensitive

      for path, dirs, files in os.walk(l_sourceDir):
        for ignore in ignoreDirs:
          if (ignore in dirs):
            dirs.remove(ignore)

        os.chdir(path)

        nsPath = path.replace(l_sourceDir,'')
        nsStr = nsPath.replace("\\","") + '.' if nsPath != '' else ''


        for file in files:
          if not file.lower().endswith(".cs"):
            continue

          #print ("file is "+file)
          lines = open(file, 'r').readlines()

          if (len(lines) == 0 or  "skip file on build" in lines[0]):
            #print ("skipping "+file)
            continue

          l_destFileName =  l_source + '.' + nsStr + file
          l_destFile = destScript + "\\" + l_destFileName
          l_destFileDev = destScriptDev + "\\" + l_destFileName

          # fake the pre-processor
          # remove symbols so scripts will compile
          # remove Conditional in Dev version
          # compiler will still remove Conditional statements in released version
          destFile = open(l_destFile, 'w')
          destFileDev = open(l_destFileDev, 'w')
          for line in lines:
            if (not line.lstrip().startswith("//")):
              if ("#define LOG_ENABLED" in line): # could not make startswith work
                destFile.write("// pre-processor symbol removed by build.py\n")
                destFileDev.write("// pre-processor symbol removed by build.py\n")
                continue
              if ("System.Diagnostics.Conditional" in line):
                destFile.write(line)
                destFileDev.write("// Conditional removed by build.py\n")
                continue
            destFile.write(line)
            destFileDev.write(line)


          # for archive, add date and time to file name
          d = datetime.datetime.fromtimestamp(os.path.getmtime(file))
          formated = str(d.year)+"-"+str(d.month).zfill(2)+"-"+str(d.day).zfill(2)+"_"+str(d.hour).zfill(2)+"-"+str(d.minute).zfill(2)+"_"+file
          archive = l_archiveDir +"\\"+formated
          try:
            os.chmod(archive, stat.S_IWRITE)
          except OSError:
            pass
          shutil.copyfile(file, archive)
          os.chmod(archive, stat.S_IREAD)

      if os.path.exists(l_dataDir):
        copyWithExtension(l_dataDir, destDataDev, ".sbc")
        copyWithExtension(l_dataDir, destData, ".sbc")
    """


def distribute_textures(source_module_paths, dist_dir):
    """
    Move all the textures out of source_module_paths into dist_dir
    """
    dist_script_path = os.path.join(dist_dir, "Data", "Scripts")
    """
        destTextureCube = endDir + r"\Textures\Models\Cubes"
    destTextureCubeDev = endDirDev + r"\Textures\Models\Cubes"

    destTexturePanel = endDir + r"\Textures\Models"
    destTexturePanelDev = endDirDev + r"\Textures\Models"

    destTextureIcon = endDir + r"\Textures\GUI\Icons\Cubes"
    destTextureIconDev = endDirDev + r"\Textures\GUI\Icons\Cubes"

    # copy textures
    for module_path in source_module_paths:
      textureDir = source_dir + "\\" + module + "\\Textures\\Cubes"
      if os.path.exists(textureDir):
        copyWithExtension(textureDir, destTextureCube, ".dds")
        copyWithExtension(textureDir, destTextureCubeDev, ".dds")
      textureDir = source_dir + "\\" + module + "\\Textures\\TextPanel"
      if os.path.exists(textureDir):
        copyWithExtension(textureDir, destTexturePanel, ".dds")
        copyWithExtension(textureDir, destTexturePanelDev, ".dds")
      textureDir = source_dir + "\\" + module + "\\Textures\\Icon"
      if os.path.exists(textureDir):
        copyWithExtension(textureDir, destTextureIcon, ".dds")
        copyWithExtension(textureDir, destTextureIconDev, ".dds")


    print("\nDistributing textures")

    model_dir_names = ["Model", "Models"]
    size_dir_names = ["large", "small"]

    for module_path in source_module_paths:
        for model_dir_name in model_dir_names:
            for size_dir_name in size_dir_names:
                models_path = os.path.join(
                    module_path, model_dir_name, size_dir_name
                )
                if os.path.exists(models_path):
                    mwm_processes.append(
                        subprocess.Popen(
                            ["python", mwm_builder_path],
                            cwd=models_path
                        )
                    )
    """


def process_models(source_modules, model_process_path, mwm_path):
    """
    start mwmBuilder processes in parallel
    """

    mwm_processes = []

    if not model_process_path:
        print("build-model.py path missing, skipping process_models")
        return mwm_processes
    elif not os.path.exists(model_process_path):
        paths.investigateBadPath("build-model.py", model_process_path)
        return mwm_processes

    if not mwm_path:
        print("mwm builder path missing, skipping process_models")
    elif not os.path.exists(mwm_path):
        paths.investigateBadPath("MwmBuilder", model_process_path)
        return mwm_processes

    model_dir_names = ["Model", "Models"]
    size_dir_names = ["large", "small"]

    print("looking for model dirs to build from")
    for module_name, module_path in source_modules.items():
        for model_dir_name in model_dir_names:
            for size_dir_name in size_dir_names:
                models_path = os.path.join(
                    module_path, model_dir_name, size_dir_name
                )
                if os.path.exists(models_path):
                    print("spawning process for " + models_path)
                    """
                    mwm_processes.append(
                        subprocess.Popen(
                            ["python", model_process_path],
                            cwd=models_path, mwm_path=mwm_path
                        )
                    )
                    """

    return mwm_processes


"""
def distribute_models_to_dirs(source_module_paths, dist_dirs):
    for dist_dir in dist_dirs:
        distribute_models(source_module_paths, dist_dir)

def clean_dist_dirs(dist_dirs):
  for dist_dir in dist_dirs:
      clean_dist_dir(dist_dir)

      def distribute_data(source_modules, dist_dir):
    \"""
    Move objects from the Data folder of each module into the dist
    \"""
    distribute(source_modules, dist_dir, [["Data"]], ".sbc")
    \"""
    dist_content_path = os.path.join(dist_dir, "Data")
    for module_name, module_path in source_modules.items():
        module_content_path = os.path.join(module_path, "Data")
        ops.copy_files_with_extension(
            module_content_path, dist_content_path, ".sbc", module_name + "."
        )
    \"""

"""