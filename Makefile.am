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

bin_SCRIPTS = util/mm-common-prepare

build_supportdir = $(pkgdatadir)/build
dist_build_support_DATA =		\
	build/compile-binding.am	\
	build/dist-changelog.am		\
	build/doc-reference.am		\
	build/generate-binding.am

aclocal_macrodir = $(datadir)/aclocal
aclocal_macro_DATA = macros/mm-common.m4
dist_aclocal_macro_DATA =		\
	macros/mm-dietlib.m4		\
	macros/mm-doc.m4		\
	macros/mm-module.m4		\
	macros/mm-pkg.m4		\
	macros/mm-warnings.m4

doctooldir = $(pkgdatadir)/doctool
dist_doctool_DATA =			\
	util/doc-install.pl		\
	util/doc-postprocess.pl		\
	util/tagfile-to-devhelp2.xsl

doctagsdir = $(pkgdatadir)/doctags
dist_doctags_DATA = doctags/libstdc++.tag

shared_pkgconfigdir = $(datadir)/pkgconfig
nodist_shared_pkgconfig_DATA = doctags/mm-common-libstdc++.pc
noinst_DATA = doctags/mm-common-libstdc++-uninstalled.pc

dist_noinst_SCRIPTS = autogen.sh

MAINTAINERCLEANFILES = $(dist_doctags_DATA)

# Remote location of the GNU libstdc++ Doxygen tag file.
libstdcxx_tag_url = http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/libstdc++.tag

# Commands for downloading a target from a remote location, taking care
# not to download a file again if its time stamp has not changed.
download_curl = $(CURL) --compressed --connect-timeout 300 -g -L -m 3600 -R --retry 5 \
		$(if $(wildcard $@),-z '$@') -o '$@'
download_wget = $(WGET) -N -nd -T 300 -t 5 -P '$(dir $@)'

# If maintainer mode is enabled, always check the remote locations
# of the tag files for updates when building the default target.
if MAINTAINER_MODE
check_updates = $(if $(filter all%,$(or $(MAKECMDGOALS),all)),$(dist_doctags_DATA))
else
check_updates =
endif

.PHONY: $(check_updates)

# Avoid shipping partially downloaded files.
.DELETE_ON_ERROR:

# Download the libstdc++ tag file from the GCC website.
doctags/libstdc++.tag:
	$(if $(CURL),$(download_curl) '$(libstdcxx_tag_url)',$(if\
	     $(WGET),$(download_wget) '$(libstdcxx_tag_url)',test -f '$@'))

include $(top_srcdir)/build/dist-changelog.am
