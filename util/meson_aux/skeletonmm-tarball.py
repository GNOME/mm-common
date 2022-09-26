#!/usr/bin/env python3

# External command, intended to be called with run_command() or custom_target()
# in meson.build

#                              argv[1]           argv[2]       argv[3:]
# skeletonmm-tarball.py <output_file_or_check> <source_dir> <input_files...>

import os
import sys
import shutil
import tarfile

if sys.argv[1] == 'check':
  # Called from run_command() during setup or configuration.
  # Check which archive format can be used.
  # In order from most wanted to least wanted: .tar.xz, .tar.gz, .tar
  available_archive_formats = []
  for af in shutil.get_archive_formats():
    # Keep the formats in a list, skip the descriptions.
    available_archive_formats += [af[0]]
  if 'xztar' in available_archive_formats:
    suffix = '.tar.xz'
  elif 'gztar' in available_archive_formats:
    suffix = '.tar.gz'
  else: # Uncompressed tar format is always available.
    suffix = '.tar'
  print(suffix, end='') # stdout can be read in the meson.build file.
  sys.exit(0)

# Create an archive.
output_file = sys.argv[1]
source_dir = sys.argv[2]

if output_file.endswith('.xz'):
  mode = 'w:xz'
elif output_file.endswith('.gz'):
  mode = 'w:gz'
else:
  mode = 'w'

def reset(tarinfo):
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = "root"
    return tarinfo


with tarfile.open(output_file, mode=mode) as tar_file:
  os.chdir(source_dir) # Input filenames are relative to source_dir.
  for file in sys.argv[3:]:
    tar_file.add(file, filter=reset)
# Errors raise exceptions. If an exception is raised, Meson+ninja will notice
# that the command failed, despite exit(0).
sys.exit(0)

# shutil.make_archive() might be an alternative, but it only archives
# whole directories. It's not useful, if you want to have full control
# of which files are archived.
