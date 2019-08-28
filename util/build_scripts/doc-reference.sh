#!/bin/sh -e

# External command, intended to be called with custom_target(),
# meson.add_install_script() or meson.add_dist_script() in meson.build.

#         $0            $1            $2        $3...
# doc-reference.sh <subcommand> <MMDOCTOOLDIR> <xxx>...

# <MMDOCTOOLDIR> is an absolute path in the source directory.

subcommand="$1"
MMDOCTOOLDIR="$2"
shift 2

case "$subcommand" in
doxygen)
  #      $1             $2...
  # <doxytagfile> <doc_input_files>...

  # <doxytagfile> is a relative or absolute path in the build directory.
  # <doc_input_files> are absolute paths in the source or build directory.
  doxytagfile="$1"
  doc_outdir="$(dirname "$1")"
  shift

  # Export this variable for use in the Doxygen configuration file.
  export MMDOCTOOLDIR

  # Remove old files.
  # -fR == --force --recursive
  rm -f "$doxytagfile"
  rm -fR "$doc_outdir/html"

  # Relative paths in Doxyfile assume that Doxygen is run from the
  # build directory one level above Doxyfile.
  saved_wd="$(pwd)"
  cd "$doc_outdir/.."
  if [ -z "$DOXYGEN" ]; then
    DOXYGEN=doxygen
  fi
  (echo '@INCLUDE =' reference/Doxyfile && echo 'INPUT =' $*) | "$DOXYGEN" -
  cd "$saved_wd"
	perl -- "$MMDOCTOOLDIR/doc-postprocess.pl" "$doc_outdir/html/*.html"
  ;;
devhelp)
  #      $1            $2            $3         $4
  # <doxytagfile> <devhelpfile> <book_name> <book_title>

  # <doxytagfile> and <devhelpfile> are relative or absolute paths in the build directory.
  doxytagfile="$1"
  devhelpfile="$2"
  book_name="$3"
  book_title="$4"
  tagfile_to_devhelp="$MMDOCTOOLDIR/tagfile-to-devhelp2.xsl"

  # The parameters to the Doxygen-to-Devhelp XSLT script.
  xsltproc \
  	--stringparam book_title "$book_title" \
    --stringparam book_name "$book_name" \
    --stringparam book_base html \
    -o "$devhelpfile" "$tagfile_to_devhelp" "$doxytagfile"
  ;;
install_doc)
  #      $1            $2           $3           $4...
  # <devhelpfile> <devhelpdir> <htmlrefdir> <docinstall_flags>...

  # <devhelpfile> is a relative or absolute path in the build directory.
  # <htmlrefdir> and <devhelpdir> are installation directories, relative to {prefix}.
  devhelpfile="$1"
  devhelpdir="$MESON_INSTALL_DESTDIR_PREFIX/$2"
  htmlrefdir="$MESON_INSTALL_DESTDIR_PREFIX/$3"
  build_dir="$(dirname "$devhelpfile")"
  shift 3

  # Create the install directories, if they do not exist.
  # -p == --parents (Posix does not support long options.)
  mkdir -p "$htmlrefdir"
  mkdir -p "$devhelpdir"

  # Install html files.
  perl -- "$MMDOCTOOLDIR/doc-install.pl" --verbose --mode=0644 \
    "$@" -t "$htmlrefdir" --glob -- "$build_dir/html/*"

  # Install the Devhelp file.
  # ${name%/} means remove trailing /, if any.
  perl -- "$MMDOCTOOLDIR/doc-install.pl" --verbose --mode=0644 \
    --book-base="${htmlrefdir%/}" -t "$devhelpdir" -- "$devhelpfile"
  ;;
dist_doc)
  #        $1                 $2               $3        $4
  # <doctool_dist_dir> <doc_ref_build_dir> <tagfile> <devhelpfile>

  # <doctool_dist_dir> is a distribution directory, relative to $MESON_DIST_ROOT.
  # <doc_ref_build_dir> is a relative or absolute path in the build directory.
  # <tagfile> and <devhelpfile> are relative or absolute paths in the build directory.
  doctool_dist_dir="$MESON_DIST_ROOT/$1"
  doc_ref_build_dir="$2"
  tagfile="$3"
  devhelpfile="$4"

  # Create the distribution directory, if it does not exist.
  mkdir -p "$doctool_dist_dir/reference"

  # Distribute files that mm-common-prepare has copied to $MMDOCTOOLDIR.
  for file in doc-install.pl doc-postprocess.pl tagfile-to-devhelp2.xsl doxygen-extra.css; do
    cp "$MMDOCTOOLDIR/$file" "$doctool_dist_dir/"
  done

  # Distribute built files: tag file, devhelp file, html files.
  for file in "$tagfile" "$devhelpfile"; do
    cp "$file" "$doctool_dist_dir/reference/"
  done
  # -R == --recursive
  cp -R "$doc_ref_build_dir/html/" "$doctool_dist_dir/reference/"
  ;;
esac
