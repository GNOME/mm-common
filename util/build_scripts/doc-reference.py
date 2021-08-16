#!/usr/bin/env python3

# External command, intended to be called with run_command(), custom_target(),
# meson.add_install_script() or meson.add_dist_script() in meson.build.

#                     argv[1]      argv[2]     argv[3:]
# doc-reference.py <subcommand> <MMDOCTOOLDIR> <xxx>...

# <MMDOCTOOLDIR> is an absolute path in the source directory.

import os
import sys
import subprocess
import shutil

subcommand = sys.argv[1]
MMDOCTOOLDIR = sys.argv[2]

# Invoked from custom_target() in meson.build.
def doxygen():
  #    argv[3]         argv[4:]
  # <doxytagfile> <doc_input_files>...

  # <doxytagfile> is a relative or absolute path in the build directory.
  # <doc_input_files> are absolute paths in the source or build directory.
  doxytagfile = sys.argv[3]
  doc_outdir = os.path.dirname(doxytagfile)

  # Search for doc_postprocess.py first in MMDOCTOOLDIR.
  sys.path.insert(0, MMDOCTOOLDIR)
  from doc_postprocess import doc_postprocess

  # Export this variable for use in the Doxygen configuration file.
  child_env = os.environ.copy()
  child_env['MMDOCTOOLDIR'] = MMDOCTOOLDIR

  # Remove old files.
  if os.path.isfile(doxytagfile):
    os.remove(doxytagfile)
  shutil.rmtree(os.path.join(doc_outdir, 'html'), ignore_errors=True)

  # Relative paths in Doxyfile assume that Doxygen is run from the
  # build directory one level above Doxyfile.
  doxygen_cwd = os.path.join(doc_outdir, '..')

  DOXYGEN = child_env.get('DOXYGEN', None)
  if not DOXYGEN:
    DOXYGEN = 'doxygen'
  doxygen_input = '@INCLUDE = ' + os.path.join('reference', 'Doxyfile') + '\n' \
                + 'INPUT = "' + '" "'.join(sys.argv[4:]) + '"\n'
  # (Starting with Python 3.7 text=True is a more understandable equivalent to
  # universal_newlines=True. Let's use only features in Python 3.5.)
  result = subprocess.run([DOXYGEN, '-'], input=doxygen_input,
    universal_newlines=True, env=child_env, cwd=doxygen_cwd)
  if result.returncode:
    return result.returncode

  return doc_postprocess(os.path.join(doc_outdir, 'html', '*.html'))

# Invoked from custom_target() in meson.build.
def devhelp():
  #    argv[3]       argv[4]       argv[5]     argv[6]
  # <doxytagfile> <devhelpfile> <book_name> <book_title>

  # <doxytagfile> and <devhelpfile> are relative or absolute paths in the build directory.
  doxytagfile = sys.argv[3]
  devhelpfile = sys.argv[4]
  book_name = sys.argv[5]
  book_title = sys.argv[6]
  tagfile_to_devhelp = os.path.join(MMDOCTOOLDIR, 'tagfile-to-devhelp2.xsl')

  # The parameters to the Doxygen-to-Devhelp XSLT script.
  cmd = [
    'xsltproc',
    '--stringparam', 'book_title', book_title,
    '--stringparam', 'book_name', book_name,
    '--stringparam', 'book_base', 'html',
    '-o', devhelpfile,
    tagfile_to_devhelp,
    doxytagfile,
  ]
  return subprocess.run(cmd).returncode

