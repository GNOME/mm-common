# tools/extra_defs_gen

# Input: cpp_compiler, skeletonmm_build_dep, install_libdir, skeletonmm_pcname
# Output: m4_files, install_m4dir

glibmm_generate_extra_defs_dep = cpp_compiler.find_library(
  'glibmm_generate_extra_defs-2.68',
# or:  'glibmm_generate_extra_defs-2.4',
)

executable('generate_defs_skeleton', 'generate_defs_skeleton.cc',
  dependencies: [skeletonmm_build_dep, glibmm_generate_extra_defs_dep],
  implicit_include_directories: false,
  install: false,
)

# Install m4 files for reuse by other *mm projects, when building from git.
m4_basefiles = [
  'convert.m4',
  'convert_skeleton.m4',
]
m4_files = []
foreach file : m4_basefiles
  m4_files += '..' / 'm4' / file
endforeach
m4_files = files(m4_files)
install_m4dir = install_libdir / skeletonmm_pcname / 'proc' / 'm4'
install_data(m4_files, install_dir: install_m4dir)
