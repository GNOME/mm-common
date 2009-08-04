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

ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS}

bin_SCRIPTS = util/mm-common-prepare

build_supportdir = $(pkgdatadir)/build
dist_build_support_DATA =		\
	build/compile-binding.am	\
	build/dist-changelog.am		\
	build/doc-reference.am		\
	build/generate-binding.am

aclocal_macrodir = $(datadir)/aclocal
dist_aclocal_macro_DATA =		\
	macros/mm-doc.m4		\
	macros/mm-module.m4		\
	macros/mm-pkg.m4		\
	macros/mm-warnings.m4

dist_noinst_DATA =			\
	util/doc-install.pl		\
	util/doc-postprocess.pl		\
	util/tagfile-to-devhelp2.xsl

dist_noinst_SCRIPTS = autogen.sh

include $(top_srcdir)/build/dist-changelog.am
