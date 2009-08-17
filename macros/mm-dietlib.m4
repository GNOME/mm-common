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

#serial 20090817

## _MM_ARG_DISABLE_DEPRECATED_API_OPTION
##
## Implementation helper macro of MM_ARG_DISABLE_DEPRECATED_API().  Pulled
## in through AC_REQUIRE() so that it will only be expanded once.
##
m4_define([_MM_ARG_DISABLE_DEPRECATED_API_OPTION],
[dnl
AC_PROVIDE([$0])[]dnl
AC_ARG_ENABLE([deprecated-api],
              [AS_HELP_STRING([--disable-deprecated-api],
                              [omit deprecated API from the library])],
              [mm_enable_deprecated_api=$enableval],
              [mm_enable_deprecated_api=yes])[]dnl
AS_IF([test "x$mm_enable_deprecated_api" = xno],
      [AC_MSG_WARN([[Deprecated API will not be built, breaking compatibility.
Do not use this option for distribution packages.]])],
      [AC_MSG_NOTICE([[Deprecated API will be built, for backwards-compatibility.]])])
AM_CONDITIONAL([DISABLE_DEPRECATED_API], [test "x$mm_enable_deprecated_api" = xno])[]dnl
])

## _MM_ARG_DISABLE_DEPRECATED_API_DEFINE(define-prefix [define-prefix ...])
##
## Implementation helper macro of MM_ARG_DISABLE_DEPRECATED_API().  Expands
## to a list of AC_DEFINE() calls, one for each prefix in the argument list.
##
m4_define([_MM_ARG_DISABLE_DEPRECATED_API_DEFINE],
[m4_foreach_w([mm_prefix], [$1],
[AC_DEFINE(m4_defn([mm_prefix])[_DISABLE_DEPRECATED], [1],
           [Define to omit deprecated API from the library.])
])])

## MM_ARG_DISABLE_DEPRECATED_API([define-prefix [define-prefix ...]])
##
## Provide the --disable-deprecated-api configure option, which may be used
## to trim the size of the resulting library at the cost of breaking binary
## compatibility.  By default, deprecated API will be built.
##
## Each <define-prefix> in the whitespace-separated argument list is expanded
## to a C preprocessor macro name <define-prefix>_DISABLE_DEPRECATED, which
## will be defined to 1 in the generated configuration header if the option
## to disable deprecated API is used.  The DISABLE_DEPRECATED_API Automake
## conditional is provided as well.
##
AC_DEFUN([MM_ARG_DISABLE_DEPRECATED_API],
[dnl
AC_REQUIRE([_MM_PRE_INIT])[]dnl
AC_REQUIRE([_MM_ARG_DISABLE_DEPRECATED_API_OPTION])[]dnl
AS_IF([test "x$mm_enable_deprecated_api" = xno],
      [_MM_ARG_DISABLE_DEPRECATED_API_DEFINE(
        m4_ifval([$1], [[$1]], [AS_TR_CPP(m4_defn([AC_PACKAGE_TARNAME]))]))])[]dnl
])
