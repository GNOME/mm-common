#!/usr/bin/env python3

# External command, intended to be called with meson.add_dist_script() in meson.build

#                        argv[1]          argv[2]
# extra-dist-cmd.py <root_source_dir> <root_build_dir>

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
logfile = open(os.path.join(os.getenv('MESON_DIST_ROOT'), 'ChangeLog'), mode='w')
result = subprocess.run(cmd, stdout=logfile)
logfile.close()

# Distribute the libstdc++.tag file in addition to the files in the local git clone.
# shutil.copy2() copies timestamps and some other file metadata.
shutil.copy2(os.path.join(root_build_dir, 'libstdc++.tag'),
             os.path.join(os.getenv('MESON_DIST_ROOT'), 'doctags'))

sys.exit(result.returncode)
