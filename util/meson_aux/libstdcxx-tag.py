#!/usr/bin/env python3

# External command, intended to be called with custom_target() in meson.build

#                         argv[1]         argv[2]    argv[3]
# libstdcxx-tag.py <curl-or-wget-or-none> <srcdir> <output_path>

import os
import sys
import subprocess
import shutil

subcommand = sys.argv[1]
srcdir = sys.argv[2]
output_path = sys.argv[3]
output_dirname, output_filename = os.path.split(output_path)
if not output_dirname:
  output_dirname = '.'

# Remote location of the GNU libstdc++ Doxygen tag file.
libstdcxx_tag_url = 'http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/' + output_filename

def curl():
  options = [
    '--connect-timeout', '300',
    '--globoff',
    '--location',
    '--max-time', '300',
    '--remote-time',
    '--retry', '5',
  ]
  if os.path.isfile(output_path):
    # Don't download the tag file unless it's newer than the local file.
    options += ['--time-cond', output_path]

  options += [
    '--output', output_path,
    libstdcxx_tag_url,
  ]
  cmd = [
    subcommand,
    '--compressed',
  ] + options
  returncode = subprocess.run(cmd).returncode
  if returncode == 0:
    return returncode

  print('Trying curl without compression.', flush=True)
  cmd = [subcommand] + options
  return subprocess.run(cmd).returncode

def wget():
  cmd = [
    subcommand,
    '--timestamping',
    '--no-directories',
    '--timeout=300',
    '--tries=5',
    '--directory-prefix=' + output_dirname,
      libstdcxx_tag_url,
    ]
  return subprocess.run(cmd).returncode

def dont_download_tag_file():
  if os.path.isfile(output_path):
    print('Did not check status of', output_path, 'because network is disabled.')
  elif os.path.isfile(os.path.join(srcdir, output_filename)):
    print('Warning:', output_path, 'does not exist.')
    print('Copying from the source directory because network is disabled.')
    print('If you want an up-to-date copy, reconfigure with the -Duse-network=true option.')
    # shutil.copy2() copies timestamps and some other file metadata.
    shutil.copy2(os.path.join(srcdir, output_filename), output_path)
  else:
    print('Error:', output_path, 'does not exist.', file=sys.stderr)
    print('Downloading it is not possible because network is disabled.', file=sys.stderr)
    print('Please reconfigure with the -Duse-network=true option.', file=sys.stderr)
    return 1
  return 0

# ----- Main -----
subcommand_base = os.path.splitext(os.path.basename(os.path.normpath(subcommand)))[0]
if subcommand_base == 'curl':
  sys.exit(curl())
if subcommand_base == 'wget':
  sys.exit(wget())
sys.exit(dont_download_tag_file())
