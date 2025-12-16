#!/usr/bin/env python3

# External command, intended to be called with custom_target() in meson.build

#                       argv[1]             argv[2]          argv[3]    argv[4]
# libstdcxx-tag.py <use_network_opt> <curl-or-wget-or-none> <srcdir> <output_path>

import os
import sys
import subprocess
import shutil

use_network_opt = sys.argv[1]
subcommand = sys.argv[2]
srcdir = sys.argv[3]
output_path = sys.argv[4]
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

def download_if_possible():
  # use_network_opt == 'true' or 'if-no-local-tag-file'
  subcommand_base = os.path.splitext(os.path.basename(os.path.normpath(subcommand)))[0]
  if subcommand_base == 'curl':
    return curl()
  if subcommand_base == 'wget':
    return wget()

  if not os.path.isfile(output_path):
    print('Error:', output_path, 'does not exist.', file=sys.stderr)
    print('Downloading it is not possible because no download command exists.',
          file=sys.stderr)
  else:
    print('Error: Downloading', output_path,
          'is not possible because no download command exists.', file=sys.stderr)
  print('Please install "curl" or "wget".', file=sys.stderr)
  return 1

def copy_or_download():
  # use_network_opt == 'false' or 'if-no-local-tag-file'
  if os.path.isfile(output_path):
    print('Did not check status of', output_path, 'because network is disabled.')
  elif os.path.isfile(os.path.join(srcdir, output_filename)):
    print('Warning:', output_path, 'does not exist in the build directory.')
    print('Copying from the source directory.')
    print('If you want an up-to-date copy, reconfigure with the -Duse-network=true option.')
    # shutil.copy2() copies timestamps and some other file metadata.
    shutil.copy2(os.path.join(srcdir, output_filename), output_path)
  elif use_network_opt == 'if-no-local-tag-file':
    return download_if_possible()
  else: # use_network_opt == 'false'
    print('Error:', output_path, 'does not exist.', file=sys.stderr)
    print('Downloading it is not possible because network is disabled.', file=sys.stderr)
    print('Please reconfigure with the -Duse-network=true or',
          '-Duse-network=if-no-local-tag-file option.', file=sys.stderr)
    return 1
  return 0

# ----- Main -----
if use_network_opt == 'true':
  sys.exit(download_if_possible())
sys.exit(copy_or_download())
