# This file is part of mm-common.

project('mm-common',
  version: '0.9.12',
  meson_version: '>= 0.49.0',
  license: 'GPLv2+'
)

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
    'util' / 'meson_aux' / 'extra-install-cmd.sh',
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
  'doc-postprocess.pl',
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
  'autogen.sh',
  '.gitignore',
  'AUTHORS',
  'COPYING',
  'ChangeLog',
  'Makefile.am',
  'README',
  'configure.ac',
  'skeletonmm.doap',
  'build/.gitignore',
  'codegen/generate_defs_and_docs.sh',
  'codegen/Makefile.am',
  'codegen/extradefs/generate_extra_defs_skeleton.cc',
  'codegen/m4/convert.m4',
  'codegen/m4/convert_skeleton.m4',
  'codegen/m4/filelist.am',
  'doc/Makefile.am',
  'doc/reference/.gitignore',
  'doc/reference/Doxyfile.in',
  'examples/.gitignore',
  'examples/Makefile.am',
  'examples/example/example.cc',
  'skeleton/.gitignore',
  'skeleton/skeletonmm-uninstalled.pc.in',
  'skeleton/skeletonmm.h',
  'skeleton/skeletonmm.pc.in',
  'skeleton/skeletonmmconfig.h.in',
  'skeleton/skeletonmm/Makefile.am',
  'skeleton/skeletonmm/filelist.am',
  'skeleton/skeletonmm/wrap_init.h',
  'skeleton/skeletonmm/private/.gitignore',
  'skeleton/src/Makefile.am',
  'skeleton/src/filelist.am',
  'skeleton/src/skeleton.ccg',
  'skeleton/src/skeleton.defs',
  'skeleton/src/skeleton.hg',
  'skeleton/src/skeleton_docs.xml',
  'skeleton/src/skeleton_enum.defs',
  'skeleton/src/skeleton_method.defs',
  'skeleton/src/skeleton_signal.defs',
  'skeleton/src/skeleton_vfunc.defs',
]
skeletonmm_files = []
foreach file : skeletonmm_basefiles
  skeletonmm_files += 'skeletonmm' / file
endforeach

# tar and either xz or gzip are required for the skeletonmm.tar.[xz|gz] file.
tar = find_program('tar', required: true)
xz = find_program('xz', required: false)
if not xz.found()
  gzip = find_program('gzip', required: true)
endif

# Create tar archive of skeletonmm for installation.
tarball_filename = xz.found() ? 'skeletonmm.tar.xz' : 'skeletonmm.tar.gz'
custom_target(tarball_filename,
  input: skeletonmm_files,
  output: tarball_filename,
  command: [
    files('util' / 'meson_aux' / 'skeletonmm-tarball.sh'),
    meson.current_source_dir(),
    '@OUTPUT@',
    skeletonmm_files,
  ],
  build_by_default: true,
  install_dir: install_docdir,
  install: true
)
install_data('README', install_dir: install_docdir)

# Either curl or wget is required for downloading libstdc++.tag,
# used by Doxygen.
download_cmd = 'none'
if get_option('use-network')
  curl = find_program('curl', required: false)
  download_cmd = 'curl'
  if not curl.found()
    wget = find_program('wget', required: true)
    download_cmd = 'wget'
  endif
endif

# Download libstdc++.tag if it does not exist or if it's out of date.
custom_target('libstdc++.tag',
  output: 'libstdc++.tag',
  command: [
    files('util' / 'meson_aux' / 'libstdcxx-tag.sh'),
    download_cmd,
    meson.current_source_dir() / 'doctags',
    '@OUTPUT@',
  ],
  build_by_default: true,
  build_always_stale: true,
  install_dir: install_doctagsdir,
  install: true
)

if not meson.is_subproject()
  # Modify the contents of the distribution directory. (not allowed in a subproject)
  meson.add_dist_script(
    'util' / 'meson_aux' / 'extra-dist-cmd.sh',
    meson.current_source_dir(),
    meson.current_build_dir(),
  )
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
