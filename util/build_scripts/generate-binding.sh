#!/bin/sh -e

# External command, intended to be called with run_command(), custom_target(),
# meson.add_install_script() and meson.add_dist_script().

#         $0                $1       $2...
# generate-binding.sh <subcommand> <xxx>...

subcommand="$1"
shift

case "$subcommand" in
generate_wrap_init)
  #      $1           $2            $3          $4...
  # <gmmproc_dir> <output_file> <namespace> <hg_files>...

  # <gmmproc_dir> is an absolute path in glibmm's installation directory.
  # <output_file> is a relative or absolute path in the build directory.
  # <hg_files> are relative or absolute paths in the source directory.
  gmmproc_dir="$1"
  output_file="$2"
  output_dir="$(dirname "$2")"
  parent_dir="$(basename "$output_dir")"
  namespace="$3"
  shift 3

  perl -- "$gmmproc_dir/generate_wrap_init.pl" --namespace="$namespace" --parent_dir="$parent_dir" "$@" >"$output_file"
  ;;
gmmproc)
  #      $1             $2            $3          $4        $5...
  # <gmmproc_dir> <output_file> <basefilename> <src_dir> <m4_dirs>...

  # <gmmproc_dir> is an absolute path in glibmm's installation directory.
  # <output_file> is a relative or absolute path in the build directory.
  # <src_dir> is an absolute path in the source directory.
  # <m4_dirs> are absolute paths in the source directory.
  gmmproc_dir="$1"
  output_file="$2"
  output_dir="$(dirname "$2")"
  basefilename="$3" # name without filetype
  src_dir="$4"
  shift 4

  include_m4_dirs=""
  for dir in "$@"; do
    include_m4_dirs="$include_m4_dirs -I $dir"
  done

  # Create the private/ directory, if it does not exist.
  # -p == --parents (Posix does not support long options.)
  mkdir -p "$output_dir/private"

  # gmmproc generates $output_dir/$basefilename.cc, $output_dir/$basefilename.h
  # and $output_dir/private/${basefilename}_p.h
  perl -I"$gmmproc_dir/pm" -- "$gmmproc_dir/gmmproc" $include_m4_dirs \
    --defs "$src_dir" "$basefilename" "$src_dir" "$output_dir"

  # gmmproc does not update the timestamps of output files that have not changed.
  # That's by design, to avoid unnecessary recompilations.
  # The updated timestamp of $output_file shows meson that this custom_target()
  # has been updated.
  touch "$output_file"
  ;;
install_built_h_files)
  #      $1             $2              $3...
  # <built_h_dir> <install_subdir> <basefilenames>...

  # <built_h_dir> is an absolute path in the build directory or source directory.
  # <install_subdir> is an installation directory, relative to {prefix}.
  built_h_dir="$1"
  install_dir="$MESON_INSTALL_DESTDIR_PREFIX/$2"
  shift 2

  # Create the install directory, if it does not exist.
  # -p == --parents
  mkdir -p "$install_dir/private"
  
  for file in "$@"; do
    echo Installing $built_h_dir/$file.h to $install_dir
    # -p == --preserve
    cp -p "$built_h_dir/$file.h" "$install_dir"
    echo Installing $built_h_dir/private/${file}_p.h to $install_dir/private
    cp -p "$built_h_dir/private/${file}_p.h" "$install_dir/private"
  done
  ;;
dist_built_files)
  #        $1            $2          $3...
  # <built_h_cc_dir> <dist_dir> <basefilenames>...

  # <built_h_cc_dir> is an absolute path in the build directory or source directory.
  # <dist_dir> is a distribution directory, relative to $MESON_DIST_ROOT.
  built_h_cc_dir="$1"
  dist_dir="$MESON_DIST_ROOT/$2"
  shift 2

  # Create the distribution directory, if it does not exist.
  # -p == --parents
  mkdir -p "$dist_dir/private"
  
  # Distribute wrap_init.cc.
  cp "$built_h_cc_dir/wrap_init.cc" "$dist_dir"

  # Distribute .h/_p.h/.cc files built from .hg/.ccg files.
  for file in "$@"; do
    cp "$built_h_cc_dir/$file.h" "$built_h_cc_dir/$file.cc" "$dist_dir"
    cp "$built_h_cc_dir/private/${file}_p.h" "$dist_dir/private"
  done
  ;;
copy_built_files)
  #     $1        $2          $3...
  # <from_dir> <to_dir> <basefilenames>...

  # <from_dir> is an absolute or relative path of the directory to copy from.
  # <to_dir> is an absolute or relative path of the directory to copy to.
  from_dir="$1"
  to_dir="$2"
  shift 2

  # Create the destination directory, if it does not exist.
  # -p == --parents
  mkdir -p "$to_dir/private"
  
  # Copy some built files if they exist in $from_dir, but not in the destination
  # directory, or if they are not up to date in the destination directory.
  # (The term "source directory" is avoided here, because $from_dir might not
  # be what Meson calls a source directory as opposed to a build directory.)

  # Copy wrap_init.cc.
  from="$from_dir/wrap_init.cc"
  to="$to_dir/wrap_init.cc"
  if [ -f "$from" ] && { [ ! -f "$to" ] || [ "$from" -nt "$to" ]; }; then
    cp "$from" "$to"
  fi
  # Copy .h/_p.h/.cc files built from .hg/.ccg files.
  for basefile in "$@"; do
    for file in "$basefile.h" "$basefile.cc"; do
      from="$from_dir/$file"
      to="$to_dir/$file"
      if [ -f "$from" ] && { [ ! -f "$to" ] || [ "$from" -nt "$to" ]; }; then
        cp "$from" "$to"
      fi
    done
    from="$from_dir/private/${basefile}_p.h"
    to="$to_dir/private/${basefile}_p.h"
    if [ -f "$from" ] && { [ ! -f "$to" ] || [ "$from" -nt "$to" ]; }; then
      cp "$from" "$to"
    fi
  done
  ;;
esac
