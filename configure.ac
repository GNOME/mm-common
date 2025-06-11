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

AC_INIT([mm-common], [1.0.7], [https://gitlab.gnome.org/GNOME/mm-common/issues/],
        [mm-common], [https://gtkmm.gnome.org/])
AC_PREREQ([2.59])
AC_CONFIG_SRCDIR([util/mm-common-prepare.in])

AM_INIT_AUTOMAKE([1.9 -Wno-portability check-news no-dist-gzip dist-xz no-define std-options foreign])
# Support silent build rules.
# Disable by either passing --disable-silent-rules to configure or passing V=1 to make.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])
AM_MAINTAINER_MODE

AC_ARG_VAR([ACLOCAL_FLAGS], [aclocal flags, e.g. -I <macro dir>])
AC_ARG_VAR([CURL], [curl transfer command])
AC_ARG_VAR([WGET], [wget download command])

AC_PROG_SED
## List of tar execs is taken from the generated ./missing script.
AC_CHECK_PROGS([TAR], [tar gnutar gtar], [no])
AS_IF([test "x$TAR" = xno], [AC_MSG_ERROR([tar utility not found])])

AC_MSG_CHECKING([whether to download libstdc++ tags])
AC_ARG_ENABLE([network],
              [AS_HELP_STRING([[--disable-network]],
                              [do not attempt to download libstdc++ tags]
                              [[default=enabled in maintainer mode]])],
              [USE_NETWORK=$enableval], [USE_NETWORK=$USE_MAINTAINER_MODE])
AC_MSG_RESULT([$USE_NETWORK])
AC_SUBST([USE_NETWORK])

AC_CHECK_PROG([CURL], [curl], [curl])
AC_CHECK_PROG([WGET], [wget], [wget])

AS_IF([test "x$USE_NETWORK$CURL$WGET" = xyes],
      [AC_MSG_ERROR([[Either curl or wget is required to download the libstdc++ tags.]])])

eval "datadir_py=${datarootdir}"
AC_SUBST([datadir_py])

AC_CONFIG_FILES([
  Makefile
  doctags/mm-common-libstdc++.pc
  doctags/mm-common-libstdc++-uninstalled.pc
  macros/mm-common.m4
  util/mm-common-prepare
  util/mm-common-get
  util/mm-common-util.pc
  util/mm-common-util-uninstalled.pc
])
AC_OUTPUT
