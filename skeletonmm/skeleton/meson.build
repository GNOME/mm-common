# skeleton

# Input: install_includedir, skeletonmm_pcname, skeletonmm_requires,
#        install_pkgconfigdir, install_libdir, build_deprecated_api,
#        skeletonmm_major_version, skeletonmm_minor_version, skeletonmm_micro_version
# Output: install_includeconfigdir

pkg_config = import('pkgconfig')
pc_variables = [
  'gmmprocm4dir=${libdir}/' + skeletonmm_pcname + '/proc/m4',
  'docdir=${datadir}/doc/' + skeletonmm_pcname,
  'doxytagfile=${docdir}/reference/' + skeletonmm_pcname + '.tag',
  'htmlrefdir=${docdir}/reference/html',
  'htmlrefpub=https://gnome.pages.gitlab.gnome.org/' + meson.project_name(),
]
pkg_config.generate(
  filebase: skeletonmm_pcname,
  variables: pc_variables,
  name: meson.project_name(),
  description: 'C++ binding for skeleton',
  url: 'https://www.gtkmm.org/',
  version: meson.project_version(),
  requires: skeletonmm_requires,
  libraries: '-L${libdir} -l' + skeletonmm_pcname,
  subdirs: [skeletonmm_pcname],
  extra_cflags: ['-I${libdir}/' + skeletonmm_pcname + '/include'],
  install_dir: install_pkgconfigdir,
)

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
  install_dir: install_includeconfigdir,
)

subdir('skeletonmm')
