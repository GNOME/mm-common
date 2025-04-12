## Copyright (c) 2009  Openismus GmbH  <http://www.openismus.com/>
##
## This file is part of mm-common.
##
## mm-common is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation, either version 2 of the License,
## or (at your option) any later version.
##
## mm-common is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with mm-common.  If not, see <http://www.gnu.org/licenses/>.

# Pick up aclocal flags from the environment.
ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS}

bin_SCRIPTS = util/mm-common-prepare util/mm-common-get
man1_MANS = util/mm-common-prepare.1 util/mm-common-get.1

# These are installed so that mm-common-prepare can copy the .am files
# into projects at autogen.sh time, and mm-common-get can copy the .py files
# at Meson setup or configure time:
build_supportdir = $(pkgdatadir)/build
dist_build_support_DATA =		\
	am_include/compile-binding.am	\
	am_include/dist-changelog.am		\
	am_include/doc-reference.am		\
	am_include/generate-binding.am \
  util/build_scripts/check-dllexport-usage.py \
  util/build_scripts/dist-build-scripts.py \
  util/build_scripts/dist-changelog.py \
  util/build_scripts/doc-reference.py \
  util/build_scripts/generate-binding.py

# These are installed so that aclocal can copy them into aclocal.m4
# at autogen.sh time:
aclocal_macrodir = $(datadir)/aclocal
aclocal_macro_DATA = macros/mm-common.m4
dist_aclocal_macro_DATA =		\
	macros/mm-ax_cxx_compile_stdcxx.m4	\
	macros/mm-ax_cxx_compile_stdcxx_11.m4	\
	macros/mm-dietlib.m4		\
	macros/mm-doc.m4		\
	macros/mm-module.m4		\
	macros/mm-pkg.m4		\
	macros/mm-warnings.m4

# These are installed so that mm-common-prepare can copy them into projects
# at autogen.sh time if a directory path is given to MM_CONFIG_DOCTOOL_DIR(),
# or they can be found via pkg-config --variable=doctooldir mm-common-util,
# which is preferrable.
# mm-common-get can copy them at Meson setup or configure time.
doctooldir = $(pkgdatadir)/doctool
dist_doctool_DATA =			\
	util/doc-install.pl		\
	util/doc_install.py		\
	util/doc-postprocess.pl		\
	util/doc_postprocess.py		\
	util/doxygen.css		\
	util/doxygen-extra.css		\
	util/tagfile-to-devhelp2.xsl

doctagsdir = $(pkgdatadir)/doctags
dist_doctags_DATA = doctags/libstdc++.tag

# Let other modules find the utils with pkg-config:
shared_pkgconfigdir = $(datadir)/pkgconfig
nodist_shared_pkgconfig_DATA =		\
	doctags/mm-common-libstdc++.pc	\
	util/mm-common-util.pc

noinst_DATA = \
	doctags/mm-common-libstdc++-uninstalled.pc \
	util/mm-common-util-uninstalled.pc

dist_doc_DATA = README.md OVERVIEW.md
doc_DATA = skeletonmm.tar.gz

skeletonmm_data_files =							\
	skeletonmm/.gitignore						\
	skeletonmm/AUTHORS						\
	skeletonmm/COPYING						\
	skeletonmm/COPYING.tools			\
	skeletonmm/ChangeLog						\
	skeletonmm/meson.build					\
	skeletonmm/meson_options.txt		\
	skeletonmm/README						\
	skeletonmm/skeletonmm.doap					\
	skeletonmm/doc/reference/Doxyfile.in		\
	skeletonmm/doc/reference/meson.build		\
	skeletonmm/examples/meson.build					\
	skeletonmm/examples/example1/main.cc		\
	skeletonmm/skeleton/meson.build					\
	skeletonmm/skeleton/skeletonmm.h				\
	skeletonmm/skeleton/skeletonmmconfig.h.in			\
	skeletonmm/skeleton/skeletonmm/meson.build			\
	skeletonmm/skeleton/skeletonmm/wrap_init.h			\
	skeletonmm/skeleton/src/skeleton.ccg				\
	skeletonmm/skeleton/src/skeleton.defs				\
	skeletonmm/skeleton/src/skeleton.hg				\
	skeletonmm/skeleton/src/skeleton_docs.xml			\
	skeletonmm/skeleton/src/skeleton_enums.defs		\
	skeletonmm/skeleton/src/skeleton_methods.defs \
	skeletonmm/skeleton/src/skeleton_signals.defs \
	skeletonmm/skeleton/src/skeleton_vfuncs.defs \
	skeletonmm/tests/meson.build \
	skeletonmm/tests/test1/main.cc \
	skeletonmm/tests/test2/main.cc \
	skeletonmm/tools/extra_defs_gen/generate_defs_skeleton.cc \
	skeletonmm/tools/extra_defs_gen/meson.build	\
	skeletonmm/tools/m4/convert.m4				\
	skeletonmm/tools/m4/convert_skeleton.m4			\
	skeletonmm/untracked/README

