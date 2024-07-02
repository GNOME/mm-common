# mm-common overview

The following sections provide an overview of the various files shipped
with mm-common, and briefly explain their purpose.  Detailed documentation
and usage instructions can be found in the files themselves.

## mm-common-prepare and Autotools

The mm-common-prepare shell script is installed in ${bindir} and must be
invoked from the bootstrap script of a binding module in order to set up
necessary support files in the project's source tree.  It should be run
before any of Autotools' own setup utilities.  The classic command line
options such as --copy and --force can be used to adjust the behavior of
mm-common-prepare.  A typical autogen.sh would look like this:
```
  #! /bin/sh -e
  test -n "$srcdir" || srcdir=`dirname "$0"`
  test -n "$srcdir" || srcdir=.

  mm-common-prepare --copy --force "$srcdir"
  autoreconf --force --install --verbose "$srcdir"
  test -n "$NOCONFIGURE" || "$srcdir/configure" --enable-maintainer-mode "$@"
```
Do not forget to set:
```
  ACLOCAL_AMFLAGS = -I build ${ACLOCAL_FLAGS}
```
in your project's top-level Makefile.am.  "build" should be changed to the
name of the Autoconf M4 macro subdirectory of your project's source tree.
Also note that mm-common-prepare inspects the project's configure.ac file
for the AC_CONFIG_AUX_DIR([...]) argument.  This is explained in further
detail below in the section on Automake include files.

## mm-common-get and Meson

The mm-common-get shell script is installed in ${bindir} and must be
invoked with run_command() early in a meson.build file. The meson.build file
should contain code similar to
```
  python3 = find_program('python3', version: '>= 3.7')
  # Do we build from a git repository?
  # Suppose we do if and only if the meson.build file is tracked by git.
  cmd_py = '''
  import shutil, subprocess, sys
  git_exe = shutil.which('git')
  if not git_exe:
    sys.exit(1)
  cmd = [ git_exe, 'ls-files', '--error-unmatch', 'meson.build' ]
  sys.exit(subprocess.run(cmd, cwd=sys.argv[1], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode)
  '''
  is_git_build = run_command(python3, '-c', cmd_py, project_source_root, check: false).returncode() == 0
  maintainer_mode_opt = get_option('maintainer-mode')
  maintainer_mode = maintainer_mode_opt == 'true' or \
                   (maintainer_mode_opt == 'if-git-build' and is_git_build)
  mm_common_get = find_program('mm-common-get', required: false)
  if maintainer_mode and not mm_common_get.found()
    message('Maintainer mode requires the \'mm-common-get\' command. If it is not found,\n' +
            'install the \'mm-common\' package, version 1.0.0 or higher.')
    # If meson --wrap-mode != forcefallback, Meson falls back to the mm-common
    # subproject only if mm-common-get is required.
    mm_common_get = find_program('mm-common-get', required: true)
  endif
  if maintainer_mode
    # Copy files to untracked/build_scripts and untracked/docs.
    run_command(mm_common_get, '--force',
      project_source_root / 'untracked' / 'build_scripts',
      project_source_root / 'untracked' / 'docs',
      check: true,
    )
  endif
```

## Autoconf M4 macros (Autotools)

The Autoconf M4 macros are installed into the system-wide macro repository
in the ${datadir}/aclocal directory.  Since all used M4 macros are copied
into aclocal.m4, these macro files are required only in maintainer-mode.
For this reason, they are not copied into the source tree of a project by
mm-common-prepare.  If mm-common is installed to a different prefix than
Automake, it may be necessary to adjust ACLOCAL_PATH accordingly so that
aclocal can find the M4 files:
```
  export ACLOCAL_PATH="${mm_common_prefix}/share/aclocal"
```
This step is not necessary when using jhbuild, as it takes care of setting
up the environment for using the locally built modules.

- macros/mm-common.m4: (generated from macros/mm-common.m4.in) \
  Provides MM_PREREQ() for requiring a minimum version of mm-common, and
  an internal initialization macro shared by the other mm-common macros.

- macros/mm-warnings.m4: \
  Implements the MM_ARG_ENABLE_WARNINGS() Autoconf macro for easy setup
  of compiler diagnostics through the --enable-warnings configure option.

- macros/mm-doc.m4: \
  Implements the MM_ARG_ENABLE_DOCUMENTATION() Autoconf macro to initialize
  the documentation support for a C++ binding package.  Among other things,
  it provides the --enable-documentation configure option, and checks for
  the required utilities.
  The other Autoconf macro defined here is MM_ARG_WITH_TAGFILE_DOC(), which
  ties all the ends together in order to make cross-referencing to external
  documentation work.  This macro should be called once for each external
  Doxygen tag file a binding package depends on.  It implements a configure
  option to override tag file locations, attempts automatic configuration
  if possible, and takes care of building the list of tag files and their
  default base paths for substitution into the configuration Doxyfile.  It
  also generates the command line options for doc-install.pl.

- macros/mm-module.m4: \
  The magic MM_INIT_MODULE() macro takes care of defining the various
  substitution variables and preprocessor macros to identify the name,
  version and API version of a C++ binding module.

- macros/mm-pkg.m4: \
  The helper macro MM_PKG_CONFIG_SUBST, which simplifies the retrieval of
  specific configuration values from pkg-config.  Checks for particular
  utility programs are also defined here, such as MM_CHECK_GNU_MAKE and
  MM_CHECK_PERL.

- macros/mm-dietlib.m4: \
  Implements Autoconf macros which provide options intended to reduce the
  binary size of the generated binding library, typically for embedded use.
  The MM_PROG_GCC_VISIBILITY macro is defined in this file as well.

