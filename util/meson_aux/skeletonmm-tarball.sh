#!/bin/sh -e

# External command, intended to be called with custom_target() in meson.build

# skeletonmm-tarball.sh <source_dir> <output_file> <input_files...>

source_dir="$1"
output_file="$2"
shift 2

# -chof == --create --dereference --old-archive --file (Posix does not support long options.)
tar_options="-chof -"

case "$output_file" in
  *.xz)
    ( cd "$source_dir"; tar $tar_options "$@" ) | xz --to-stdout --extreme >"$output_file"
    ;;
  *.gz)
    ( cd "$source_dir"; tar $tar_options "$@" ) | gzip --to-stdout --best --no-name >"$output_file"
    ;;
  *) echo "Error: Unknown filetype, $output_file"
     exit 1
     ;;
esac