skeletonmm_script_files = \
  skeletonmm/tools/generate_defs_and_docs.sh

skeletonmm_files = $(skeletonmm_script_files) $(skeletonmm_data_files)

dist_noinst_DATA = util/mm-common-prepare.1.in util/mm-common-get.1.in $(skeletonmm_data_files)
dist_noinst_SCRIPTS = autogen.sh $(skeletonmm_script_files)

CLEANFILES = $(man1_MANS) $(doc_DATA)
MAINTAINERCLEANFILES = $(dist_doctags_DATA)

# Distribute files needed when building mm-common with meson.
EXTRA_DIST = \
  meson.build \
  meson_options.txt \
  util/meson_aux/copy-files.py \
  util/meson_aux/extra-dist-cmd.py \
  util/meson_aux/extra-install-cmd.py \
  util/meson_aux/libstdcxx-tag.py \
  util/meson_aux/skeletonmm-tarball.py

# Remote location of the GNU libstdc++ Doxygen tag file.
libstdcxx_tag_url = http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/libstdc++.tag

# Commands for downloading a target from a remote location, taking care
# not to download a file again if its time stamp has not changed.
download_curl = $(CURL) --compressed --connect-timeout 300 -g -L -m 3600 -R --retry 5 \
		$(if $(wildcard $@),-z $@) -o $@
download_wget = $(WGET) -N -nd -T 300 -t 5 -P $(dir $@)

subst_manpage = $(SED) 's|[@]PACKAGE_STRING[@]|$(PACKAGE_STRING)|g;s|[@]docdir[@]|$(docdir)|g'
srctar_stdout = cd $(top_srcdir) >/dev/null && $(TAR) chof -

# If network access is enabled (either by explicit user request or by default
# if in maintainer mode), then always check the remote location of the tag file
# for updates when building the default target.
check_updates = $(and $(USE_NETWORK:no=),$(filter all%,$(or $(MAKECMDGOALS),all)),$(dist_doctags_DATA))

# By declaring a target phony, its rule is always executed.
.PHONY: $(check_updates) postinst-acdir-notice

# Avoid shipping partially downloaded files.
.DELETE_ON_ERROR:

# Download the libstdc++ tag file from the GCC website.
doctags/libstdc++.tag:
	@$(if $(USE_NETWORK:no=),:,echo 'Error: $@ does not exist.' >&2; \
	echo 'Downloading it is not possible because network is disabled.' >&2; \
	echo 'Please run "$(MAKE) USE_NETWORK=yes", or reconfigure with' >&2; \
	echo 'the --enable-network option.' >&2; exit 1)
	$(AM_V_GEN)$(if\
	$(CURL),$(download_curl) '$(libstdcxx_tag_url)',$(if\
	$(WGET),$(download_wget) '$(libstdcxx_tag_url)',test -f $@))

# Build the mm-common-prepare(1) manual page.
util/mm-common-prepare.1: $(srcdir)/util/mm-common-prepare.1.in Makefile
	$(AM_V_GEN)$(subst_manpage) $(srcdir)/util/mm-common-prepare.1.in >$@

# Build the mm-common-get(1) manual page.
util/mm-common-get.1: $(srcdir)/util/mm-common-get.1.in Makefile
	$(AM_V_GEN)$(subst_manpage) $(srcdir)/util/mm-common-get.1.in >$@

# Create tar archive of skeletonmm for installation.
skeletonmm.tar.gz: $(skeletonmm_files)
	$(AM_V_GEN)($(srctar_stdout) $(skeletonmm_files)) | gzip -c -n >$@

include $(top_srcdir)/am_include/dist-changelog.am

install-data-hook: $(if $(DESTDIR),,postinst-acdir-notice)

# Inform the installer that M4 macro files installed in a prefix
# not known to aclocal will not be picked up automatically.
postinst-acdir-notice:
	@$(POST_INSTALL)
	@-acdir=`$${ACLOCAL-aclocal} --print-ac-dir 2>/dev/null || :`; \
	case ":$$ACLOCAL_PATH:$$acdir:" in *':$(aclocal_macrodir):'*) ;; *) \
	  echo; echo 'NOTICE:'; echo; \
	  echo 'The $(PACKAGE_NAME) Autoconf macro files have been installed in a different'; \
	  echo 'prefix than the system aclocal directory.  In order for the installed'; \
	  echo 'macros to be found, it may be necessary to add the $(PACKAGE_NAME) include'; \
	  echo 'path to the ACLOCAL_PATH environment variable:'; echo; \
	  echo '  ACLOCAL_PATH="$(aclocal_macrodir)"'; \
	  echo '  export ACLOCAL_PATH'; echo;; \
	esac
