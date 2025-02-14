# skeleton

# Input: install_includedir, skeletonmm_pcname, install_libdir,
#        build_deprecated_api, skeletonmm_major_version,
#        skeletonmm_minor_version, skeletonmm_micro_version
# Output: install_includeconfigdir

pkg_conf_data = configuration_data()
if not build_deprecated_api
  pkg_conf_data.set('SKELETONMM_DISABLE_DEPRECATED', true)
endif
pkg_conf_data.set('SKELETONMM_MAJOR_VERSION', skeletonmm_major_version)
pkg_conf_data.set('SKELETONMM_MINOR_VERSION', skeletonmm_minor_version)
pkg_conf_data.set('SKELETONMM_MICRO_VERSION', skeletonmm_micro_version)

install_includeconfigdir = install_libdir / skeletonmm_pcname / 'include'
configure_file(
  input: 'skeletonmmconfig.h.in',
  output: '@BASENAME@',
  configuration: pkg_conf_data,
  install: true,
  install_dir: install_includeconfigdir,
  install_tag: 'devel',
)

subdir('skeletonmm')
