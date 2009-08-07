## Copyright (c) 2009  Daniel Elstner <daniel.kitta@gmail.com>
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

#serial 20090807

## MM_ARG_ENABLE_DOCUMENTATION
##
## Provide the --disable-documentation configure option.  By default,
## the documentation will be included in the build.  If not explicitly
## disabled, also check whether the necessary tools are installed, and
## abort if any are missing.
##
## The tools checked for are Perl, dot, Doxygen and xsltproc.  The
## substitution variables PERL, DOT, DOXYGEN and XSLTPROC are set to
## the command paths, unless overridden in the user environment.
##
## If the package provides the --enable-maintainer-mode option, the
## tools dot, Doxygen and xsltproc are mandatory only when maintainer
## mode is enabled.  Perl is required for the installdox utility even
## if not in maintainer mode.
##
AC_DEFUN([MM_ARG_ENABLE_DOCUMENTATION],
[dnl
AC_ARG_VAR([PERL], [path to Perl interpreter])[]dnl
AC_ARG_VAR([DOT], [path to dot utility])[]dnl
AC_ARG_VAR([DOXYGEN], [path to Doxygen utility])[]dnl
AC_ARG_VAR([XSLTPROC], [path to xsltproc utility])[]dnl
dnl
AC_PATH_PROG([PERL], [perl], [perl])
AC_PATH_PROG([DOT], [dot], [dot])
AC_PATH_PROG([DOXYGEN], [doxygen], [doxygen])
AC_PATH_PROG([XSLTPROC], [xsltproc], [xsltproc])
dnl
AC_ARG_ENABLE([documentation],
              [AS_HELP_STRING([--disable-documentation],
                              [do not build or install the documentation])],
              [ENABLE_DOCUMENTATION=$enableval],
              [ENABLE_DOCUMENTATION=yes])
AS_IF([test "x$ENABLE_DOCUMENTATION" != xno],
[
  AS_IF([test "x$PERL" = xperl],
        [AC_MSG_FAILURE([[Perl is required for installing the documentation.]])])

  AS_IF([test "x$USE_MAINTAINER_MODE" != xno],
  [
    for mm_prog in "$DOT" "$DOXYGEN" "$XSLTPROC"
    do
      AS_CASE([$mm_prog], [[dot|doxygen|xsltproc]],
              [AC_MSG_FAILURE([[The documentation will be built in this configuration,
but the required tool $mm_prog could not be found.]])])
    done
  ])[]dnl
])
AM_CONDITIONAL([ENABLE_DOCUMENTATION], [test "x$ENABLE_DOCUMENTATION" != xno])
AC_SUBST([DOXYGEN_TAGFILES], [[]])
AC_SUBST([DOCINSTALL_FLAGS], [[]])[]dnl
])

