#!/bin/sh -e

# External command, intended to be called with meson.add_dist_script() in meson.build

# dist-changelog.sh <root_source_dir>

# Make a ChangeLog file for distribution.
git --git-dir="$1/.git" --work-tree="$1" log --no-merges --date=short --max-count=200 \
    --pretty='tformat:%cd  %an  <%ae>%n%n  %s%n%w(0,0,2)%+b' > "$MESON_DIST_ROOT/ChangeLog"
