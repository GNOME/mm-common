#!/usr/bin/env python3

# External command, intended to be called with meson.add_dist_script() in meson.build

#                        argv[1]         argv[2]        argv[3:]
# extra-dist-cmd.py <root_source_dir> <root_build_dir> <no_dist>...

# <no_dist> Zero or more names (relative to MESON_PROJECT_DIST_ROOT)
#           of files and directories that shall not be distributed.

# Meson does not preserve timestamps on distributed files.
# But this script preserves the timestamps on libstdc++.tag.

import os
import sys
import subprocess
import shutil

root_source_dir = sys.argv[1]
root_build_dir = sys.argv[2]

# Make a ChangeLog file for distribution.
cmd = [
  'git',
  '--git-dir=' + os.path.join(root_source_dir, '.git'),
  '--work-tree=' + root_source_dir,
  'log',
  '--no-merges',
  '--date=short',
  '--max-count=200',
  '--pretty=tformat:%cd  %an  <%ae>%n%n  %s%n%w(0,0,2)%+b',
]
# MESON_PROJECT_DIST_ROOT is set only if meson.version() >= 0.58.0.
project_dist_root = os.getenv('MESON_PROJECT_DIST_ROOT', os.getenv('MESON_DIST_ROOT'))
logfilename = os.path.join(project_dist_root, 'ChangeLog')
with open(logfilename, mode='w', encoding='utf-8') as logfile:
  result = subprocess.run(cmd, stdout=logfile)
  if result.returncode:
    sys.exit(result.returncode)

# Distribute the libstdc++.tag file in addition to the files in the local git clone.
# shutil.copy2() copies timestamps and some other file metadata.
shutil.copy2(os.path.join(root_build_dir, 'libstdc++.tag'),
             os.path.join(project_dist_root, 'doctags'))

# Remove specified files and directories from the MESON_PROJECT_DIST_ROOT directory.
for rel_path in sys.argv[3:]:
  abs_path = os.path.join(project_dist_root, rel_path)
  if os.path.isfile(abs_path):
    os.remove(abs_path)
  elif os.path.isdir(abs_path):
    shutil.rmtree(abs_path, ignore_errors=True)
  else:
    # Ignore non-existent files and directories.
    print('--- Info:', abs_path, 'not found, not removed.')
