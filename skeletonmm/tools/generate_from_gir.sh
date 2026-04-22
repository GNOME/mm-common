#!/bin/bash

# skeletonmm/tools/generate_from_gir.sh

# Global environment variables:
# GMMPROC_GEN_SOURCE_DIR  Top directory where source files are searched for.
#                         Default value: $(dirname "$0")/../..
#                         i.e. 2 levels above this file.
# GMMPROC_GEN_BUILD_DIR   Top directory where built files are searched for.
#                         Default value: $GMMPROC_GEN_SOURCE_DIR
# GMMPROC_GEN_INSTALL_DIR Top directory where installed files are searched for.
#                         Default value: $HOME/jhbuild/install
#
# If you use jhbuild, you can set these environment variables equal to jhbuild's
# configuration variables checkoutroot, buildroot and prefix, respectively.
# Usually you can leave GMMPROC_GEN_SOURCE_DIR undefined.
# If you have set buildroot=None, GMMPROC_GEN_BUILD_DIR can be undefined.
# If you have not defined prefix in $HOME/.config/jhbuildrc, and there is no /opt/gnome
# directory, GMMPROC_GEN_INSTALL_DIR can be undefined.

# Generated files:
#   skeletonmm/skeleton/src/skeleton_docs.xml
#   skeletonmm/skeleton/src/skeleton_enums.defs
#   skeletonmm/skeleton/src/skeleton_methods.defs
#   skeletonmm/skeleton/src/skeleton_signals.defs
#   skeletonmm/skeleton/src/skeleton_vfuncs.defs

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

# Where to search for installed files.
if [ -z "$GMMPROC_GEN_INSTALL_DIR" ]; then
  GMMPROC_GEN_INSTALL_DIR="$HOME/jhbuild/install"
fi

# Script in glibmm. This is a source file.
gen_docs="$GMMPROC_GEN_SOURCE_DIR/glibmm/tools/defs_gen/docextract_to_xml.py"

# Where to find the executable that generates defs files from GIR files.
gen_with_mmgir="$GMMPROC_GEN_BUILD_DIR/glibmm/tools/mmgir/mmgir"

source_prefix="$GMMPROC_GEN_SOURCE_DIR/skeleton"
build_prefix="$GMMPROC_GEN_BUILD_DIR/skeleton"
if [ "$source_prefix" == "$build_prefix" ]; then
  # skeleton is built with meson, which requires non-source-dir builds.
  # This is what jhbuild does, if necessary, to force non-source-dir builds.
  build_prefix="$build_prefix/build"
fi

gir_dir="$GMMPROC_GEN_INSTALL_DIR/share/gir-1.0"
out_dir="$root_dir/skeleton/src"

echo ===== Documentation
params="--with-properties --no-recursion"
for dir in "$source_prefix/skeleton" "$build_prefix/skeleton"; do
  if [ -d "$dir" ]; then
    params="$params -s $dir"
  fi
done
"$gen_docs" $params > "$out_dir/skeleton_docs.xml"

echo; echo ===== Enums, methods, signals and vfuncs
"$gen_with_mmgir" --gir "$gir_dir"/Skeleton-1.0.gir \
  --gir-search-dir "$gir_dir" \
  --enum-defs "$out_dir"/skeleton_enums.defs \
  --function-defs "$out_dir"/skeleton_methods.defs \
  --signal-defs "$out_dir"/skeleton_signals.defs \
  --vfunc-defs "$out_dir"/skeleton_vfuncs.defs

