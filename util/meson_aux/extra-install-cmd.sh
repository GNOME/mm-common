#!/bin/bash -e

# External command, intended to be called with meson.add_install_script() in meson.build

# extra-install-cmd.sh <aclocal_macrodir>

if [ -z "$DESTDIR" ]; then
  # Inform the installer that M4 macro files installed in a directory
  # not known to aclocal will not be picked up automatically.
  acdir="$(aclocal --print-ac-dir 2>/dev/null || :)"
  case ":$ACLOCAL_PATH:$acdir:" in
    *":$1:"*)
      ;;
    *)
      echo "NOTE"
      echo "----"
      echo "The mm-common Autoconf macro files have been installed in a different"
      echo "directory than the system aclocal directory. In order for the installed"
      echo "macros to be found, it may be necessary to add the mm-common include"
      echo "path to the ACLOCAL_PATH environment variable:"
      echo "  ACLOCAL_PATH=\"\$ACLOCAL_PATH:$1\""
      echo "  export ACLOCAL_PATH"
      ;;
  esac
fi
