#!/bin/bash -e

# External command, intended to be called with meson.add_dist_script() in meson.build

# extra-dist-cmd.sh <root_source_dir> <root_build_dir> <relative_dist_dir>

# relative_dist_dir is the distribution directory path relative to root_build_dir.
# Meson does not preserve timestamps on distributed files.
# But this script preserves the timestamps on libstdc++.tag.

# Make a ChangeLog file for distribution.
git --git-dir="$1/.git" --work-tree="$1" log --no-merges --date=short --max-count=200 \
    --pretty='tformat:%cd  %an  <%ae>%n%n  %s%n%w(0,0,2)%+b' > "$2/$3/ChangeLog"

# Distribute the libstdc++.tag file in addition to the files in the local git clone.
cd "$2"
cp --preserve=timestamps "libstdc++.tag" "$3/doctags/"
