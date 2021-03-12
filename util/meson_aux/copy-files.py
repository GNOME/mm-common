#!/usr/bin/env python3

# External command, intended to be called with run_command() in meson.build.

#                argv[1]    argv[2]    argv[3:]
# copy-files.py <from_dir> <to_dir> <file_names>...

import os
import sys
import shutil

# <from_dir> is an absolute or relative path of the directory to copy from.
# <to_dir> is an absolute or relative path of the directory to copy to.
from_dir_root = sys.argv[1]
to_dir_root = sys.argv[2]

# Copy some files if they exist in from_dir, but not in the destination
# directory, or if they are not up to date in the destination directory.
# (The term "source directory" is avoided here, because from_dir might not
# be what Meson calls a source directory as opposed to a build directory.)

for file in sys.argv[3:]:
  from_file = os.path.join(from_dir_root, file)
  to_file = os.path.join(to_dir_root, file)
  if os.path.isfile(from_file) and ((not os.path.isfile(to_file))
     or (os.stat(from_file).st_mtime > os.stat(to_file).st_mtime)):

    # Create the destination directory, if it does not exist.
    os.makedirs(os.path.dirname(to_file), exist_ok=True)

    # shutil.copy2() copies timestamps and some other file metadata.
    shutil.copy2(from_file, to_file)
sys.exit(0)
