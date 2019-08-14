#!/bin/sh -e

# External command, intended to be called with custom_target() in meson.build

# libstdcxx-tag.sh <curl-or-wget-or-none> <srcdir> <output_path>

output_dirname="$(dirname "$3")"
output_filename="$(basename "$3")"

# Remote location of the GNU libstdc++ Doxygen tag file.
libstdcxx_tag_url="http://gcc.gnu.org/onlinedocs/libstdc++/latest-doxygen/$output_filename"

case "$1" in
  curl)
    # These options don't contain filenames, and thus no spaces that
    # must be preserved in the call to curl.
    simple_curl_options="--compressed --connect-timeout 300 --globoff --location --max-time 3600 --remote-time --retry 5"
    if [ -f "$3" ]; then
      curl $simple_curl_options --time-cond "$3" --output "$3" "$libstdcxx_tag_url"
    else
      curl $simple_curl_options --output "$3" "$libstdcxx_tag_url"
    fi
    ;;
  wget)
    wget --timestamping --no-directories --timeout=300 --tries=5 \
         --directory-prefix="$output_dirname" "$libstdcxx_tag_url"
    ;;
  *)
    if [ -f "$3" ]; then
      echo "Did not check status of $3 because network is disabled."
    elif [ -f "$2/$output_filename" ]; then
      echo "Warning: $3 does not exist."
      echo "Copying from the source directory because network is disabled."
      echo "If you want an up-to-date copy, reconfigure with the -Duse-network=true option."
      cp --preserve=timestamps "$2/$output_filename" "$3"
    else
      echo "Error: $3 does not exist." >&2
      echo "Downloading it is not possible because network is disabled." >&2
      echo "Please reconfigure with the -Duse-network=true option." >&2
      exit 1
    fi
    ;;
esac
