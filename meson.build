# This file is part of mm-common.

project('mm-common',
  version: '1.0.4',
  license: 'GPLv2+',
  meson_version: '>= 0.55.0', # required for meson.add_dist_script(python3, ...)
                              # and meson.add_install_script(python3, ...)
)

python3 = import('python').find_installation()
python_version = python3.language_version()
python_version_req = '>= 3.5'
if not python_version.version_compare(python_version_req)
  error('Requires Python @0@, found @1@.'.format(python_version_req, python_version))
endif

# Use these instead of meson.source_root() and meson.build_root().
# source_root() and build_root() are not useful, if this is a subproject.
project_source_root = meson.current_source_dir()
project_build_root = meson.current_build_dir()

script_dir = project_source_root / 'util' / 'meson_aux'

# Install directories are relative to {prefix}.
install_prefix = get_option('prefix')
install_bindir = get_option('bindir')

install_datadir = get_option('datadir')
install_aclocal_macrodir = install_datadir / 'aclocal'
install_pkgconfigdir = install_datadir / 'pkgconfig'
install_docdir = install_datadir / 'doc' / meson.project_name()

install_pkgdatadir = install_datadir / meson.project_name()
install_build_supportdir = install_pkgdatadir / 'build'
install_doctooldir = install_pkgdatadir / 'doctool'
install_doctagsdir = install_pkgdatadir / 'doctags'

install_mandir = get_option('mandir')
install_man1dir = install_mandir / 'man1'

# Configuration data for built files:
#   doctags/mm-common-libstdc++.pc.in -> mm-common-libstdc++.pc
#   doctags/mm-common-libstdc++-uninstalled.pc.in -> mm-common-libstdc++-uninstalled.pc
#   macros/mm-common.m4.in -> mm-common.m4
#   util/mm-common-get.1.in -> mm-common-get.1
#   util/mm-common-get.in -> mm-common-get
#   util/mm-common-prepare.1.in -> mm-common-prepare.1
#   util/mm-common-prepare.in -> mm-common-prepare
#   util/mm-common-util.pc.in -> mm-common-util.pc
#   util/mm-common-util-uninstalled.pc.in -> mm-common-util-uninstalled.pc
conf_data = configuration_data()
conf_data.set('prefix', install_prefix)
conf_data.set('datarootdir', '${prefix}' / install_datadir)
conf_data.set('datadir', '${datarootdir}')
conf_data.set('docdir', install_prefix / install_docdir)
conf_data.set('PACKAGE_NAME', meson.project_name())
conf_data.set('PACKAGE_TARNAME', meson.project_name())
conf_data.set('PACKAGE_VERSION', meson.project_version())
conf_data.set('PACKAGE_STRING', meson.project_name() + ' ' + meson.project_version())

# These are installed so that mm-common-prepare can copy them
# into projects at autogen.sh time.
autotools_build_support_basefiles = [
  'compile-binding.am',
  'dist-changelog.am',
  'doc-reference.am',
  'generate-binding.am',
]
build_support_files = []
foreach file : autotools_build_support_basefiles
  build_support_files += 'am_include' / file
endforeach

# These are installed so that mm-common-get can copy them
# into projects at Meson setup or configure time.
meson_build_support_basefiles = [
  'check-dllexport-usage.py',
  'dist-build-scripts.py',
  'dist-changelog.py',
  'doc-reference.py',
  'generate-binding.py',
]
foreach file : meson_build_support_basefiles
  build_support_files += 'util' / 'build_scripts' / file
endforeach
install_data(build_support_files, install_dir: install_build_supportdir)

# These are installed so that aclocal can copy them into aclocal.m4
# at autogen.sh time.
aclocal_macro_basefiles = [
  'mm-ax_cxx_compile_stdcxx.m4',
  'mm-ax_cxx_compile_stdcxx_11.m4',
  'mm-dietlib.m4',
  'mm-doc.m4',
  'mm-module.m4',
  'mm-pkg.m4',
  'mm-warnings.m4',
]
aclocal_macro_files = []
foreach file : aclocal_macro_basefiles
  aclocal_macro_files += 'macros' / file
endforeach
install_data(aclocal_macro_files, install_dir: install_aclocal_macrodir)

conf_data2 = configuration_data()
conf_data2.merge_from(conf_data)
conf_data2.set('configure_input', 'mm-common.m4.  Generated from macros/mm-common.m4.in')
configure_file(
  input: 'macros' / 'mm-common.m4.in',
  output: '@BASENAME@',
  configuration: conf_data2,
  install_dir: install_aclocal_macrodir
)

