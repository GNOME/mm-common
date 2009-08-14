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

#serial 20090814

## MM_PKG_CONFIG_SUBST(variable, arguments, [action-if-found], [action-if-not-found])
##
## Run the pkg-config utility with the specified command-line <arguments>
## and capture its standard output in the named shell <variable>.  If the
## command exited successfully, execute <action-if-found> in the shell if
## specified.  If the command failed, run <action-if-not-found> if given,
## otherwise ignore the error.
##
AC_DEFUN([MM_PKG_CONFIG_SUBST],
[dnl
m4_assert([$# >= 2])[]dnl
AC_REQUIRE([_MM_PRE_INIT])[]dnl
AC_REQUIRE([PKG_PROG_PKG_CONFIG])[]dnl
AC_MSG_CHECKING([for $1])

AS_IF([test -z "${$1+set}"],
      [$1=`$PKG_CONFIG $2 2>&AS_MESSAGE_LOG_FD`
       AS_IF([test "[$]?" -eq 0], [$3], [$4])])

AC_MSG_RESULT([[$]$1])
AC_SUBST([$1])[]dnl
])