- macros/mm-ax_cxx_compile_stdcxx.m4: \
  Implements the MM_AX_CXX_COMPILE_STDCXX() macro to test and set flags
  for C++11/14/17 compatibility of the C++ compiler. This is identical to the
  AX_CXX_COMPILE_STDCXX() macro described at
  <http://www.gnu.org/software/autoconf-archive/ax_cxx_compile_stdcxx.html>,
  except for the MM_ prefix.

## Automake include files (Autotools)

The Automake include files are located in the am_include/ directory.
The installed mm-common-prepare program copies all of the .am files into
a project's source tree.  If AC_CONFIG_AUX_DIR([...]) is specified in
the configure.ac file, the .am files will be placed in the indicated
subdirectory.

- am_include/generate-binding.am: \
  Variables and rules for running the gmmproc code generator to produce
  the source code files for a C++ binding module.

- am_include/compile-binding.am: \
  Variables and rules for compiling and linking the shared library which
  implements a C++ binding module.

- am_include/doc-reference.am: \
  Variables and rules for building the API reference documentation using
  Doxygen, and to create a Devhelp book for the library.  The installation
  rules also take care of translating references to external documentation
  in the generated hypertext documents.

- am_include/dist-changelog.am: \
  A dist-hook rule to automatically generate a ChangeLog file when making
  a release, intended to be used by modules which use the version control
  log exclusively to document changes.

## Python build scripts (Meson)

These scripts can be called from meson.build files with run_command(),
custom_target(), meson.add_postconf_script(), meson.add_install_script()
and meson.add_dist_script().

- util/build_scripts/generate-binding.py: \
  Commands for running the gmmproc code generator to produce
  the source code files for a C++ binding module.

- util/build_scripts/doc-reference.py: \
  Commands for building the API reference documentation using
  Doxygen, and to create a Devhelp book for the library. The installation
  rules also take care of translating references to external documentation
  in the generated hypertext documents.

- util/build_scripts/dist-changelog.py: \
  A git command to generate a ChangeLog file when making a release,
  intended to be used by modules which use the version control
  log exclusively to document changes.

- util/build_scripts/dist-build-scripts.py: \
  Commands that trim the distribution directory before a tarball is made.
  The scripts copied by mm-common-get are distributed, although they are
  not checked into the git repository. All .gitignore files and an empty build/
  directory are removed

- util/build_scripts/check-dllexport-usage.py: \
  Command that checks on the gmmproc version that is to be used or has been used
  to generate the sources, to check whether to use compiler directives to
  export symbols.  Only used for Visual Studio or clang-cl builds.

## Documentation utilities (Meson and Autotools)

These are two Perl scripts and two equivalent Python scripts, a style sheet,
and one XSL transformation which assist with the task of generating and installing
the Doxygen reference documentation.  At least doc-install.pl or doc-install.py
is also required for tarball builds. Autotools uses the Perl scripts.
Meson uses the Python scripts.

Autotools: To avoid copying these files into all binding modules, they are
distributed and installed with the mm-common module.  Those binding modules
which shall depend on mm-common only in maintainer-mode must call
MM_CONFIG_DOCTOOL_DIR([...]) in configure.ac to indicate to mm-common-prepare
that it should copy the documentation utilities into the project's source tree.
Otherwise the files installed with mm-common will be used automatically.

- util/doc-postprocess.pl: \
  util/doc_postprocess.py: \
  A simple script to post-process the HTML files generated by Doxygen.
  It replaces various code constructs that do not match the coding style
  used throughout the C++ bindings.  For instance, it rewrites function
  prototypes in order to place the reference symbol (&) next to the type
  instead of the name of the argument.

- util/doc-install.pl: \
  util/doc_install.py: \
  A replacement for the installdox script generated by Doxygen.  Its
  purpose is to translate references to external documentation at the
  time the documentation is installed.  This step is necessary because
  the documentation is included in the tarballs, and the location of
  external documentation on the installation system is not known at the
  time the documentation is generated.
  Apart from replacing the functionality of installdox, doc-install.pl
  also acts as a drop-in replacement for the classic BSD install command
  for easy integration with Automake.  It also translates Devhelp books
  as well, and will happily pass through unrecognized files without any
  alterations.

- util/doxygen.css: \
  A Cascading Style Sheet to unify the appearance of the HTML reference
  documentation generated by Doxygen for each C++ binding module.
  This file is deprecated. Use util/doxygen-extra.css instead.

- util/doxygen-extra.css: \
  A Cascading Style Sheet to unify the appearance of the HTML reference
  documentation generated by Doxygen for each C++ binding module.

- util/tagfile-to-devhelp2.xsl: \
  An XSLT script to generate a Devhelp2 book for the Doxygen reference
  documentation.  The generated Doxygen tag file serves as the input of
  the translation.

## GNU C++ Library tag file

All modules in the GNOME C++ bindings set make use of the C++ standard
library in the API.  As the GNU C++ Library shipped with GCC also uses
Doxygen for its reference documentation, its tag file is made available
by mm-common at a shared location for use by all C++ binding modules.

- doctags/libstdc++.tag: \
  The Doxygen tag file for the GNU libstdc++ reference documentation
  hosted at <http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/>.
  This file is distributed with release archives of mm-common, but not
  checked into version control on gnome.org.  If mm-common is built with
  Autotools in maintainer-mode or with Meson and use-network=true,
  the file will be downloaded automatically from the gcc.gnu.org web server.
  The file libstdc++.tag is installed into the package data directory
  of mm-common.  The mm-common-libstdc++ pkg-config module defines the
  variables ${doxytagfile} and ${htmlrefpub}, which can be queried for
  the location of the tag file and the URL of the online documentation.
