# mm-common

This module is part of the GNOME C++ bindings effort <https://gtkmm.gnome.org/>.

# General information

The mm-common module provides the build infrastructure and utilities
shared among the GNOME C++ binding libraries.  It is only a required
dependency for building the C++ bindings from the gnome.org version
control repository.  An installation of mm-common is not required for
building tarball releases, unless configured to use maintainer-mode.

Release archives of mm-common include the Doxygen tag file for the
GNU C++ Library reference documentation.  It is covered by the same
licence as the source code it was extracted from.  More information
is available at <http://gcc.gnu.org/onlinedocs/libstdc++/>.

Web site
 - https://gtkmm.gnome.org

Download location
 - https://download.gnome.org/sources/mm-common

Discussion on GNOME's discourse forum
 - https://discourse.gnome.org/tag/cplusplus
 - https://discourse.gnome.org/c/platform

Git repository
 - https://gitlab.gnome.org/GNOME/mm-common

Bugs can be reported to
 - https://gitlab.gnome.org/GNOME/mm-common/issues

Patches can be submitted to
 - https://gitlab.gnome.org/GNOME/mm-common/merge_requests

# Autotools or Meson?

mm-common can be built with Autotools or Meson. Autotools support may be
dropped in the future.

The files that mm-common installs and mm-common-prepare copies to other
modules are useful in modules that are built with Autotools.
The files that mm-common installs and mm-common-get copies to other
modules are useful in modules that are built with Meson.

The files in the skeletonmm directory show the start of a project that will
use Meson.

# Skeleton C++ binding module

When creating a new C++ binding module based on mm-common, the easiest way
to get started is to copy the `skeletonmm` directory shipped with mm-common.
It contains the build support files required for a C++ binding module using
Meson, gmmproc and glibmm.

In order to create a new binding project from the copied skeleton directory,
any files which have `skeleton` in the filename must be renamed.  References
to the project name or author in the files need to be substituted with the
actual name and author of the new binding.

# mm-common overview

See [OVERVIEW.md](OVERVIEW.md) for an overview of the files shipped with mm-common.
