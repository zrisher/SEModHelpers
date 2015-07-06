import os
import os.path
import re
import shutil

special_chars = re.compile("[^a-zA-Z0-9_\-]")

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print ("creating directory path: " + dir_path)
        os.makedirs(dir_path)

def eraseDir(l_dir):
    if os.path.exists(l_dir):
      #print ("deleting: "+l_dir)
      shutil.rmtree(l_dir)

def copy_files_with_extension(source, destination, extension,
                              filename_prefix="", comp_dirs_to_remove=[]):
    """
    Copy all files with extension `extension` from `source` to `destination`.
    Optionally append `filename_prefix` to the name of the copies.
    """
    if not os.path.exists(source):
        return

    lowercase_extension = extension.lower()
    create_dir(destination)

    for filename in os.listdir(source):
        if filename.lower().endswith(lowercase_extension):
            source_file_path = os.path.join(source, filename)
            if os.path.isfile(source_file_path):
                dist_file_path = os.path.join(
                    destination, filename_prefix + filename
                )
                print("Copying file {0} => {1}".format(
                    source_file_path, dist_file_path
                ))
                shutil.copy(source_file_path, dist_file_path)


def deep_copy_files_with_extension(source, destination, extension,
                                   filename_prefix="", comp_dirs_to_remove=[],
                                   squash_dirs=False):
    """
    Copy all files with extension `extension` from every folder in `source` to
    a corresponding folder in `destination`.

    Optionally append `filename_prefix` to the name of the copies.

    Optionally discard folder structure in destination and instead prefix the
    file names with their folder names in "Path.To.File.Filename" format.

    The provided filename prefix is added before the directory prefix.
    """

    for relative_dir_path, dirs, files in os.walk(source):
        source_dir = os.path.join(source, relative_dir_path)

        current_file_prefix = filename_prefix
        if squash_dirs:
            destination_dir = destination
            current_file_prefix += re.sub(special_chars, '_', relative_dir_path)
        else:
            destination_dir = os.path.join(destination, relative_dir_path)

        print("copying files with ext '{0}' from {1} => {2}".format(
            extension, source_dir, destination_dir
        ))

        copy_files_with_extension(
            source_dir, destination_dir, extension, current_file_prefix,
            comp_dirs_to_remove
        )


def recursive_delete_if_empty(path):
    """
    Recursively delete empty directories; return True
    if everything was deleted.
    http://stackoverflow.com/questions/26774892/how-to-find-recursively-empty-directories-in-python
    """

    if not os.path.isdir(path):
        # If you also want to delete some files like desktop.ini, check
        # for that here, and return True if you delete them.
        return False

    # Note that the list comprehension here is necessary, a
    # generator expression would shortcut and we don't want that!
    if all([recursive_delete_if_empty(os.path.join(path, filename))
            for filename in os.listdir(path)]):
        # Either there was nothing here or it was all deleted
        os.rmdir(path)
        return True
    else:
        return False



"""
# copied from http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows/1214935#1214935
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

shutil.rmtree('Archive', ignore_errors=False, onerror=handleRemoveReadonly)
"""