# Invoked from meson.add_install_script().
def install_doc():
  #    argv[3]       argv[4]      argv[5]        argv[6:]
  # <devhelpfile> <devhelpdir> <htmlrefdir> <docinstall_flags>...

  # <devhelpfile> is a relative or absolute path in the build directory.
  # <htmlrefdir> and <devhelpdir> are installation directories, relative to {prefix}.
  devhelpfile = sys.argv[3]
  destdir_devhelpdir = os.path.join(os.getenv('MESON_INSTALL_DESTDIR_PREFIX'), sys.argv[4])
  destdir_htmlrefdir = os.path.join(os.getenv('MESON_INSTALL_DESTDIR_PREFIX'), sys.argv[5])
  prefix_htmlrefdir = os.path.join(os.getenv('MESON_INSTALL_PREFIX'), sys.argv[5])
  build_dir = os.path.dirname(devhelpfile)

  # Search for doc_install.py first in MMDOCTOOLDIR.
  sys.path.insert(0, MMDOCTOOLDIR)
  from doc_install import doc_install_cmdargs, doc_install_funcargs

  # Create the installation directories, if they do not exist.
  os.makedirs(destdir_htmlrefdir, exist_ok=True)
  os.makedirs(destdir_devhelpdir, exist_ok=True)

  verbose = []
  if not os.getenv('MESON_INSTALL_QUIET'):
    verbose = ['--verbose']

  # Install html files.
  cmdargs = [
    '--mode=0o644',
  ] + verbose + sys.argv[6:] + [
    '-t', destdir_htmlrefdir,
    '--glob',
    '--',
    os.path.join(build_dir, 'html', '*'),
  ]
  result1 = doc_install_cmdargs(cmdargs)

  # Install the Devhelp file.
  # rstrip('/') means remove trailing /, if any.
  result2 = doc_install_funcargs(
    sources=[devhelpfile],
    target=destdir_devhelpdir,
    target_is_dir=True,
    mode=0o644,
    verbose=bool(verbose),
    book_base=prefix_htmlrefdir.rstrip('/'),
  )

  return max(result1, result2)

# Invoked from meson.add_dist_script().
def dist_doc():
  #      argv[3]              argv[4]       argv[5]     argv[6]
  # <doctool_dist_dir> <doc_ref_build_dir> <tagfile> <devhelpfile>

  # <doctool_dist_dir> is a distribution directory, relative to MESON_PROJECT_DIST_ROOT.
  # <doc_ref_build_dir> is a relative or absolute path in the build directory.
  # <tagfile> and <devhelpfile> are relative or absolute paths in the build directory.

  # MESON_PROJECT_DIST_ROOT is set only if meson.version() >= 0.58.0.
  project_dist_root = os.getenv('MESON_PROJECT_DIST_ROOT', os.getenv('MESON_DIST_ROOT'))
  doctool_dist_dir = os.path.join(project_dist_root, sys.argv[3])
  doc_ref_build_dir = sys.argv[4]
  tagfile = sys.argv[5]
  devhelpfile = sys.argv[6]

  # Create the distribution directory, if it does not exist.
  os.makedirs(os.path.join(doctool_dist_dir, 'reference'), exist_ok=True)

  # Distribute files that mm-common-get has copied to MMDOCTOOLDIR.
  # shutil.copy() does not copy timestamps.
  for file in ['doc_install.py', 'doc_postprocess.py', 'doxygen-extra.css', 'tagfile-to-devhelp2.xsl']:
    shutil.copy(os.path.join(MMDOCTOOLDIR, file), doctool_dist_dir)

  # Distribute built files: tag file, devhelp file, html files.
  for file in [tagfile, devhelpfile]:
    shutil.copy(file, os.path.join(doctool_dist_dir, 'reference'))
  shutil.copytree(os.path.join(doc_ref_build_dir, 'html'),
                  os.path.join(doctool_dist_dir, 'reference', 'html'),
                  copy_function=shutil.copy)
  return 0

# Invoked from run_command() in meson.build.
def get_script_property():
  #  argv[3]
  # <property>
  # argv[2] (MMDOCTOOLDIR) is not used.
  prop = sys.argv[3]
  if prop == 'requires_perl':
    print('false', end='') # stdout can be read in the meson.build file.
    return 0
  print(sys.argv[0], ': unknown property,', prop)
  return 1

# ----- Main -----
if subcommand == 'doxygen':
  sys.exit(doxygen())
if subcommand == 'devhelp':
  sys.exit(devhelp())
if subcommand == 'install_doc':
  sys.exit(install_doc())
if subcommand == 'dist_doc':
  sys.exit(dist_doc())
if subcommand == 'get_script_property':
  sys.exit(get_script_property())
print(sys.argv[0], ': illegal subcommand,', subcommand)
sys.exit(1)