if find_program('aclocal', required: false).found()
  meson.add_install_script(
    python3, script_dir / 'extra-install-cmd.py',
    install_prefix / install_aclocal_macrodir
  )
endif

# These are installed so that mm-common-prepare can copy them into projects
# at autogen.sh time, if a directory path is given to MM_CONFIG_DOCTOOL_DIR(),
# or they can be found via pkg-config --variable=doctooldir mm-common-util.
# They are also installed so that mm-common-get can copy them
# into projects at Meson setup or configure time.
doctool_basefiles = [
  'doc-install.pl',
  'doc_install.py',
  'doc-postprocess.pl',
  'doc_postprocess.py',
  'doxygen.css',
  'doxygen-extra.css',
  'tagfile-to-devhelp2.xsl',
]
doctool_files = []
foreach file : doctool_basefiles
  doctool_files += 'util' / file
endforeach
install_data(doctool_files, install_dir: install_doctooldir)

# Let other modules find the utils with pkg-config.
configure_file(
  input: 'doctags' / 'mm-common-libstdc++.pc.in',
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: install_pkgconfigdir
)

configure_file(
  input: 'util' / 'mm-common-util.pc.in',
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: install_pkgconfigdir
)

configure_file(
  input: 'doctags' / 'mm-common-libstdc++-uninstalled.pc.in',
  output: '@BASENAME@',
  configuration: conf_data,
)

configure_file(
  input: 'util' / 'mm-common-util-uninstalled.pc.in',
  output: '@BASENAME@',
  configuration: conf_data,
)

# mm-common-get command.
conf_data3 = configuration_data()
conf_data3.merge_from(conf_data)
conf_data3.set('configure_input', 'mm-common-get.  Generated from util/mm-common-get.in')
conf_data3.set('datadir_py', install_prefix / install_datadir)
configure_file(
  input: 'util' / 'mm-common-get.in',
  output: '@BASENAME@',
  configuration: conf_data3,
  install_dir: install_bindir,
  install_mode: 'rwxr-xr-x'
)

# mm-common-get.1 manual page.
configure_file(
  input: 'util' / 'mm-common-get.1.in',
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: install_man1dir
)

# mm-common-prepare command.
conf_data4 = configuration_data()
conf_data4.merge_from(conf_data)
conf_data4.set('configure_input', 'mm-common-prepare.  Generated from util/mm-common-prepare.in')
configure_file(
  input: 'util' / 'mm-common-prepare.in',
  output: '@BASENAME@',
  configuration: conf_data4,
  install_dir: install_bindir,
  install_mode: 'rwxr-xr-x'
)

# mm-common-prepare.1 manual page.
configure_file(
  input: 'util' / 'mm-common-prepare.1.in',
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: install_man1dir
)

# Skeleton project.
skeletonmm_basefiles = [
  '.gitignore',
  'AUTHORS',
  'COPYING',
  'ChangeLog',
  'meson.build',
  'meson_options.txt',
  'README',
  'skeletonmm.doap',
  'doc/reference/Doxyfile.in',
  'doc/reference/meson.build',
  'examples/meson.build',
  'examples/example1/main.cc',
  'skeleton/meson.build',
  'skeleton/skeletonmm-uninstalled.pc.in',
  'skeleton/skeletonmm.h',
  'skeleton/skeletonmm.pc.in',
  'skeleton/skeletonmmconfig.h.in',
  'skeleton/skeletonmm/meson.build',
  'skeleton/skeletonmm/wrap_init.h',
  'skeleton/src/skeleton.ccg',
  'skeleton/src/skeleton.defs',
  'skeleton/src/skeleton.hg',
  'skeleton/src/skeleton_docs.xml',
  'skeleton/src/skeleton_enums.defs',
  'skeleton/src/skeleton_methods.defs',
  'skeleton/src/skeleton_signals.defs',
  'skeleton/src/skeleton_vfuncs.defs',
  'tests/meson.build',
  'tests/test1/main.cc',
  'tests/test2/main.cc',
  'tools/generate_defs_and_docs.sh',
  'tools/extra_defs_gen/generate_defs_skeleton.cc',
  'tools/extra_defs_gen/meson.build',
  'tools/m4/convert.m4',
  'tools/m4/convert_skeleton.m4',
  'untracked/README',
]
skeletonmm_files = []
foreach file : skeletonmm_basefiles
  skeletonmm_files += 'skeletonmm' / file
endforeach