## _MM_ARG_WITH_TAGFILE_DOC(option-basename, tagfilename, [module])
##
m4_define([_MM_ARG_WITH_TAGFILE_DOC],
[dnl
  AC_MSG_CHECKING([for $1 documentation])
  AC_ARG_WITH([$1-doc],
              [AS_HELP_STRING([[--with-$1-doc=[TAGFILE@]HTMLREFDIR]],
                              [Link to external $1 documentation]m4_ifval([$3], [[ [auto]]]))],
  [
    mm_htmlrefdir=`[expr "@$withval" : '.*@\(.*\)' 2>&]AS_MESSAGE_LOG_FD`
    mm_tagname=`[expr "/$withval" : '[^@]*[\\/]\([^\\/@]*\)@' 2>&]AS_MESSAGE_LOG_FD`
    mm_tagpath=`[expr "X$withval" : 'X\([^@]*\)@' 2>&]AS_MESSAGE_LOG_FD`
    test "x$mm_tagname" != x || mm_tagname="$2"
    test "x$mm_tagpath" != x || mm_tagpath=$mm_tagname[]dnl
  ], [
    mm_htmlrefdir=
    mm_tagname="$2"
    mm_tagpath=$mm_tagname[]dnl
  ])
  AS_CASE([$mm_tagpath], [[.[\\/]*|..[\\/]*]], [mm_tagpath=`pwd`/$mm_tagpath])
m4_ifval([$3], [dnl
  AS_IF([test "x$mm_htmlrefdir" = x],
  [
    mm_htmlrefdir=`$PKG_CONFIG --variable=htmlrefdir "$3" 2>&AS_MESSAGE_LOG_FD`dnl
  ])
  AS_CASE([$mm_htmlrefdir], [[http://*|https://*]], [mm_htmlrefpub=$mm_htmlrefdir],
  [
    mm_htmlrefpub=`$PKG_CONFIG --variable=htmlrefpub "$3" 2>&AS_MESSAGE_LOG_FD`
    test "x$mm_htmlrefpub" != x || mm_htmlrefpub=$mm_htmlrefdir
    test "x$mm_htmlrefdir" != x || mm_htmlrefdir=$mm_htmlrefpub
  ])
  AS_CASE([$mm_tagpath], [[*[\\/]*]],,
  [
    mm_doxytagfile=`$PKG_CONFIG --variable=doxytagfile "$3" 2>&AS_MESSAGE_LOG_FD`
    test "x$mm_doxytagfile" = x || mm_tagpath=$mm_doxytagfile
  ])
])[]dnl
  AC_MSG_RESULT([$mm_tagpath@$mm_htmlrefdir])

  AS_IF([test "x$USE_MAINTAINER_MODE" != xno && test ! -f "$mm_tagpath"],
        [AC_MSG_WARN([Doxygen tag file $2 not found])])
  AS_IF([test "x$mm_htmlrefdir" = x],
        [AC_MSG_WARN([Location of external $1 documentation not set])])[]dnl

  test "x$DOXYGEN_TAGFILES" = x || DOXYGEN_TAGFILES="$DOXYGEN_TAGFILES "
  DOXYGEN_TAGFILES=$DOXYGEN_TAGFILES[\]"$mm_tagpath=$[mm_htmlref]m4_ifval([$3], [pub], [dir])[\]"
  test "x$DOCINSTALL_FLAGS" = x || DOCINSTALL_FLAGS="$DOCINSTALL_FLAGS "
  DOCINSTALL_FLAGS=$DOCINSTALL_FLAGS"-l '$mm_tagname@$mm_htmlrefdir'"dnl
])

## MM_ARG_WITH_TAGFILE_DOC(tagfilename, [module])
##
## Provide a --with-<tagfilebase>-doc=[/path/tagfile@]htmlrefdir configure
## option, which may be used to specify the location of a tag file and the
## path to the corresponding HTML reference documentation.  If the project
## provides the maintainer mode option and maintainer mode is not enabled,
## the user does not have to provide the full path to the tag file.  The
## full path is only required for rebuilding the documentation.
##
## If the optional <module> argument has been specified, and either the tag
## file or the HTML location have not been overridden by the user already,
## try to retrieve the missing paths automatically via pkg-config.  Also ask
## pkg-config for the URI to the online documentation, for use as the preset
## location when the documentation is generated.
##
## A warning message will be shown if the HTML path could not be determined.
## If maintainer mode is active, a warning is also displayed if the tag file
## could not be found.
##
## The results are appended to the substitution variables DOXYGEN_TAGFILES
## and DOCINSTALL_FLAGS, using the following format:
##
##  DOXYGEN_TAGFILES = "/path/tagfile=htmlrefpub" [...]
##  DOCINSTALL_FLAGS = -l 'tagfile@htmlrefdir' [...]
##
## The substitutions are intended to be used for the Doxygen configuration,
## and as argument list to the doc-install.pl or installdox utility.
##
AC_DEFUN([MM_ARG_WITH_TAGFILE_DOC],
[dnl
m4_assert([$# >= 1])[]dnl
m4_ifval([$2], [AC_REQUIRE([PKG_PROG_PKG_CONFIG])])[]dnl
AC_REQUIRE([MM_ARG_ENABLE_DOCUMENTATION])[]dnl
dnl
AS_IF([test "x$ENABLE_DOCUMENTATION" != xno], [_MM_ARG_WITH_TAGFILE_DOC(
  m4_quote(m4_bpatsubst([$1], [\([-+][0123456789]\|[+]*[._]\).*$])), [$1], [$2])])[]dnl
])
