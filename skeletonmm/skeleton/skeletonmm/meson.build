# skeleton/skeletonmm

# Input: skeletonmm_build_dep, skeletonmm_pcname, maintainer_mode, project_source_root,
#        generate_binding, m4_files, skeletonmm_libversion, install_includedir,
#        macos_darwin_versions, python3
# Output: hg_ccg_basenames, extra_h_files, built_h_file_targets, built_files_root,
#         skeletonmm_own_dep

defs_basefiles = [
  'skeleton.defs',
  'skeleton_methods.defs',
  'skeleton_enums.defs',
  'skeleton_signals.defs',
  'skeleton_vfuncs.defs',
  'skeleton_docs.xml',
]

defs_files = []
foreach file : defs_basefiles
  defs_files += '..' / 'src' / file
endforeach

hg_ccg_basenames = [
  'skeleton',
]

extra_cc_files = [
]

extra_h_files = [
  'wrap_init.h',
]

install_headers('..' / 'skeletonmm.h', subdir: skeletonmm_pcname)
install_headers(extra_h_files, subdir: skeletonmm_pcname / 'skeletonmm')

untracked_skeletonmm = 'untracked' / 'skeleton' / 'skeletonmm'
rel_untracked_skeletonmm = '..' / '..' / untracked_skeletonmm
src_untracked_skeletonmm = project_source_root / untracked_skeletonmm

if maintainer_mode

  # Maintainer mode. Generate .h and .cc files from .hg and .ccg files in ../src.

  # doc/reference/meson.build needs this.
  built_files_root = project_build_root
  built_h_file_targets = []

  # Force meson+ninja to generate source files before anything is compiled.
  # Compilation must depend on these targets.
  built_cc_file_targets = []

  hg_files = []
  foreach file : hg_ccg_basenames
    hg_files += '..' / 'src' / file + '.hg'
  endforeach

  # Create wrap_init.cc in project_build_root/skeleton/skeletonmm.
  built_cc_file_targets += custom_target('wrap_init.cc',
    input: hg_files,
    output: 'wrap_init.cc',
    command: [
      python3, generate_binding, 'generate_wrap_init',
      gmmproc_dir,
      '@OUTPUT@',
      'Skeleton', # namespace
      '@INPUT@',
    ],
    build_by_default: maintainer_mode,
    install: false,
  )

  # Create .h/_p.h/.cc files from .hg/.ccg files in project_build_root/skeleton/skeletonmm.
  foreach file : hg_ccg_basenames
    hg_file = '..' / 'src' / file + '.hg'
    ccg_file = '..' / 'src' / file + '.ccg'
    built_file_target = custom_target(file + '.cc',
      input: [hg_file, ccg_file],
      output: [file + '.stamp', file + '.cc', file + '.h'],
      command: [
        python3, generate_binding, 'gmmproc',
        gmmproc_dir,
        '@OUTPUT0@',
        file,
        meson.current_source_dir() / '..' / 'src',
        project_source_root / 'tools' / 'm4',
      ],
      depend_files: defs_files + m4_files,
      build_by_default: maintainer_mode,
      install: false,
    )
    built_cc_file_targets += built_file_target[1]
    built_h_file_targets += built_file_target[2]
  endforeach

  extra_include_dirs = ['..']
  skeletonmm_library = library(skeletonmm_pcname,
    built_cc_file_targets, built_h_file_targets, extra_cc_files,
    version: skeletonmm_libversion,
    darwin_versions: macos_darwin_versions,
    implicit_include_directories: false,
    include_directories: extra_include_dirs,
    dependencies: skeletonmm_build_dep,
    install: true,
  )

  built_h_cc_dir = meson.current_build_dir()

else # not maintainer_mode

  # Not maintainer mode. Compile built source code files in
  # project_source_root/untracked/skeleton/skeletonmm.

  # doc/reference/meson.build needs these.
  built_files_root = project_source_root / 'untracked'
  built_h_file_targets = []

  # Two cases:
  # 1. The source code comes from a tarball, where the built files
  #    are stored in project_source_root/untracked.
  #    There are no built files in the build tree.
  # 2. Files have been built in the build tree. Then maintainer_mode has
  #    been changed from true to false. Files that are missing or not up to date
  #    in project_source_root/untracked are copied from the build tree.

  # Try to copy built source code files to the source tree.
  run_command(
    python3, generate_binding, 'copy_built_files',
    meson.current_build_dir(),
    src_untracked_skeletonmm,
    hg_ccg_basenames,
    check: true,
  )

  built_cc_files = [ rel_untracked_skeletonmm / 'wrap_init.cc' ]
  foreach file : hg_ccg_basenames
    built_cc_files += rel_untracked_skeletonmm / file + '.cc'
  endforeach

  extra_include_dirs = [ '..', '..' / '..' / 'untracked' / 'skeleton' ]
  skeletonmm_library = library(skeletonmm_pcname,
    built_cc_files, extra_cc_files,
    version: skeletonmm_libversion,
    darwin_versions: macos_darwin_versions,
    implicit_include_directories: false,
    include_directories: extra_include_dirs,
    dependencies: skeletonmm_build_dep,
    install: true,
  )

  built_h_cc_dir = src_untracked_skeletonmm

endif

# Generate .pc files, used by pkg-config.
pkg_config = import('pkgconfig')
pc_common_variables = [
  'doxytagfile=${docdir}/reference/' + skeletonmm_pcname + '.tag',
  'htmlrefdir=${docdir}/reference/html',
  'htmlrefpub=https://gnome.pages.gitlab.gnome.org/' + meson.project_name(),
]
pc_variables = [
  'gmmprocm4dir=${libdir}/' + skeletonmm_pcname + '/proc/m4',
  'docdir=${datadir}/doc/' + skeletonmm_pcname,
] + pc_common_variables
pc_uninstalled_variables = [
  'gmmprocm4dir=${srcdir}/tools/m4',
  'docdir=${prefix}/doc',
] + pc_common_variables

pkg_config.generate(skeletonmm_library,
  filebase: skeletonmm_pcname,
  variables: pc_variables,
  uninstalled_variables: pc_uninstalled_variables,
  name: meson.project_name(),
  description: 'C++ binding for skeleton',
  url: 'https://gtkmm.gnome.org/',
  subdirs: [skeletonmm_pcname],
  extra_cflags: ['-I${libdir}/' + skeletonmm_pcname + '/include'],
)

# Install built .h and _p.h files.
meson.add_install_script(
  python3, generate_binding, 'install_built_h_files',
  built_h_cc_dir,
  install_includedir / skeletonmm_pcname / 'skeletonmm', # subdir below {prefix}
  hg_ccg_basenames,
  install_tag: 'devel',
)

# Distribute built files.
meson.add_dist_script(
  python3, generate_binding, 'dist_built_files',
  built_h_cc_dir,
  untracked_skeletonmm,
  hg_ccg_basenames,
)

# This is used when building example programs and test programs.
# It's also a part of skeletonmm_dep, when skeletonmm is a subproject.
skeletonmm_own_dep = declare_dependency(
  sources: built_h_file_targets,
  link_with: skeletonmm_library,
  include_directories: extra_include_dirs,
  dependencies: skeletonmm_build_dep
)
