# This file is part of mm-common.

project('mm-common',
  version: '0.9.12',
  meson_version: '>= 0.49.0',
  license: 'GPLv2'
)

# Installation directories.
mm_common_prefix = get_option('prefix')
mm_common_bindir = join_paths(mm_common_prefix, get_option('bindir'))

mm_common_datadir = join_paths(mm_common_prefix, get_option('datadir'))
mm_common_aclocal_macrodir = join_paths(mm_common_datadir, 'aclocal')
mm_common_pkgconfigdir = join_paths(mm_common_datadir, 'pkgconfig')
mm_common_docdir = join_paths(mm_common_datadir, 'doc', meson.project_name())

mm_common_pkgdatadir = join_paths(mm_common_datadir, meson.project_name())
mm_common_build_supportdir = join_paths(mm_common_pkgdatadir, 'build')
mm_common_doctooldir = join_paths(mm_common_pkgdatadir, 'doctool')
mm_common_doctagsdir = join_paths(mm_common_pkgdatadir, 'doctags')

mm_common_mandir = join_paths(mm_common_prefix, get_option('mandir'))
mm_common_man1dir = join_paths(mm_common_mandir, 'man1')

# Configuration data for built files:
#   doctags/mm-common-libstdc++.pc.in -> mm-common-libstdc++.pc
#   doctags/mm-common-libstdc++-uninstalled.pc.in -> mm-common-libstdc++-uninstalled.pc
#   macros/mm-common.m4.in -> mm-common.m4
#   util/mm-common-prepare.1.in -> mm-common-prepare.1
#   util/mm-common-prepare.in -> mm-common-prepare
#   util/mm-common-util.pc.in -> mm-common-util.pc
#   util/mm-common-util-uninstalled.pc.in -> mm-common-util-uninstalled.pc
conf_data = configuration_data()
conf_data.set('prefix', mm_common_prefix)
conf_data.set('datarootdir', join_paths('${prefix}', get_option('datadir')))
conf_data.set('datadir', '${datarootdir}')
conf_data.set('docdir', mm_common_docdir)
conf_data.set('PACKAGE_NAME', meson.project_name())
conf_data.set('PACKAGE_TARNAME', meson.project_name())
conf_data.set('PACKAGE_VERSION', meson.project_version())
conf_data.set('PACKAGE_STRING', meson.project_name() + ' ' + meson.project_version())

# These are installed so that mm-common-prepare can copy them
# into projects at autogen.sh time.
build_support_basefiles = [
  'compile-binding.am',
  'dist-changelog.am',
  'doc-reference.am',
  'generate-binding.am',
]
build_support_files = []
foreach i : build_support_basefiles
  build_support_files += join_paths('am_include', i)
endforeach
install_data(build_support_files, install_dir: mm_common_build_supportdir)

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
foreach i : aclocal_macro_basefiles
  aclocal_macro_files += join_paths('macros', i)
endforeach
install_data(aclocal_macro_files, install_dir: mm_common_aclocal_macrodir)

conf_data2 = configuration_data()
conf_data2.merge_from(conf_data)
conf_data2.set('configure_input', 'mm-common.m4.  Generated from macros/mm-common.m4.in')
configure_file(
  input: join_paths('macros', 'mm-common.m4.in'),
  output: '@BASENAME@',
  configuration: conf_data2,
  install_dir: mm_common_aclocal_macrodir
)

if find_program('aclocal', required: false).found()
  meson.add_install_script(
    join_paths('util', 'meson_aux', 'extra-install-cmd.sh'),
    mm_common_aclocal_macrodir
  )
endif

# These are installed so that mm-common-prepare can copy them into projects
# at autogen.sh time, if a directory path is given to MM_CONFIG_DOCTOOL_DIR(),
# or they can be found via pkg-config --variable=doctooldir mm-common-util.
doctool_basefiles = [
  'doc-install.pl',
  'doc-postprocess.pl',
  'doxygen.css',
  'doxygen-extra.css',
  'tagfile-to-devhelp2.xsl',
]
doctool_files = []
foreach i : doctool_basefiles
  doctool_files += join_paths('util', i)
endforeach
install_data(doctool_files, install_dir: mm_common_doctooldir)

# Let other modules find the utils with pkg-config.
configure_file(
  input: join_paths('doctags', 'mm-common-libstdc++.pc.in'),
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: mm_common_pkgconfigdir
)

configure_file(
  input: join_paths('util', 'mm-common-util.pc.in'),
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: mm_common_pkgconfigdir
)

configure_file(
  input: join_paths('doctags', 'mm-common-libstdc++-uninstalled.pc.in'),
  output: '@BASENAME@',
  configuration: conf_data,
)

configure_file(
  input: join_paths('util', 'mm-common-util-uninstalled.pc.in'),
  output: '@BASENAME@',
  configuration: conf_data,
)

# mm-common-prepare command.
conf_data3 = configuration_data()
conf_data3.merge_from(conf_data)
conf_data3.set('configure_input', 'mm-common-prepare.  Generated from util/mm-common-prepare.in')
configure_file(
  input: join_paths('util', 'mm-common-prepare.in'),
  output: '@BASENAME@',
  configuration: conf_data3,
  install_dir: mm_common_bindir,
  install_mode: 'rwxr-xr-x'
)

# mm-common-prepare.1 manual page.
configure_file(
  input: join_paths('util', 'mm-common-prepare.1.in'),
  output: '@BASENAME@',
  configuration: conf_data,
  install_dir: mm_common_man1dir
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
foreach i : skeletonmm_basefiles
  skeletonmm_files += join_paths('skeletonmm', i)
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
    files(join_paths('util', 'meson_aux', 'skeletonmm-tarball.sh')),
    meson.current_source_dir(),
    '@OUTPUT@',
    skeletonmm_files,
  ],
  build_by_default: true,
  install_dir: mm_common_docdir,
  install: true
)
install_data('README', install_dir: mm_common_docdir)

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
    files(join_paths('util', 'meson_aux', 'libstdcxx-tag.sh')),
    download_cmd,
    join_paths(meson.current_source_dir(), 'doctags'),
    '@OUTPUT@',
  ],
  build_by_default: true,
  build_always_stale: true,
  install_dir: mm_common_doctagsdir,
  install: true
)

# Modify the contents of the distribution directory.
meson.add_dist_script(
  join_paths('util', 'meson_aux', 'extra-dist-cmd.sh'),
  meson.current_source_dir(),
  meson.current_build_dir(),
  join_paths('meson-dist', meson.project_name() + '-' + meson.project_version()),
)

# Print a summary.
summary = [
  '',
  '------',
  meson.project_name() + ' ' + meson.project_version(),
  '',
  '       Use network: @0@'.format(get_option('use-network')),
  'Directories:',
  '            prefix: @0@'.format(mm_common_prefix),
  '            bindir: @0@'.format(mm_common_bindir),
  '           datadir: @0@'.format(mm_common_datadir),
  '            docdir: @0@'.format(mm_common_docdir),
  '  aclocal_macrodir: @0@'.format(mm_common_aclocal_macrodir),
  '      pkgconfigdir: @0@'.format(mm_common_pkgconfigdir),
  '        pkgdatadir: @0@'.format(mm_common_pkgdatadir),
  '  build_supportdir: @0@'.format(mm_common_build_supportdir),
  '        doctooldir: @0@'.format(mm_common_doctooldir),
  '        doctagsdir: @0@'.format(mm_common_doctagsdir),
  '           man1dir: @0@'.format(mm_common_man1dir),
  '------'
]

message('\n'.join(summary))
