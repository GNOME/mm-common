#!/usr/bin/env python3

# External command, intended to be called with meson.add_dist_script() in meson.build

#                       argv[1]
# dist-changelog.py <root_source_dir>

import os
import sys
import subprocess

# Make a ChangeLog file for distribution.
cmd = [
  'git',
  '--git-dir=' + os.path.join(sys.argv[1], '.git'),
  '--work-tree=' + sys.argv[1],
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
  sys.exit(subprocess.run(cmd, stdout=logfile).returncode)