# Create tar archive of skeletonmm for installation.
skeletonmm_tarball_script = script_dir / 'skeletonmm-tarball.py'
tarball_filetype = run_command(python3,
  skeletonmm_tarball_script, 'check',
  check: true,
)
tarball_filename = 'skeletonmm' + tarball_filetype.stdout()
custom_target(tarball_filename,
  input: skeletonmm_files,
  output: tarball_filename,
  command: [
    python3,
    skeletonmm_tarball_script,
    '@OUTPUT@',
    project_source_root,
    skeletonmm_files,
  ],
  build_by_default: true,
  install_dir: install_docdir,
  install: true
)
install_data('OVERVIEW.md', 'README.md', install_dir: install_docdir)

# Either curl or wget is required for downloading libstdc++.tag,
# used by Doxygen.
download_cmd = 'none'
if get_option('use-network')
  curl = find_program('curl', required: false)
  if curl.found()
    download_cmd = curl.full_path()
  else
    wget = find_program('wget', required: true)
    download_cmd = wget.full_path()
  endif
endif

# Download libstdc++.tag if it does not exist or if it's out of date.
tag_file = custom_target('libstdc++.tag',
  output: 'libstdc++.tag',
  command: [
    python3,
    script_dir / 'libstdcxx-tag.py',
    download_cmd,
    project_source_root / 'doctags',
    '@OUTPUT@',
  ],
  build_by_default: true,
  build_always_stale: true,
  install_dir: install_doctagsdir,
  install: true
)

if not meson.is_subproject() or meson.version().version_compare('>= 0.58.0')
  # Modify the contents of the distribution directory.
  # (not allowed in a subproject if meson.version() < 0.58.0)
  meson.add_dist_script(
    python3, script_dir / 'extra-dist-cmd.py',
    project_source_root,
    project_build_root,
  )
endif

if meson.is_subproject()
  # A version of mm-common-get that can be executed uninstalled.
  conf_data_subproj = configuration_data()
  conf_data_subproj.merge_from(conf_data)
  conf_data_subproj.set('configure_input', 'mm-common-get2 (for execution uninstalled).  Generated from util/mm-common-get.in')
  conf_data_subproj.set('datadir_py', project_build_root)
  mm_common_get2 = configure_file(
    input: 'util' / 'mm-common-get.in',
    output: 'mm-common-get2',
    configuration: conf_data_subproj,
    install: false,
  )
  # Make the uninstalled mm-common-get2 executable.
  cmd_py = '''
import os
import sys
os.chmod(sys.argv[1], 0o755)'''
  run_command(python3, '-c', cmd_py,
    project_build_root / 'mm-common-get2',
    check: true,
  )

  # A main project that looks for mm-common-get shall find mm_common_get2.
  meson.override_find_program('mm-common-get', mm_common_get2)

  # Copy files needed by mm-common-get2 from source dir to build dir.
  # The directory structure must be the same as in the installation directory.
  run_command(python3, script_dir / 'copy-files.py',
    project_source_root / 'util' / 'build_scripts',
    project_build_root / meson.project_name() / 'build',
    meson_build_support_basefiles,
    check: true,
  )
  run_command(python3, script_dir / 'copy-files.py',
    project_source_root / 'util',
    project_build_root / meson.project_name() / 'doctool',
    doctool_basefiles,
    check: true,
  )

  mm_common_libstdc_dep = declare_dependency(
    variables: {
      'doxytagfile': project_build_root / 'libstdc++.tag',
      'htmlrefpub': 'http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/'
    }
  )
  # A main project that looks for mm-common-libstdc++.pc shall find mm_common_libstdc_dep.
  meson.override_dependency('mm-common-libstdc++', mm_common_libstdc_dep)

  # May be used in a main project.
  global_tag_file_target = tag_file
endif

# Print a summary.
summary = [
  '',
  '------',
  meson.project_name() + ' ' + meson.project_version(),
  '',
  '       Use network: @0@'.format(get_option('use-network')),
  'Directories:',
  '            prefix: @0@'.format(install_prefix),
  '            bindir: @0@'.format(install_prefix / install_bindir),
  '           datadir: @0@'.format(install_prefix / install_datadir),
  '            docdir: @0@'.format(install_prefix / install_docdir),
  '  aclocal_macrodir: @0@'.format(install_prefix / install_aclocal_macrodir),
  '      pkgconfigdir: @0@'.format(install_prefix / install_pkgconfigdir),
  '        pkgdatadir: @0@'.format(install_prefix / install_pkgdatadir),
  '  build_supportdir: @0@'.format(install_prefix / install_build_supportdir),
  '        doctooldir: @0@'.format(install_prefix / install_doctooldir),
  '        doctagsdir: @0@'.format(install_prefix / install_doctagsdir),
  '           man1dir: @0@'.format(install_prefix / install_man1dir),
  '------'
]

message('\n'.join(summary))
