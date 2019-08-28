#!/bin/sh -e

# External command, intended to be called with meson.add_dist_script() in meson.build

#                            $1                $2
# dist-build-scripts.sh <root_src_dir> <relative_script_dir>

# <relative_script_dir> is the directory with the build scripts, relative to <root_source_dir>.
src_script_dir="$1/$2"
dist_script_dir="$MESON_DIST_ROOT/$2"

# Create the distribution directory, if it does not exist.
# -p == --parents (Posix does not support long options.)
mkdir -p "$dist_script_dir"

# Distribute files that mm-common-prepare has copied to $src_script_dir.
for file in dist-build-scripts.sh dist-changelog.sh doc-reference.sh generate-binding.sh; do
  cp "$src_script_dir/$file" "$dist_script_dir/"
done

# Remove all .gitignore files and an empty $MESON_DIST_ROOT/build directory.
find "$MESON_DIST_ROOT" -name ".gitignore" -exec rm '{}' \;
if [ -d "$MESON_DIST_ROOT/build" ]; then
  # Ignore the error, if not empty.
  rmdir "$MESON_DIST_ROOT/build" 2>/dev/null || true
fi
