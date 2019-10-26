#!/usr/bin/env bash

# skeletonmm/codegen/generate_defs_and_docs.sh

# Global environment variables:
# GMMPROC_GEN_SOURCE_DIR  Top directory where source files are searched for.
#                         Default value: $(dirname "$0")/../..
#                         i.e. 2 levels above this file.
# GMMPROC_GEN_BUILD_DIR   Top directory where built files are searched for.
#                         Default value: $GMMPROC_GEN_SOURCE_DIR
#
# If you use jhbuild, you can set these environment variables equal to jhbuild's
# configuration variables checkoutroot and buildroot, respectively.
# Usually you can leave GMMPROC_GEN_SOURCE_DIR undefined.
# If you have set buildroot=None, GMMPROC_GEN_BUILD_DIR can also be undefined.

# Generated files:
#   skeletonmm/skeleton/src/skeleton_docs.xml
#   skeletonmm/skeleton/src/skeleton_enums.defs
#   skeletonmm/skeleton/src/skeleton_methods.defs
#   skeletonmm/skeleton/src/skeleton_signals.defs

# Root directory of skeletonmm source files.
root_dir="$(dirname "$0")/.."

# Where to search for source files.
if [ -z "$GMMPROC_GEN_SOURCE_DIR" ]; then
  GMMPROC_GEN_SOURCE_DIR="$root_dir/.."
fi

# Where to search for built files.
if [ -z "$GMMPROC_GEN_BUILD_DIR" ]; then
  GMMPROC_GEN_BUILD_DIR="$GMMPROC_GEN_SOURCE_DIR"
fi

# Scripts in glibmm. These are source files.
gen_docs="$GMMPROC_GEN_SOURCE_DIR/glibmm/tools/defs_gen/docextract_to_xml.py"
gen_methods="$GMMPROC_GEN_SOURCE_DIR/glibmm/tools/defs_gen/h2def.py"
gen_enums="$GMMPROC_GEN_SOURCE_DIR/glibmm/tools/enum.pl"

# Where to find the executable that generates extra defs (signals and properties).
extra_defs_gen_dir="$GMMPROC_GEN_BUILD_DIR/skeletonmm/tools/extra_defs_gen"
### If skeletonmm is built with meson:
if [ "$GMMPROC_GEN_SOURCE_DIR" == "$GMMPROC_GEN_BUILD_DIR" ]; then
  # skeletonmm is built with meson, which requires non-source-dir builds.
  # This is what jhbuild does, if necesary, to force non-source-dir builds.
  extra_defs_gen_dir="$GMMPROC_GEN_BUILD_DIR/skeletonmm/build/tools/extra_defs_gen"
fi
### If skeletonmm is built with autotools:
# skeletonmm is built with autotools.
# autotools support, but don't require, non-source-dir builds.

source_prefix="$GMMPROC_GEN_SOURCE_DIR/skeleton"
build_prefix="$GMMPROC_GEN_BUILD_DIR/skeleton"
### If skeleton is built with meson:
if [ "$source_prefix" == "$build_prefix" ]; then
  # skeleton is built with meson, which requires non-source-dir builds.
  # This is what jhbuild does, if neccesary, to force non-source-dir builds.
  build_prefix="$build_prefix/build"
fi
### If skeleton is built with autotools:
# skeleton is built with autotools, which support, but don't require, non-source-dir builds.

out_dir="$root_dir/skeleton/src"

# Documentation
echo === skeleton_docs.xml ===
params="--with-properties --no-recursion"
for dir in "$source_prefix/skeleton" "$build_prefix/skeleton"; do
  if [ -d "$dir" ]; then
    params="$params -s $dir"
  fi
done
"$gen_docs" $params > "$out_dir/skeleton_docs.xml"

shopt -s nullglob # Skip a filename pattern that matches no file

# Enums
echo === skeleton_enum.defs ===
"$gen_enums" "$source_prefix"/skeleton/*.h "$build_prefix"/skeleton/*.h  > "$out_dir/skeleton_enums.defs"

# Functions and methods
echo === skeleton_method.defs ===
"$gen_methods" "$source_prefix"/skeleton/*.h "$build_prefix"/skeleton/*.h  > "$out_dir/skeleton_methods.defs"

# Properties and signals
echo === skeleton_signal.defs ===
"$extra_defs_gen_dir"/generate_defs_skeleton > "$out_dir/skeleton_signals.defs"

