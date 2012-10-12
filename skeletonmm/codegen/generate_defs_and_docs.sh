#!/bin/bash

# skeletonmm/codegen/generate_defs_and_docs.sh

# This script must be executed from directory skeletonmm/codegen.

# Assumed directory structure:
#   glibmm/tools/defs_gen/docextract_to_xml.py
#   glibmm/tools/defs_gen/h2def.py
#   glibmm/tools/enum.pl
#   skeleton/src/*.h
#   skeleton/src/*.c
#   skeletonmm/codegen/extradefs/generate_extra_defs

# Generated files:
#   skeletonmm/skeleton/src/skeleton_docs.xml
#   skeletonmm/skeleton/src/skeleton_enum.defs
#   skeletonmm/skeleton/src/skeleton_method.defs
#   skeletonmm/skeleton/src/skeleton_signal.defs

GLIBMM_TOOLS_DIR=../../glibmm/tools
SKELETON_DIR=../../skeleton
SKELETONMM_SKELETON_SRC_DIR=../skeleton/src

$GLIBMM_TOOLS_DIR/defs_gen/docextract_to_xml.py \
  -s $SKELETON_DIR/src \
  >$SKELETONMM_SKELETON_SRC_DIR/skeleton_docs.xml

$GLIBMM_TOOLS_DIR/enum.pl \
  $SKELETON_DIR/src/*.h \
  >$SKELETONMM_SKELETON_SRC_DIR/skeleton_enum.defs

$GLIBMM_TOOLS_DIR/defs_gen/h2def.py \
  $SKELETON_DIR/src/*.h \
  >$SKELETONMM_SKELETON_SRC_DIR/skeleton_method.defs

extradefs/generate_extra_defs \
  >$SKELETONMM_SKELETON_SRC_DIR/skeleton_signal.defs

