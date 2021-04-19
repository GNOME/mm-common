#!/usr/bin/env python3

# External command, intended to be called with meson.add_install_script() in meson.build

#                           argv[1]
# extra-install-cmd.py <aclocal_macrodir>

import os
import sys
import subprocess

if not (os.getenv('DESTDIR') or os.getenv('MESON_INSTALL_QUIET')):
  # Inform the installer that M4 macro files installed in a directory
  # not known to aclocal will not be picked up automatically.
  # (Starting with Python 3.7 text=True is a more understandable equivalent to
  # universal_newlines=True. Let's use only features in Python 3.5.)
  try:
    result = subprocess.run(['aclocal', '--print-ac-dir'],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            universal_newlines=True)
    acdir = result.stdout
    aclocal_path = os.getenv('ACLOCAL_PATH')
    # acdir and aclocal_path can be sequences of os.pathsep-separated paths.
    # Merge them to one sequence with leading and trailing os.pathsep.
    # os.pathsep is ':' for Linux, ';' for Windows.
    acdirs = os.pathsep
    if aclocal_path:
      acdirs += aclocal_path + os.pathsep
    if acdir:
      acdirs += acdir.rstrip('\n') + os.pathsep

    if (os.pathsep + sys.argv[1] + os.pathsep) not in acdirs:
      # f'''.....''' would require Python 3.6. Avoid it.
      print('''\
                NOTE
                ----
(If you don't intend to use Autotools, you can ignore this note.)
The mm-common Autoconf macro files have been installed in a different
directory than the system aclocal directory. In order for the installed
macros to be found, it may be necessary to add the mm-common include
path to the ACLOCAL_PATH environment variable:
  ACLOCAL_PATH="$ACLOCAL_PATH:{}"
  export ACLOCAL_PATH'''.format(sys.argv[1])
      )
  except FileNotFoundError:
    # https://mail.gnome.org/archives/gtkmm-list/2021-April/msg00005.html
    # On Windows, subprocess.run() may fail to find aclocal even if
    # the calling meson.build file has found it. Ignore this case.
    pass
sys.exit(0)
