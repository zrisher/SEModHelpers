import os
import os.path
import re
import shutil
import fileinput

special_chars = re.compile("[^a-zA-Z0-9_\-]")
conditional_line = re.compile("\[System.Diagnostics.Conditional\(\"(.*?)\"\)\]")

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        print ("creating directory path: " + dir_path)
        os.makedirs(dir_path)

def eraseDir(l_dir):
    if os.path.exists(l_dir):
      #print ("deleting: "+l_dir)
      shutil.rmtree(l_dir)

def copy_files_with_extension(source, destination, extension,
                              filename_prefix="", comp_sym_to_remove=[]):
    """
    Copy all files with extension `extension` from `source` to `destination`.
    Optionally append `filename_prefix` to the name of the copies.
    """
    if not os.path.exists(source):
        return

    create_dir(destination)

    lowercase_extension = extension.lower()
    for filename in os.listdir(source):
        if filename.lower().endswith(lowercase_extension):
            source_file_path = os.path.join(source, filename)
            if os.path.isfile(source_file_path):
                dist_file_path = os.path.join(
                    destination, filename_prefix + filename
                )
                print("Copy from {0}\n       to {1}".format(
                    source_file_path, dist_file_path
                ))
                shutil.copy(source_file_path, dist_file_path)

                if lowercase_extension[-2:] == "cs":
                    preprocess_cs_file(dist_file_path, comp_sym_to_remove)


def deep_copy_files_with_extension(source, destination, extension,
                                   filename_prefix="",
                                   comp_sym_to_remove=[],
                                   squash_dirs=False):
    """
    Copy all files with extension `extension` from every folder in `source` to
    a corresponding folder in `destination`.

    Optionally append `filename_prefix` to the name of the copies.

    Optionally discard folder structure in destination and instead prefix the
    file names with their folder names in "Path.To.File.Filename" format.

    The provided filename prefix is added before the directory prefix.
    """
    #print("    deep_copy *.{0} from {1} => {2}".format(extension, source, destination))

    for dir_path, sub_dirs, files in os.walk(source):
        #source_path = os.path.join(source, dir_path)
        #print("!!{0} = os.path.join({1}, {2})".format(source_path, source, dir_path))
        #print("!!!Source {0}\n!!!Destin {1}".format(source_path, destination))


        rel_dir_path = os.path.relpath(dir_path, source)
        if squash_dirs:
            dist_path = destination
            squashed_dirs_file_prefix = re.sub(special_chars, '.', rel_dir_path)
            if squashed_dirs_file_prefix == ".":
                squashed_dirs_file_prefix = ''
            else:
                squashed_dirs_file_prefix += '.'

            current_file_prefix = filename_prefix + squashed_dirs_file_prefix
        else:
            dist_path = os.path.join(destination, rel_dir_path)
            current_file_prefix = filename_prefix
            #print("!!!{0} = os.path.join({1}, {2})".format(dist_path, destination, rel_dir_path))

        #print("!!!Source {0}\n!!!Destin {1}".format(dir_path, dist_path))

        #print("      deep dir {0}, file prefix '{1}'".format(
        #    dir_path, current_file_prefix
        #))

        copy_files_with_extension(
            dir_path, dist_path, extension, current_file_prefix,
            comp_sym_to_remove
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


def preprocess_cs_file(file_path, comp_sym_to_remove):
    """
    SE doesn't actually allow preprocessor symbol definitions in files,
    but it will remove conditional lines without defined symbols all the same

    we fake it by:
    parsing the symbol definitions, filtering for the valid ones for this distro
    removing all the symbol definition lines (so it will compile)
    removing the "System.Diagnostics.Conditional"s targeted at valid symbols
    """

    # find valid compilation symbols

    file = open(file_path, 'r')
    valid_syms = []

    for line in file:
        if not line.startswith('#'):
            break
        if line.startswith('#DEFINE'):
            comp_sym = line[7:].trim
            if not comp_sym in comp_sym_to_remove:
                valid_syms += comp_sym

    # remove conditional lines for valid symbols

    for line in fileinput.input(file_path, inplace=True):
        conditional_on = re.match(conditional_line, line).group(1)

        if conditional_on in valid_syms:
            continue
        else:
            print(line, end="")




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