#!/usr/bin/env python3

# External command, intended to be called with meson.add_dist_script() in meson.build

#                         sys.argv[1]      sys.argv[2]
# dist-build-scripts.py <root_src_dir> <relative_script_dir>

# <relative_script_dir> is the directory with the build scripts, relative to <root_source_dir>.

import os
import sys
import shutil

src_script_dir = os.path.join(sys.argv[1], sys.argv[2])
dist_script_dir = os.path.join(os.getenv('MESON_DIST_ROOT'), sys.argv[2])

# Create the distribution script directory, if it does not exist.
os.makedirs(dist_script_dir, exist_ok=True)

# Distribute files that mm-common-get has copied to src_script_dir.
files = [
  'check-dllexport-usage.py',
  'dist-build-scripts.py',
  'dist-changelog.py',
  'doc-reference.py',
  'generate-binding.py'
]
for file in files:
  shutil.copy(os.path.join(src_script_dir, file), dist_script_dir)

# Don't distribute .gitignore files.
for dirpath, dirnames, filenames in os.walk(os.getenv('MESON_DIST_ROOT')):
  if '.gitignore' in filenames:
    os.remove(os.path.join(dirpath, '.gitignore'))

# Remove an empty MESON_DIST_ROOT/build directory.
dist_build_dir = os.path.join(os.getenv('MESON_DIST_ROOT'), 'build')
if os.path.isdir(dist_build_dir):
  try:
    os.rmdir(dist_build_dir)
  except OSError:
    # Ignore the error, if not empty.
    pass
